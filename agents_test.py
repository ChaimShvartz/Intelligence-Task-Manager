from database.db_connection import db
from database.agent_db import agent_db

db.create_database()
db.create_tables()


# print(agent_db.get_all_agents())
# print(agent_db.get_agent_by_id(2))
print(agent_db.create_agent({'name': 'Chaim', 'specialty': 'many'} ))
# print(agent_db.update_agent(10, {'l':2, 'name': 'Chaim', 'specialty': 'many', 'agent_rank': 'Commander'} ))
# print(agent_db.deactivate_agent(2))
# print(agent_db.increment_completed(2))
# print(agent_db.increment_failed(2))
# print(agent_db.get_all_agents())
# print(agent_db.get_agent_performance(2))
# print(agent_db.count_active_agents())