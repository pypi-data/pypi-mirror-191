from glob import glob
import itertools
import json
import os
from time import sleep
from .definition import JobStatus, WORKSPACE_DIR

from .worker import Worker, GPU
from .project import Project
from .job import Job


def main():
            
    # workers 정보 가져오기
    workers_info = json.load(open('workers.json'))
    workers = [Worker(**worker_info) for worker_info in workers_info.values()]
    
    projects = []
    
    while True:
        
        sleep(10)
        
        # 유저가 제출한 프로젝트 목록 가져오기 (시간 순 정렬)
        # `project_path` = /path/to/workspace/username_projectname
        new_projects = [
            Project(project_path=project_path, user=project_path.split("_")[0]) 
            for project_path in glob(f"{WORKSPACE_DIR}/*")
        ]
        
        # 추가된 project
        for new_project in new_projects:
            if new_project.project_name not in [project.project_name for project in projects]:
                projects.append(new_project)
                
                # 추가되는 project 의 job 이 이전에 실행되었던 job 이면, 해당 stopped container 를 삭제
                stopped_jobs = " ".join([job.job_name for job in new_project.jobs.values()])
                for worker in workers:                    
                    worker.ssh.ssh_exec_command(f"docker rm -f {stopped_jobs}")
                                        
        # 메모리로 관리하는 projects 가 있는데, 디스크에는 없으면 삭제된 것으로 간주함
        deleted_projects = []
        for project in projects:   
            if project.project_name not in [new_project.project_name for new_project in new_projects]:
                deleted_projects.append(project)
                
                projects.remove(project)
                
        deleted_jobs = [job.job_name for project in deleted_projects for job in project.jobs.values()]
            
        print(f"projects: {[project.project_name for project in projects]}")

        if len(deleted_projects) > 0:
            
            # worker 마다 deleted job 에 해당하는 container 중지
            for worker in workers:
                                    
                # running jobs 목록 가져오기
                running_jobs_name = worker.get_running_jobs()

                # Running 중인 Job 인데, deleted project 목록에 있으면 stop
                stopping_jobs = []
                for job_name in running_jobs_name:
                    if job_name in deleted_jobs:
                        stopping_jobs.append(job_name)                                

                if len(stopping_jobs) > 0:
                    print(f"{worker.ip} 에서 중지할 job: {stopping_jobs}")
                    worker.ssh.ssh_exec_command(
                        command=f"docker stop {' '.join(stopping_jobs)} && docker rm {' '.join(stopping_jobs)}"
                    )
        
        # projects 를 job 단위로 분리
        jobs = [job for project in projects for job in project.jobs.values() if job.status == JobStatus.PENDING]
                                                                        
        # 사용 가능한 GPU 를 가져오고, Waiting 상태인 최상단 job 을 실행
        available_gpus = []
        for worker in workers:
            for gpu in worker.get_available_gpus():
                available_gpus.append((worker, gpu))                    
        
        if len(jobs) > 0 and len(available_gpus) > 0:            
            for job, (worker, gpu) in zip(jobs, available_gpus):                                
                job.run(worker, gpu)
            
        else:            
            if len(jobs) == 0:
                print("No pending job")
                
            if len(available_gpus) == 0:
                print("No available GPU")
        
        # Job status 업데이트
        for worker in workers:
            worker.update_job_status(projects=projects)
                    
        # 특정 Project 의 모든 Job 이 끝난 상태면, Project 삭제        
        projects_done = []
        for project in projects:
            if all([
                job.status in (JobStatus.SUCCESS, JobStatus.FAILED, JobStatus.CRASHED, JobStatus.STOPPED, JobStatus.UNKNOWN) 
                for job in project.jobs.values()]
            ):
                print(f"Delete project {project.project_name}")
                project.delete()
                
                projects_done.append(project)
        
        for project in projects_done:
            projects.remove(project)
        
        print('-' * 80)
                                                
if __name__ == '__main__':
    main()
