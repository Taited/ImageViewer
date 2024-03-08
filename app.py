import os.path as osp
import math
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import get_file_names, concat_page_data

DIR = '/mnt/tedsun/cafidata/SSDiff_vis'
TOTAL_NUM = 11000#1700
PAGE_LIMIT = 20
TOTAL_PAGE = math.ceil(TOTAL_NUM / PAGE_LIMIT)

app = FastAPI()
# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify the exact domain names, e.g., ["https://your-frontend-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/image/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def pagination(page: int = 1, limit: int = 10, total: int = TOTAL_NUM):
    begin_id = (page - 1) * limit + 1
    if begin_id + limit > total:
        limit = total - begin_id
    return begin_id, limit


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request})

@app.get("/image/", response_class=HTMLResponse)
async def render_home(request: Request):
                    #   current_user: User = Depends(get_current_active_user)):

    project_name = get_file_names(DIR)
    project_list = []
    for name in project_name:
        project_list.append(
            (name, osp.join('/image/show', name, '1'))
        )

    return templates.TemplateResponse(
        "home.html", 
        {"request": request, "project_list": project_list})


@app.get("/image/show/{proj_name}/{page}", response_class=HTMLResponse)
async def render_page(request: Request, proj_name: str, page: int = 1):
    base_dir = osp.join(DIR, proj_name)

    category = get_file_names(base_dir)
    begin_id, valid_limit = pagination(page, limit=PAGE_LIMIT)
    page_data = concat_page_data(proj_name, category, begin_id, valid_limit)
    
    # page navigation
    begin_page = page - 5 if (page - 5) > 0 else 1
    end_page = begin_page + 9 if (begin_page + 9) <= TOTAL_PAGE else TOTAL_PAGE
    page_list = []
    for page_id in range(begin_page, end_page, 1):
        page_list.append(
            (page_id, osp.join('/image/show', proj_name, str(page_id)))
        )
    
    # last and next
    last_page = page - 1 if (page - 1) > 0 else 1 
    next_page = page + 1 if (page + 1) <= TOTAL_PAGE else TOTAL_PAGE
    last_page_url = osp.join('/image/show', proj_name, str(last_page))
    next_page_url = osp.join('/image/show', proj_name, str(next_page))

    return templates.TemplateResponse(
        "page.html", 
        {"request": request, "page_data": page_data,
         "category": category, "page_list": page_list,
         "last_page": last_page_url, "next_page": next_page_url})


@app.get("/image/image_bed/{project}/{category}/{item_name}")
async def download_files_stream(project: str, category: str, item_name: str):
    file_like = osp.join(DIR, project, category, item_name)
    if not osp.exists(file_like):
        item_name = item_name.replace('.png', '.jpg')
        file_like = osp.join(DIR, project, category, item_name)
    return FileResponse(file_like)


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        reload=True,
        port=5001,
        host="0.0.0.0",
        ssl_keyfile="./select.key",
        ssl_certfile="./select.crt"
    )