from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import utils
from routes.agent_routes import router as agent_router
from logs.config import logger

app = FastAPI()
app.include_router(agent_router, prefix='/agents', tags=['AGENTS'])

@app.exception_handler((utils.AgentNotFoundError))
def not_found_handler(req:Request, e: utils.AgentNotFoundError):
    logger.warning(e.detail)
    return JSONResponse(e.detail, 404)

@app.exception_handler(HTTPException)
def not_found_handler(req:Request, e:HTTPException):
    logger.warning(e.detail)
    return JSONResponse(e.detail, e.status_code)