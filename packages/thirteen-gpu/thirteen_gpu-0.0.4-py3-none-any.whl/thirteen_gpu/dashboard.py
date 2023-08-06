import json
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    status = json.load(open("status.json"))
    return status    