# Intelligence-Task-Manager

## System description
The purpose of the system is to manage tasks and agents.   
The system includes a connection to MYSQL, creating tables and OOP classes for data management
The system is written in Python and uses SQL as the database

## Folder structure
intelligence-task-manager/   

    ├── database/
    │   ├── db_connection.py
    │   ├── agent_db.py
    │   └── mission_db.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## Table structure

### Agents
| FIELD | TYPE | Notes |\
id | INT AUTO_INCREMENT PK	| Unique identifier\
name | VARCHAR | agent's name\
specialty |	VARCHAR | Field of specialization\
is_active |	BOOLEAN | default: TRUE\
completed_missions | INT | default: 0\
failed_missions | INT | default: 0\
agent_rank | ENUM / VARCHAR | Junior / Senior / Commander ONLY

### Missions
FIELD | TYPE | Notes |\
id | INT AUTO_INCREMENT PK | unique ID\
title | VARCHAR(50) | mission's title\
description | TEXT | Detailed description\
location | VARCHAR(100) | location\
difficulty | INT | 1 - 10 only\
importance | INT | 1 - 10 only\
status | VARCHAR | default: NEW\
risk_level | VARCHAR | Automatically calculated 
— does not come from the user
assigned_agent_id | INT	| NULL until assigned

## Explanation of the departments

### DBConnection
Used to connect the program to the database.\
Its methods: \
    get_connection() - returns an active connection to MySQL\
    create_database() - creates Intelligence_db if it does not exist\
    create_tables() - creates both tables if they do not exist

### AgentDB
Responsible for all SQL operations against the agents table.\
Its method:\
    create_agent(data) - creates a new agent and returns the agent's dict\
    get_all_agents() - returns a list of all agents\
    get_agent_by_id(id) - returns one agent by ID, or None\
    update_agent(id, data) - UPDATE the row (id cannot be changed)\
    deactivate_agent(id) - sets the agent to inactive\
    increment_completed(id) - updates the number of completed tasks\
    increment_failed(id) - updates the number of failed tasks\
    get_agent_performance(id) - returns a dictionary with these keys completed, failed, total, success_rate\
    count_active_agents() - returns the number of active agents

### MissionDB
Responsible for all SQL operations against the missions table.\
Its method:\
    create_mission(data) - Creates a new mission and returns the entire dict\
    get_all_missions() - returns all missions\
    get_mission_by_id(id) - returns a single mission by ID, or None\
    assign_mission(m_id, a_id) - assigns a mission to an agent\
    update_mission_status(id, status) - is used for any status change\
    get_open_missions_by_agent(id) - returns ASSIGNED/IN_PROGRESS missions of an agent\
    count_all_missions() - total missions\
    count_by_status(status) - counts by a specific status\
    count_open_missions() - counts open missions\
    count_critical_missions() - counts CRITICAL missions\
    get_top_agent() - the agent with the highest completed_missions

## System rules
-  rank must be Junior / Senior / Commander — any other value throws an error.
- difficulty and importance must be between 1 and 10 — otherwise an error.
- risk_level is calculated automatically when creating a task — the user does not submit it.
- An agent with is_active=False cannot accept tasks.
- An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
- If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
- Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
- Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
- Only a task with the status IN_PROGRESS can be finished and changed to failed or completed.
- Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error.

## Running instructions
Make sure you don't have another MySQL container running so there is no port conflict.\
Then run the following command in the terminal:

docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
