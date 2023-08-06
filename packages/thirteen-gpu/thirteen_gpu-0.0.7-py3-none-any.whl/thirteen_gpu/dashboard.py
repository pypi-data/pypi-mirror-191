import json
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/")
def read_root():
    html = """
    <html>
        <head>
            <title> Thirteen GPU dashboard </title>
        </head>
        <body>
            {}
        </body>
    </html>
    """
    # use join method to concatenate all strings in the list into a single string
    
    
    status = json.load(open("status.json"))
    text = "<a href='http://54.180.160.135:2014/'>GPU Status</a>"
    
    projects = []
    for project_name, project_status in status.items():
        user = project_status["user"]
        submit_at = project_status["submit_at"]
        
        status_info = [(status_name, status_count) for status_name, status_count in project_status["status"].items()]
        
        projects.append((project_name, user, submit_at, status_info))
        
    projects = sorted(projects, key=lambda x: x[2], reverse=True)
    
    for project_name, user, submit_at, status_info in projects:
        text += f"""
            <h2> Project: {project_name} </h2>
        """
        text += f"user: {user} / submitted at: {submit_at} <br>"
        
        for status_name, status_count in status_info:
            text += f" {status_name}: {status_count} "
            
    contents = html.format(text)
    
    # return HTML Rendered Page
    return HTMLResponse(content=contents, status_code=200)