import os
import os.path as osp

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import get_file_names, concat_page_data


DIR = '/mnt/tedsun/cafidata/SSDiff_vis'

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def render_home(request: Request, proj_name: str):
    base_dir = osp.join(DIR, proj_name)

    project_list = get_file_names(base_dir)

    return templates.TemplateResponse(
        "home.html", 
        {"request": request, "project_list": project_list})


@app.get("/show/{proj_name}", response_class=HTMLResponse)
async def render_page(request: Request, proj_name: str):
    base_dir = osp.join(DIR, proj_name)

    category = get_file_names(base_dir)
    
    page_data = concat_page_data(proj_name, category, 1, 10)

    return templates.TemplateResponse(
        "page.html", 
        {"request": request, "page_data": page_data,
         "category": category})


@app.get("/image_bed/{project}/{category}/{item_name}")
async def download_files_stream(project: str, category: str, item_name: str):
    file_like = osp.join(DIR, project, category, item_name)
    return FileResponse(file_like)


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        reload=True,
        port=5010,
        host="localhost",
        ssl_keyfile="./key.pem",
        ssl_certfile="./cacert.pem"
    )