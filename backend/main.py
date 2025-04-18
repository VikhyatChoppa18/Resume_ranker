from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from reader import process_resumes
from celery  import AsyncResult
from celery_worker import celery_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

@app.post("/rank")
async def resume_ranker(files: List[UploadFile] = File(...), job_description: str = ""):
    return process_resumes(files, job_description)


@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"status": result.status, "result": result.result}