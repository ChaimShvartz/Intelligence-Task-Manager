from database.base_db import BaseDB
from database.agent_db import agent_db
from utils import AgentNotFoundError, MissionNotFoundError

class MissionsDB(BaseDB):
    def __init__(self):
        super().__init__('missions')

    def create_mission(self, data:dict):
        id = self.create(data)
        return self.get_by_id(id)

    def get_all_missions(self):
        return self.get_all()

    def get_mission_by_id(self, id):
        return self.get_by_id(id)

    def assign_mission(self, m_id:int, a_id:int):
        agent = agent_db.get_by_id(a_id)
        if not agent:
            raise AgentNotFoundError
        mission = self.get_by_id(m_id)
        if not mission:
            raise MissionNotFoundError
        
        if not agent['is_active']:
            raise ValueError('Inactive agent')
        if len(self.get_open_missions_by_agent(a_id)) >= 3:
            raise ValueError('An agent cannot have more than 3 open missions at the same time')
        if mission['risk_level'] == 'CRITICAL' and agent['agent_rank'] != 'Commander':
            raise ValueError('Only a commander-ranked agent can receive critical missions')
        if mission['status'] != 'NEW':
            raise ValueError('It is not possible to assign a mission whose status is not NEW')
        self.update(m_id, {'assigned_agent_id': a_id})
        return self.update_mission_status(m_id, 'ASSIGNED')
        
    def update_mission_status(self, id:int, status:str):
        mission = self.get_by_id(id)
        if not mission:
            raise MissionNotFoundError
        if status not in ('ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED'):
            raise ValueError('invalid status')
        
        last_status = mission['status']
        print((last_status))

        if status == 'ASSIGNED' and last_status != 'NEW':
            raise ValueError('Unable to assign a non-new mission')
        if status == 'IN_PROGRESS' and last_status != 'ASSIGNED':
            raise ValueError('Unable to start an unassociated mission')
        if status in ('COMPLETED', 'FAILED') and last_status != 'IN_PROGRESS':
            raise ValueError('Unable to complete a mission that is not in progress')
        if status == 'CANCELLED' and last_status not in ('NEW', 'ASSIGNED'):
            raise ValueError('It is not possible to cancel a mission once it has started.')
        self.update(id, {'status': status})
        return 'mission updated successfully'

    def get_open_missions_by_agent(self, id:int):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELETC * FROM missions WHERE assigned_agent_id = %s AND status IN ('ASSIGNED', 'IN_PROGRESS'", (id,))
            return cursor.fetchall()

    def count_all_missions(self):
        return self.count()

    def count_by_status(self, status:str):
        return self.count('WHERE status = %s', (status,))

    def count_open_missions(self):
        return self.count("WHERE status IN ('ASSIGNED', 'IN_PROGRESS')")

    def count_critical_missions(self):
        return self.count('WHERE risk_level = %s', ('CRITICAL',))

    def get_top_agent(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1')
            return cursor.fetchone()
        
    @staticmethod
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
        return {'risk_level': level}
    
mission_db = MissionsDB()
