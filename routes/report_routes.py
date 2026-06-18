from fastapi import APIRouter, HTTPException
from database.agent_db import agent_db
from database.mission_db import mission_db

router = APIRouter()

@router.get('/summary')
def get_summary():
    return {
        'data': {
            "active_agents_count": agent_db.count_active_agents(),
            "total_missions": mission_db.count_all_missions(),
            "open_missions": mission_db.count_open_missions(),
            "completed_missions": mission_db.count_by_status('COMPLETED'),
            "failed_missions": mission_db.count_by_status('FAILED'),
            "cancelled_missions": mission_db.count_by_status('CANCELLED')
            }
        }

@router.get('/missions-by-status')
def get_missions_by_status():
    statuses = ('new', 'assigned', 'in_progress', 'completed', 'failed', 'cancelled')
    return {'data': {f'{status}_missions': mission_db.count_by_status(status.upper()) for status in statuses}}

@router.get('/top-agent')
def get_top_agent():
    top_agent = mission_db.get_top_agent()
    if not top_agent:
        raise HTTPException('No top agent')
    return {'data': top_agent}
