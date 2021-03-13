import psycopg2

class SnakeDAO:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def dbConnection(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="snake",
                user="postgres",
                password="123"
            )

            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection is not None:
                print("Database connection established")

    def dbCloseConnection(self):     
        self.connection.close()
        print("Database connection closed")
