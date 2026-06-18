from database.base_db import BaseDB
# from utils import InvalidAgentDetails

class AgentDB(BaseDB):
    def __init__(self):
        super().__init__('agents')

    def get_all_agents(self):
        return self.get_all()
    
    def get_agent_by_id(self, id:int):
        return self.get_by_id(id)
        
    def create_agent(self, data):
        return self.create(data)
    
    def update_agent(self, id:int, data:dict):
        return self.update(id, data)
        
    # The following function is not used, I left it in light of the test requirements
    def deactivate_agent(self, id:int):  
        updated = self.update(id, {'is_active': False})
        msg = 'agent disabled successfully' if updated else 'nothing updated'
        return msg
    
    def increment_completed(self, id:int):
        connection = self.connection
        with connection.cursor() as cursor:
            cursor.execute('UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s', (id,))
            connection.commit()
            return cursor.rowcount > 0
    
    def increment_failed(self, id:int):
        connection = self.connection
        with connection.cursor() as cursor:
            cursor.execute('UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s', (id,))
            connection.commit()
            return cursor.rowcount > 0
    
    # The following function is not used, I left it in light of the test requirements
    def get_agent_performance(self, id:int):
        agent = self.get_by_id(id)
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
    
    def count_active_agents(self):
        return self.count('WHERE is_active = true')
    
    
agent_db = AgentDB()