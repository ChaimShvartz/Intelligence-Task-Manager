from database.db_connection import db
# from database.agent_db import agent_db
from database.mission_db import mission_db

db.create_database()
db.create_tables()

print(mission_db.create_mission({'title': 'titl', 'location':'banj', 'importance':5, 'difficulty': 7, 'description': 'edrfghj'}))
# print(mission_db.get_all_missions())
# print(mission_db.get_mission_by_id(3))
# print(mission_db.update_mission_status(3, 'CANCELLED'))

# print(mission_db.count_all_missions())
# print(mission_db.count_by_status('NEW'))
# print(mission_db.count_open_missions())
# print(mission_db.count_critical_missions())
# print(mission_db.get_top_agent())