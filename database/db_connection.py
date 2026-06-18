import mysql.connector
from logs.config import logger

class ConnectionDB:
    def __init__(self):
        logger.info('Trying to establish a connection')
        self.connect()

    def get_connection(self):
        if not self.connection.is_connected():
            logger.warning('The connection went wrong, returns a new one')
            self.connect()
        logger.info('Connection established successfully')
        return self.connection
    
    def connect(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                  user='root', password='1234')
        self.create_database()
        
    def create_database(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS Intelligence_db')
            cursor.execute('USE Intelligence_db')

    def create_tables(self):
        self.create_agents_table()
        self.create_missions_table()

    def create_agents_table(self):
        cmd = '''CREATE TABLE IF NOT EXISTS agents(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        specialty VARCHAR(100) NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT true,
        completed_missions INT NOT NULL DEFAULT 0,
        failed_missions INT NOT NULL DEFAULT 0,
        agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
        )
        '''
        with self.get_connection().cursor() as cursor:
            cursor.execute(cmd)

    def create_missions_table(self):
        cmd = '''CREATE TABLE IF NOT EXISTS missions(
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        description TEXT NOT NULL,
        location VARCHAR(100) NOT NULL,
        difficulty INT NOT NULL,
        importance INT NOT NULL,
        status ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS',
          'COMPLETED', 'FAILED', 'CANCELLED') NOT NULL,
        risk_level VARCHAR(10) NOT NULL,
        assigned_agent_id INT DEFAULT NULL
        )
        '''
        with self.get_connection().cursor() as cursor:
            cursor.execute(cmd)

db = ConnectionDB()

