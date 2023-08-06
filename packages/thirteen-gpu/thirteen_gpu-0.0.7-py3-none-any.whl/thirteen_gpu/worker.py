from collections import defaultdict
import json
from thirteen_gpu.definition import JobStatus
from thirteen_gpu.ssh import SSH
import ast


def get_available_gpus_across_workers(workers):
    
    for worker in workers:
        worker_available_gpus = worker.get_available_gpus()
        
        # 첫번째 available gpu 반환
        if len(worker_available_gpus) > 0:
            return worker_available_gpus[0]
    
    # available gpus 가 모든 workers 에 없으면 빈 리스트 반환
    return []


class Worker(object):
    def __init__(self, ip, port, user, n_gpus):
        self.ip = ip
        self.port = port
        self.user = user
        self.n_gpus = n_gpus
        
        self.ssh = SSH(ip, port, user)
    
        self.max_jobs_per_gpu = 2
            
    def get_available_gpus(self):
        """ job 이 `max_jobs_per_gpu` 개 이하로 사용 중인 gpu 목록 반환한다 """
        
        gpu_usage = {gpu: 0 for gpu in range(self.n_gpus)}
        
        # Running container 목록을 가져오기
        containers = self.ssh.ssh_exec_command(            
            "docker ps --format '{{.Names}}' --filter 'status=running'"
        ).split("\n")
        
        containers = [container for container in containers if container.startswith("job_")]
        
        for container_name in containers:
            
            # container 가 사용 중인 gpu 조회
            out = self.ssh.ssh_exec_command(    
                "docker inspect -f '{{json .HostConfig.DeviceRequests}}'" +  f" {container_name}"
            )
                        
            # 해당 gpu 사용 중인 job 수 증가
            for used_gpu in ast.literal_eval(out.split("\n")[0])[0]["DeviceIDs"]:
                gpu_usage[int(used_gpu)] += 1
    
        # 사용 중인 gpu 제외하고 남은 gpu 반환
        available_gpus = []
        for gpu_id in range(self.n_gpus):
            
            for count in range(self.max_jobs_per_gpu - gpu_usage[gpu_id]):
                available_gpus.append(GPU(self.ip, self.port, self.user, gpu_id))
                
        return available_gpus
    
    def get_running_jobs(self):
        jobs = self.ssh.ssh_exec_command(
            "docker ps --format '{{.Names}}' --filter 'status=running'"
        ).split("\n")
        
        jobs = [job for job in jobs if job.startswith("job_")]                
        return jobs
    
    def update_job_status(self, projects: list):
        """ Worker 안에서 실행되는 모든 프로젝트의 job 들의 상태를 업데이트한다 """
        
        SUCCESSED_CODES = ["Exited (0)"] # TODO: stop 과 success 를 어떻게 구분?
        FAILED_CODES = ["Exited (1)", "Exited (125)", "Exited (126)", "Exited (127)"]
        CRASHED_CODES = ["Exited (137)"]
        
        exited_jobs = self.ssh.ssh_exec_command(            
            "docker ps --format '{{.Names}},{{.Status}}' --filter 'status=exited'"
        ).split("\n")[:-1]
                
        exited_jobs = [(job.split(",")[0], " ".join(job.split(",")[1].split(" ")[:2])) for job in exited_jobs] # [[job_name, status], ...]
        exited_jobs = [job for job in exited_jobs if job[0].startswith("job_")]
                
        # container 의 exit code 에 따라 job 의 상태를 업데이트한다
        for job_name, exit_code in exited_jobs:
            if exit_code in SUCCESSED_CODES:
                for project in projects:
                    if job_name in project.jobs:
                        print(f"[Status Update] job {job_name} finished")
                        project.jobs[job_name].status = JobStatus.SUCCESS
            
            elif exit_code in FAILED_CODES:
                for project in projects:
                    if job_name in project.jobs:
                        print(f"[Status Update] job {job_name} failed")
                        project.jobs[job_name].status = JobStatus.FAILED
            
            elif exit_code in CRASHED_CODES:
                for project in projects:
                    if job_name in project.jobs:
                        print(f"[Status Update] job {job_name} crashed")
                        project.jobs[job_name].status = JobStatus.CRASHED
            
            else:
                for project in projects:
                    if job_name in project.jobs:
                        print(f"[Status Update] job {job_name} unknown")
                        project.jobs[job_name].status = JobStatus.UNKNOWN
                        
        # remove all stopped containers
        job_names = [job[0] for job in exited_jobs]
        self.ssh.ssh_exec_command(
            f"docker rm -f {' '.join(job_names)}"
        )
                
        # write job status to txt file
        with open(f"status.json", "w") as f:
            status = defaultdict(lambda: defaultdict(int))            
            
            for project in projects:
                # initialize status dict (dict of dict of int) 
                status[project.project_name]["user"] = project.user
                status[project.project_name]["submit_at"] = project.submit_at
                status[project.project_name]["status"] = defaultdict(int)
                
                for job in project.jobs.values():
                    status[project.project_name]["status"][job.status.name] += 1
                
                # dump to json file
            json.dump(status, f, indent=4)
                
                
                    
class GPU(object):
    def __init__(self, ip, port, user, gpu_id):
        self.ip = ip
        self.port = port
        self.user = user
        self.gpu_id = gpu_id
