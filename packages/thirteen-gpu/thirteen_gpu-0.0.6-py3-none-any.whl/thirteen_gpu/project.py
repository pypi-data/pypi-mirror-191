from glob import glob
import json
import os

from thirteen_gpu.definition import JobStatus
from thirteen_gpu.job import Job
from datetime import datetime


class Project(object):
    def __init__(self, project_path, user, submit_at):
        
        self.path = project_path
        self.project_name = os.path.basename(project_path)
        self.user = user
        
        # assign current time 
        self.submit_at = submit_at               
                
        # job 목록 초기화
        self.jobs = {}
        
        for i, config_path in enumerate(glob(f"{self.path}/config/runs/*.json")):
            config = json.load(open(config_path))
            
            job_name = f"job_{self.project_name}_{i}"
            
            self.jobs[job_name] = Job(self.project_name, job_name, self.user, "/".join(config_path.split("/")[-3:]), id=i)
    
    def delete(self):
        print(f"Delete project {self.project_name}...")
        os.system(f"rm -rf {self.path}")
