from database.base_db import BaseDB
from database.agent_db import agent_db
# from utils import AgentNotFoundError, MissionNotFoundError

class MissionsDB(BaseDB):
    def __init__(self):
        super().__init__('missions')

    def create_mission(self, data:dict):
        id = self.create(data)
        return id

    def get_all_missions(self):
        return self.get_all()

    def get_mission_by_id(self, id):
        return self.get_by_id(id)

    def assign_mission(self, m_id:int, a_id:int):
        self.update(m_id, {'assigned_agent_id': a_id})
        return self.update_mission_status(m_id, 'ASSIGNED')
        
    def update_mission_status(self, id:int, status:str):      
        return self.update(id, {'status': status})

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
        
    def count_missions_by_agent(self, id:int):
        return self.count("SELETC count(*) FROM missions WHERE assigned_agent_id = %s", (id,))

    # The following function is not used, I left it in light of the test requirements
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
