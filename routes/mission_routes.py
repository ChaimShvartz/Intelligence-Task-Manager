from fastapi import APIRouter, HTTPException
from logs.config import logger
from database.agent_db import agent_db
from database.mission_db import mission_db
import utils

router = APIRouter()

@router.post('', status_code=201)
def create_mission(data:utils.MissionModelCreating):
    data = data.model_dump()
    if not (1 <= data['difficulty'] <= 10 and 1 <= data['importance'] <= 10):
        raise HTTPException(400, 'difficulty and importance fields must be in range(1, 10)')
    data['risk_level'] = utils.get_risk_level()
    logger.info('trying to create the mission')
    id = mission_db.create_mission(data)
    logger.info('mission created successfully')
    return {'msg': 'mission created successfull','id': id}

@router.get('')
def get_all_missions():
    missions = mission_db.get_all_missions()
    if not missions:
        logger.warning('query returned successfully but no missions yet')
    else:
        logger.info(f'returned {len(missions)} missions')
    return {'data': missions} 

@router.get('/{id}')
def get_mission_by_id(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, 'Mission not found')
    logger.info('returned a mission')
    return {'data': mission}

@router.put('/{id}/assign/{agent_id}')
def assign_mission(id:int, agent_id:int):
    mission = mission_db.get_by_id(id)
    if not mission:
        raise HTTPException(404, 'Mission not found')
    agent = agent_db.get_by_id(agent_id)
    if not agent:
        raise HTTPException(404, 'Agent not found')
    if mission['status'] != 'NEW':
        raise HTTPException(400, 'Mission not available')
    if not agent['is_active']:
        raise HTTPException(400, 'Agent is not active')
    if not len(mission_db.get_open_missions_by_agent(agent_id)) < 3:
        raise HTTPException(400, 'Agent has reached maximum missions')
    if mission['risk_level'] == 'CRITICAL' and agent['agent_rank'] != 'Commander':
        raise HTTPException(400, 'Only Commander can handle critical missions')
    
    logger.info('tryung assign the mission')
    mission_db.update(id, {'assigned_agent_id': agent_id})
    mission_db.update_mission_status(id, 'ASSIGNED')
    logger.info('mission assigned successfully')
    return {'msg': 'mission assigned successfully'}

@router.put('/{id}/start')
def start_mission(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, 'Mission not found')
    if mission['status'] != 'ASSIGNED':
        raise HTTPException(400, 'Unable to start an unassociated mission')
    mission_db.update_mission_status(id, 'IN_PROGRESS')
    logger.info('mission started successfully')
    return {'msg': 'mission started successfully'}

@router.put('/{id}/complete')
def complete_mission(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, 'Mission not found')
    if mission['status'] != 'IN_PROGRESS':
        raise HTTPException(400, 'Unable to complete a mission that is not in progress')
    mission_db.update_mission_status(id, 'COMPLETED')
    logger.info('mission completed successfully')
    agent_db.increment_completed(mission['assigned_agent_id'])
    return {'msg': 'mission completed successfully'}

@router.put('/{id}/fail')
def fail_mission(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, 'Mission not found')
    if mission['status'] != 'IN_PROGRESS':
        raise HTTPException(400, 'Unable to failed a mission that is not in progress')
    mission_db.update_mission_status(id, 'FAILED')
    logger.info('mission failed successfully')
    agent_db.increment_failed(mission['assigned_agent_id'])
    return {'msg': 'mission failed successfully'}

@router.put('/{id}/cancel')
def cancel_mission(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, 'Mission not found')
    if mission['status'] not in ('NEW', 'ASSIGNED'):
        raise HTTPException(400, 'It is not possible to cancel a mission once it has started')
    mission_db.update_mission_status(id, 'CANCELLED')
    logger.info('mission cancelled successfully')
    return {'msg': 'mission cancelled successfully'}
