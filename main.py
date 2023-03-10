import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from image.routers import reader, power, point
import uvicorn

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

# app对象
app = FastAPI(docs_url=None, redoc_url=None)

# 静态文件位置
static_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=f"{static_dir}/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8080",
        "http://192.168.31.186:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(reader.app, prefix="/reader", tags=['读取xlsx文件到数据库'])
app.include_router(power.app, prefix="/power", tags=['计算受力并保存到数据库'])
app.include_router(point.app, prefix="/point", tags=['计算坐标并保存到数据库'])

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
