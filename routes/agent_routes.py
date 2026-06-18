from fastapi import APIRouter, HTTPException
from logs.config import logger
from database.agent_db import agent_db
import utils

router = APIRouter()

@router.post('', status_code=201)
def create_agent(data:utils.AgentModelCreating):
    data = data.model_dump()
    if data['agent_rank'] not in ('Junior', 'Senior', 'Commander'):
        raise HTTPException(400, 'Rank mast be one from: Junior / Senior / Commander')
    logger.info('trying to create the agent')
    agent = agent_db.create_agent(data)
    logger.info('agent created successfully')
    return {'msg': 'agent created successfull', 'data': agent}

@router.get('')
def get_all_agents():
    agents = agent_db.get_all_agents()
    if not agents:
        logger.warning('query returned successfully but no agents yet')
    else:
        logger.info(f'returned {len(agents)} agents')
    return {'msg': f'returns all agents', 'data': agents} 

@router.get('/{id}')
def get_agent_by_id(id:int):
    agent = agent_db.get_agent_by_id(id)
    if not agent:
        raise utils.AgentNotFoundError
    logger.info('returned an agent')
    return {'msg': 'returns an agent', 'data': agent}

@router.put('/{id}')
def update_agent(id:int, data:utils.AgentModelUpdating):
    data = data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, 'nothing to update')
    if not agent_db.get_agent_by_id(id):
        raise utils.AgentNotFoundError
    logger.info('trying to update the agent')
    updated_agent = agent_db.update_agent(id, data)
    if not updated_agent:
        raise HTTPException(400, 'nothing updated')
    logger.info('agent updated successfull')
    return {'msg': 'agent updated successfull', 'data': updated_agent}

@router.post('/{id}/deactivate')
def deactivate_agent(id:int):
    if not agent_db.get_agent_by_id(id):
        raise utils.AgentNotFoundError
    logger.info('trying to deactivate the agent')
    updated_agent = agent_db.update_agent(id, {'is_active': False})
    if not updated_agent:
        raise HTTPException(400, 'agent already deactive')
    logger.info('agent deactivate successfull')
    return {'msg': 'agent deactivate successfull', 'data': updated_agent}

@router.get('/{id}/performance')
def get_agent_performance(id:int):
    agent = agent_db.get_agent_by_id(id)
    if not agent:
        raise utils.AgentNotFoundError
    logger.info("returns agent's performance")
    return utils.get_agent_performance(agent, id)