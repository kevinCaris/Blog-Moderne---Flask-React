from Config.db import query_db


class Model:
    
    
    @staticmethod
    def get(table, criteria=None, one=False):
        
        query = f'SELECT * FROM {table}'
        args = ()

        if criteria:
            where_clause = ' AND '.join([f"{key} = ?" for key in criteria.keys()])
            query = f"{query} WHERE {where_clause}"
            args = tuple(criteria.values())

        return query_db(query, args, fetch=True, one=one)

    @staticmethod
    def create(table, data):
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.values()])
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return query_db(query, values)
        
        
    @staticmethod
    def update(table, record_id, data):
        
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (record_id,) 

        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        query_db(query, values)
        return True


    @staticmethod
    def delete(table, record_id):
        
        query = f"DELETE FROM {table} WHERE id = ?"
        query_db(query, (record_id,))
        return True

        
        