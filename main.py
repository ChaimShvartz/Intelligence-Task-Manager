from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database.db_connection import ConnectionDB
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as reports_router
from logs.config import logger

@asynccontextmanager
async def lifespan(app:FastAPI):
    # create database and tables happend in init
    logger.info('Loading up the server')
    yield
    ConnectionDB().get_connection().close()
    logger.info('Shutting down the server')

app = FastAPI(lifespan=lifespan)

app.include_router(agent_router, prefix='/agents', tags=['AGENTS'])
app.include_router(mission_router, prefix='/missions', tags=['MISSIONS'])
app.include_router(reports_router, prefix='/reports', tags=['REPORTS'])

@app.middleware('HTTP')
def middleware(req:Request, next):
    logger.info(f'{req.url.path} - {req.method}')
    return next(req)

@app.exception_handler(HTTPException)
def not_found_handler(req:Request, e:HTTPException):
    logger.warning(e.detail)
    return JSONResponse(e.detail, e.status_code)