from pydantic import BaseModel
from typing import Literal

class InvalidAgentDetails(Exception):
    pass

class AgentNotFoundError(Exception):
    detail = 'agent not found'

class MissionNotFoundError(Exception):
    detail = 'mission not found'

class AgentModelCreating(BaseModel):
    name: str
    specialty: str
    is_active: bool = True
    completed_missions: int = 0
    failed_missions: int = 0
    agent_rank: str

class AgentModelUpdating(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    completed_missions: int | None = None
    failed_missions: int | None = None
    agent_rank: str | None = None

def get_agent_performance(agent:dict, id:int):
    completed = agent['completed_missions']
    failed = agent['failed_missions']
    total = completed + failed
    try:
        success_rate = round(completed / total * 100, 2)
    except ZeroDivisionError:
        success_rate = 0
    return {
        'total': total,
        'completed': completed,
        'failed': failed,
        'success_rate': f'{success_rate} %'
    }