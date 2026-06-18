from pydantic import BaseModel
from typing import Literal

class InvalidAgentDetails(Exception):
    pass

class AgentNotFoundError(Exception):
    detail = 'Agent not found'

class MissionNotFoundError(Exception):
    detail = 'Mission not found'

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

class MissionModelCreating(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int
    status: str | None = 'NEW'

def get_risk_level(difficulty:int, importance:int):
    result = difficulty * 2 + importance
    if result < 9:
        level = 'LOW'
    elif result < 17:
        level = 'MEDIUM'
    elif result < 24:
        level = 'HIGH'
    else:
        level = 'CRITICAL'
    return level