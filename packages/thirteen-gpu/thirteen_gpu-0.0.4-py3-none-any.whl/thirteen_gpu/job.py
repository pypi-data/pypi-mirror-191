

from .definition import JobStatus, WORKSPACE_DIR
from .ssh import SSH
from .worker import GPU, Worker


def get_running_jobs(workers: list):
    running_jobs = []
    
    for worker in workers:
        running_jobs += worker.get_running_jobs()
    
    return running_jobs

class Job(object):
    def __init__(self, project_name, job_name, user, config_path, id=0):
        
        self.status = JobStatus.PENDING
        self.project_name = project_name
        self.job_name = job_name
        self.config_path = config_path # config/runs/xxx.json
        self.user = user
        self.job_id = id
    
    def run(self, worker: Worker, gpu: GPU):
                
        # project code 를 worker 로 복사
        worker.ssh.ssh_copy(
            src=f"{WORKSPACE_DIR}/{self.project_name}",
            dst=f"/home/thirteen/{self.project_name}/"
        )
                
        IMAGE_NAME = "thirteen/neural-quant:latest"
        REMOTE_WORKSPACE_DIR = "/home/thirteen"
        
        # worker 에서 job 을 실행하는 docker container start
        out = worker.ssh.ssh_exec_command(
            f"docker run -itd --gpus '\"device={gpu.gpu_id}\"' " + \
            f"-v {REMOTE_WORKSPACE_DIR}/{self.project_name}:/root/{self.project_name} -v /data:/root/{self.project_name}/data " + \
            f"-w /root/{self.project_name} " + \
            "--shm-size=1T " + \
            f"--name {self.job_name} " + \
            f"-e AWS_ACCESS_KEY_ID=AKIAXCPLIY4KT76BUDF4 -e AWS_SECRET_ACCESS_KEY=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 -e AWS_S3_BUCKET=thirteen-ai " + \
            f"{IMAGE_NAME} " + \
            f"bash -c \"python train.py {self.config_path}\""
        )
        
        print(f"Job {self.job_name} is running on {gpu.ip}:{gpu.port} (gpu: {gpu.gpu_id})")
    
        self.status = JobStatus.RUNNING
        
        self.worker = worker
            
    def stop(self, ):
        self.worker.ssh.ssh_exec_command(
            f"docker stop {self.job_name}"
        )
        
        self.status = JobStatus.STOPPED
    
