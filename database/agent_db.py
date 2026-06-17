from database.base_db import BaseDB
from utils import InvalidAgentDetails

class AgentDB(BaseDB):
    def __init__(self):
        super().__init__('agents')

    def get_all_agents(self):
        return self.get_all()
    
    def get_agent_by_id(self, id:int):
        return self.get_by_id(id)
        
    def create_agent(self, data):
        try:
            if data['agent_rank'] not in ('Junior', 'Senior', 'Commander'):
                raise InvalidAgentDetails('Rank mast be one from: Junior / Senior / Commander')
        except KeyError:
            raise InvalidAgentDetails('Missing the rank key')
        agent_id = self.create(data)
        return self.get_by_id(agent_id)
    
    def update_agent(self, id:int, data:dict):
        if 'id' in data:
            raise InvalidAgentDetails('Unable to update ID')
        updated = self.update(id, data)
        msg = 'agent updated successfully' if updated else 'nothing updated'
        return msg
    
    def deactivate_agent(self, id:int):
        updated = self.update(id, {'is_active': False})
        msg = 'agent disabled successfully' if updated else 'nothing updated'
        return msg
    
    def increment_completed(self, id:int):
        connection = self.connection
        with connection.cursor() as cursor:
            cursor.execute('UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s', (id,))
            connection.commit()
            updated = cursor.rowcount > 0
        msg = 'The number of missions has been updated successfully' if updated else 'nothing updated'
        return msg
    
    def increment_failed(self, id:int):
        connection = self.connection
        with connection.cursor() as cursor:
            cursor.execute('UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s', (id,))
            connection.commit()
            updated = cursor.rowcount > 0
        msg = 'The number of missions has been updated successfully' if updated else 'nothing updated'
        return msg
    
    def get_agent_performance(self, id:int):
        agent = self.get_by_id(id)
        completed = agent['completed_missions']
        failed = agent['failed_missions']
        total = completed + failed
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'success_rate': f'{round(completed / total * 100, 2)} %'
        }
    
    def count_active_agents(self):
        return self.count('WHERE is_active = true')
    