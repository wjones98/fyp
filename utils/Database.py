import pyodbc


class Database:

    @staticmethod
    def connect():
        conn = pyodbc.connect(
                'Driver={ODBC Driver 17 for SQL Server};'
                'Server=(LocalDb)\MSSQLLocalDB;'
                'Database=MetaData;'
                'uid=admin;'
                'pwd=letsusefirebase;')
        return conn

    @staticmethod
    def execute_sproc(sproc, params, cursor):
        query = """
            DECLARE @out nvarchar(max);
            EXEC %s ,@responseMessage = @out OUTPUT;
            SELECT @out AS the_output;         
            """ % sproc
        cursor.execute(query, params)
        return cursor.fetchall()

    @staticmethod
    def execute_query(query, cursor):
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def execute_non_query(query, cursor):
        cursor.execute(query)