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
    mission = mission_db.create_mission(data)
    logger.info('mission created successfully')
    return {'msg': 'mission created successfull', 'data': mission}

@router.get('')
def get_all_missions():
    missions = mission_db.get_all_missions()
    if not missions:
        logger.warning('query returned successfully but no missions yet')
    else:
        logger.info(f'returned {len(missions)} missions')
    return {'msg': f'returns all missions', 'data': missions} 

@router.get('/{id}')
def get_mission_by_id(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise utils.MissionNotFoundError
    logger.info('returned a mission')
    return {'msg': 'returns a mission', 'data': mission}

@router.post('/{id}/assign/{agent_id}')
def assign_mission(id:int, agent_id:int):
    mission = mission_db.get_by_id(id)
    if not mission:
        raise utils.MissionNotFoundError
    agent = agent_db.get_by_id(agent_id)
    if not agent:
        raise utils.AgentNotFoundError
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
    updated_mission = mission_db.update_mission_status(id, 'ASSIGNED')
    logger.info('mission assigned successfully')
    return {'msg': 'mission assigned successfully', 'data': updated_mission}

@router.post('/{id}/start')
def start_mission(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise ModuleNotFoundError
    if mission['status'] != 'NEW':
        raise HTTPException(400, )

@router.post('/{id}/complete')
def complete_mission(id:int):
    pass

@router.post('/{id}/fail')
def fail_mission(id:int):
    pass

@router.post('/{id}/cancel')
def cancel_mission(id:int):
    pass


# @router.put('/{id}')
# def update_agent(id:int, data:utils.AgentModelUpdating):
#     data = data.model_dump(exclude_unset=True)
#     if not data:
#         raise HTTPException(400, 'nothing to update')
#     if not agent_db.get_agent_by_id(id):
#         raise utils.AgentNotFoundError
#     logger.info('trying to update the agent')
#     updated_agent = agent_db.update_agent(id, data)
#     if not updated_agent:
#         raise HTTPException(400, 'nothing updated')
#     logger.info('agent updated successfull')
#     return {'msg': 'agent updated successfull', 'data': updated_agent}

# @router.post('/{id}/deactivate')
# def deactivate_agent(id:int):
#     if not agent_db.get_agent_by_id(id):
#         raise utils.AgentNotFoundError
#     logger.info('trying to deactivate the agent')
#     updated_agent = agent_db.update_agent(id, {'is_active': False})
#     if not updated_agent:
#         raise HTTPException(400, 'agent already deactive')
#     logger.info('agent deactivate successfull')
#     return {'msg': 'agent deactivate successfull', 'data': updated_agent}

# @router.get('/{id}/performance')
# def get_agent_performance(id:int):
#     agent = agent_db.get_agent_by_id(id)
#     if not agent:
#         raise utils.AgentNotFoundError
#     logger.info("returns agent's performance")
#     return utils.get_agent_performance(agent, id)