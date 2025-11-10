import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn_params = {
            'dbname': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'devangkankaria'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            if not self.conn or self.conn.closed:
                self.connect()

            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Query execution error: {e}")
            return None

    def execute_update(self, query, params=None):
        """Execute an INSERT/UPDATE/DELETE query"""
        try:
            if not self.conn or self.conn.closed:
                self.connect()

            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Update execution error: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

# Global database instance
db = Database()
