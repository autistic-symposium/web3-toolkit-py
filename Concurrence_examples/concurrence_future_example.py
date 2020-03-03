import random
import logging
import concurrent.futures

WORKER_COUNT = 10
JOB_COUNT = 10

class Job:
    def __init__(self, number):
        self.number = number

def process_job(job):
    # Wait between 0 and 0.01 seconds.
    time.sleep(random.random()/100.0)
    logging.info("Job number {:d}".format(job.number))
    
def main():
    with concurrent.futures.ThreadPoolExecutor(
         max_workers=WORKER_COUNT) as executor:
       futures = [executor.submit(process_job, Job(i))
                        for i in range(JOB_COUNT)]
       for future in concurrent.futures.as_completed(futures):
           pass