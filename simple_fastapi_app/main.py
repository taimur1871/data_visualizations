#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Library imports
from typing import List
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# import chart and stats
import shutil, os
from pathlib import Path

# Create app and model objects
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")
templates = Jinja2Templates(directory="templates/")


# Welcome page
@app.get("/", response_class=HTMLResponse)
async def read_root(request:Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# function to save uploaded files
def save_uploaded_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

# main function for cutter processing
@app.post("/uploadfiles/")
async def create_upload_files(request:Request, files: List[UploadFile] = File(...)):
    
    # specify upload folder
    temp_folder = './upload'

    for file in files:
        fn = file.filename
        print(fn)
        p = Path(temp_folder +'/'+ fn)
        save_uploaded_file(file, p)
    
    file_list = os.listdir(temp_folder)

    return templates.TemplateResponse("index.html", {"request":request, "file_list":file_list,
                                    "SN":fn})