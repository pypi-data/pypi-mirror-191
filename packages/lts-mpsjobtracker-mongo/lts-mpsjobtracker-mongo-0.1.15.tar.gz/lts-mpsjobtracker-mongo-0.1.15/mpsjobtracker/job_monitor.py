import json, time, traceback
import datetime
from datetime import timedelta
# MQ utilities package
from mpsmqutils import mqutils
# Job tracker module
from mpsjobtracker.trackers.jobtracker import JobTracker, log_error_and_reraise
import celery as celeryapp
import os

job_tracker = JobTracker()

_success_queue = os.getenv("SUCCESS_QUEUE")
_failure_queue = os.getenv("FAILURE_QUEUE")
_max_child_errors = int(os.getenv("CHILD_ERROR_LIMIT", 10))

class JobMonitor():
    def __init__(self, progress_check_duration):
        self.progress_check_duration = timedelta(seconds=progress_check_duration)

    def run(self):
        while True:
            self.check_inprocess_jobs()
            time.sleep(self.progress_check_duration.seconds)


    def check_inprocess_jobs(self):
        current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0)
        print('Checking running jobs ' + str(current_time), flush=True)
        running_jobs = job_tracker.get_jobs('running')
        self.attempt_to_resolve_jobs(running_jobs, current_time)

        print("Checking for stalled queued jobs...", flush=True)
        queued_jobs = job_tracker.get_jobs('queued', {
            'parent_job_ref': {"$exists": False},
            'context.child_job_spawning_status': 'failure'
        })
        self.attempt_to_resolve_jobs(queued_jobs, current_time)
    
    def attempt_to_resolve_jobs(self, inprocess_jobs, current_time):
        for job_doc in inprocess_jobs:
            job_id = job_doc["_id"]
            print(f"inprocess job {str(job_id)}", flush=True)
            parent_ref = job_doc.get('parent_job_ref')
            child_job_spawning_status = 'unfinished'
            if 'context' in job_doc:
                child_job_spawning_status = job_doc['context'].get('child_job_spawning_status')
            
            # TODO: Check for tracker_doc child_job_spawning_status success, failure, unfinished
            if (parent_ref is None and child_job_spawning_status != 'unfinished'):
                # Check if this job is complete by seeing if all child jobs are failed or successful
                print("Attempting to resolve parent job " + str(job_id), flush=True)
                child_jobs = job_tracker.get_child_jobs(job_id)
                job_finished = True
                total_child_job_count = 0
                failed_job_count = 0

                for child_job in child_jobs:
                    child_job_status = child_job['job_management']['job_status']
                    total_child_job_count += 1
                    if child_job_status != 'success' and child_job_status != 'failed':
                        job_finished = False
                    elif child_job_status == 'failed':
                        # TODO: ADD RETRY COUNT BEING AT THE MAX TO THE CONDITIONAL
                        failed_job_count += 1

                # If all child jobs have failed, or failures are greater than a configurable threshold, do fail the parent job
                if child_job_spawning_status == 'failure' or failed_job_count >= _max_child_errors or failed_job_count >= total_child_job_count:
                    print("Found a failed parent job..." + str(job_id), flush=True)
                    job_tracker.set_job_status('failed', job_id)
                    print("Set the parent job's status to failed..." + str(job_id), flush=True)
                    celeryapp.execute.send_task("tasks.tasks.do_task", args=[{'job_id': str(job_id), 'status': 'failed'}], kwargs={}, queue=_failure_queue)
                # if job is finished (and not failed) we mark it as successful
                elif job_finished and total_child_job_count > 0:
                    print("Found a complete parent job..." + str(job_id), flush=True)
                    job_tracker.set_job_status('success', job_id)
                    print("Resolved the completed job..." + str(job_id), flush=True)
                    # We skip the time comparison if we resolve a job
                    celeryapp.execute.send_task("tasks.tasks.do_task", args=[{'job_id': str(job_id), 'status': 'success'}], kwargs={}, queue=_success_queue)
                else:
                    print("Job is not finished...")
            elif (parent_ref is None and child_job_spawning_status == 'unfinished'):
                print("Parent job has not finished spawning children " + str(job_id), flush=True)
            else:
                # Check for stalled child jobs
                print("Checking status of child job " + str(job_id), flush=True)
                try:
                    job_doc_time = job_doc['last_modified_date'].replace(tzinfo=datetime.timezone.utc)
                    diff = current_time - job_doc_time
                    #If it has been more than the expected duration, we assume
                    #that the process has stalled.
                    if diff >= self.progress_check_duration:
                        self.handle_stalled_job(job_doc)
                except Exception as e:
                    # TODO: This doesn't actually print the error, we get "exception: 'event'" in all cases
                    print('exception: {}'.format(e))


    def handle_stalled_job(self, job_doc):
        job_management = job_doc.get("job_management")
        if (job_management is None):
            #TODO what to do here - what does this mean?
            return False
        number_of_tries = job_management["numberOfTries"]
        max_number_of_tries = job_management["maxNumberOfTries"]
        if (number_of_tries < max_number_of_tries):
            #Requeue
            print("Requeued job id" + str(job_doc["_id"]))
            return self.requeue(job_doc, number_of_tries+1)
        #Trigger the undo procedure.
        return self.revert(job_doc)

    def requeue(self, job_doc, trial_number):
        #Update the number of tries in the tracker file
        job_doc["job_management"]["numberOfTries"] = trial_number
        try:
            updated_job_doc = job_tracker.replace_tracker_doc(job_doc)
        except Exception as e:
            #TODO what to do here - what does this mean if the tracker retrievel fails?
            return False
        #Log message
        #Queue the step again
        ticket_id = str(job_doc['_id'])
        # TODO: THIS IS THE WRONG KEY, CREATE REQUEUE MESSAGE HAS NEVER FIRED
        parent_ticket_id = str(job_doc.get('parent_ref', ''))
        if not parent_ticket_id:
            message = mqutils.create_task_manager_queue_message(ticket_id)
        else:
            message = mqutils.create_requeue_message(ticket_id, parent_ticket_id)
        try:
            json_message = json.loads(message)
        except ValueError as e:
            log_error_and_reraise("JSON loading failed in requeue")
        job_name = json_message["event"]
        # TODO: STILL USING OLD ACTIVEMQ METHODS
        mqconn = mqutils.get_mq_connection()
        queue = '/queue/'+job_name
        mqconn.send(queue, message,  headers = {"persistent":"true"})
        return True

    def revert(self, job_doc):
        # TODO: INCORRECT KEY, THIS WILL NOT WORK AS EXPECTED, REVERT CODE HAS NEVER FIRED
        if job_doc.get('parent_ref') is None:
            #Nothing to revert if this is a parent job
            return True
        ticket_id = str(job_doc['_id'])
        # TODO: INCORRECT KEY, THIS WILL NOT WORK AS EXPECTED
        parent_ticket_id = str(job_doc.get('parent_ref', ''))
        message = mqutils.create_revert_message(ticket_id, parent_ticket_id)
        if (message is None):
            #TODO Do something that indicates there are no more tasks to revert
            return True
        try:
            json_message = json.loads(message)
        except ValueError as e:
            log_error_and_reraise("JSON loading failed in revert")


        job_name = json_message["event"]

        # TODO: THIS APPEARS UNFINISHED
