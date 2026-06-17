from database.base_db import BaseDB

class AgentDB(BaseDB):
    def __init__(self):
        super().__init__('agents')

    def get_all_agents(self):
        return self.get_all()
    
    def get_agent_by_id(self, id:int):
        return self.get_by_id(id)
        
    def create_agent(self, data):
        agent_id = self.create(data)
        return self.get_by_id(agent_id)
    
    def update_agent(self, id:int, data:dict):
        updated = self.update(id, data)
        msg = 'agent updated successfully' if updated else 'nothing updated'
        return {'msg': msg}
    
    def deactivate_agent(self, id:int):
        updated = self.update(id, {'is_active': False})
        msg = 'agent disabled successfully' if updated else 'nothing updated'
        return {'msg': msg}
    
    def increment_completed(self, id:int):
        updated = self.update(id, {'completed_missions': 'completed_missions + 1'})
        msg = 'The number of tasks has been updated successfully' if updated else 'nothing updated'
        return {'msg': msg}
    
    def increment_failed(self, id:int):
        updated = self.update(id, {'failed_missions': 'failed_missions + 1'})
        msg = 'The number of missions has been updated successfully' if updated else 'nothing updated'
        return {'msg': msg}
    
    def get_agent_performance(self, id:int):
        agent = self.get_by_id(id)
        completed = agent['completed_missions']
        failed = agent['failed_missions']
        total = completed + failed
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'success_rate': completed / total * 100
        }
    
    def count_active_agents(self):
        return self.count('WHERE is_active = true')
    
if __name__ == '__main__':
    pass