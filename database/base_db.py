from database.db_connection import db

class BaseDB:
    def __init__(self, table_name):
        self.table_name = table_name

    @property
    def connection(self):
        return db.get_connection()
    
    def get_all(self) -> list[dict]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name}')
            return cursor.fetchall()
        
    def get_by_id(self, id:int) -> dict | None:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = %s', (id,))
            return cursor.fetchone()
        
    def create(self, data:dict) -> int:
        connection = self.connection
        keys = ', '.join(data)
        place_holders = '%s, ' * (len(data) - 1) + '%s'
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO {self.table_name}(
                           {keys})VALUES({place_holders})''', [*data.values()])
            connection.commit()
            return cursor.lastrowid
        
    def update(self, id:int, data:dict) -> bool:
        connection = self.connection
        statements = ', '.join(f'{key} = %s' for key in data)
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE {self.table_name} SET {statements} WHERE id = %s', [*data.values(), id])
            connection.commit()
            return cursor.rowcount > 0
        
    def count(self, condition:str=None, values:tuple=None) -> int:
        condition = condition or ''
        values = values or tuple()
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(f'SELECT COUNT(*) as count FROM {self.table_name} ' + condition, values)
            return cursor.fetchone()['count']