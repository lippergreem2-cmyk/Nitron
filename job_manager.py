"""
Nitron Job Manager
"""

import uuid
import time


class JobManager:

    def __init__(self):

        self.jobs = {}

    def create(self, job_type, prompt):

        job_id = str(uuid.uuid4())[:8]

        self.jobs[job_id] = {
            "id": job_id,
            "type": job_type,
            "prompt": prompt,
            "status": "waiting",
            "created": time.time(),
            "result": None
        }

        return job_id

    def start(self, job_id):

        if job_id in self.jobs:
            self.jobs[job_id]["status"] = "running"

    def finish(self, job_id, result):

        if job_id in self.jobs:
            self.jobs[job_id]["status"] = "finished"
            self.jobs[job_id]["result"] = result

    def fail(self, job_id, reason):

        if job_id in self.jobs:
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["result"] = reason

    def get(self, job_id):

        return self.jobs.get(job_id)

    def list(self):

        return list(self.jobs.values())

    def clear(self):

        self.jobs.clear()


jobs = JobManager()
