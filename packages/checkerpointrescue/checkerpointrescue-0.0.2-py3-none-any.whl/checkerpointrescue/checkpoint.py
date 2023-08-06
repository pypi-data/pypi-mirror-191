import os
import json
import sqlite3
from dotenv import load_dotenv
import datetime
from pathlib import Path

load_dotenv()

class Checkpoint:
    def __init__(self, storage_medium, file_path=None, db_conn=None, timeout=10):
        """Initialise constructor parameter"""
        self.storage_medium = str.lower(storage_medium)
        self.file_path = file_path
        self.db_conn = db_conn
        self.timeout = timeout
    
    def save_checkpoint_data(self, checkpoint_value):
        """Save the checkpoint data in specified storage medium"""
        if self.storage_medium == 'file':
            self._save_to_file(checkpoint_value)
        elif self.storage_medium == 'database':
            self._save_to_db(checkpoint_value)
        else:
            raise ValueError('Invalid storage medium, It should be either \'file\' or \'database\'.')
    
    def get_last_checkpoint(self):
        """Retrive the checkpoint from specified storage medium"""
        if self.storage_medium == 'file':
            return self._get_from_file()
        elif self.storage_medium == 'database':
            return self._get_from_db()
        else:
            raise ValueError('Storage medium is not specified.')
    
    def _save_to_file(self, checkpoint_value):
        """To save checkpoint data in file storage based on specified extension"""
        assert self.file_path 
        
        file_ext = os.path.splitext(self.file_path)[1]
        if file_ext == '.json':
            with open(self.file_path, 'w') as f:
                json.dump(checkpoint_value, f)
        elif file_ext == '.txt':
            with open(self.file_path, 'w') as f:
                f.write(str(checkpoint_value))
        elif file_ext == '.env':
            with open(self.file_path, 'w') as f:
                f.write(f'CHECKPOINT={checkpoint_value}')
        else:
            raise ValueError('Please specify the file path')
     
    def _get_from_file(self):
        """To retrive checkpoint data from file storage based on file extension"""
        assert self.file_path

        file_ext = os.path.splitext(self.file_path)[1]
        if file_ext == '.json':
            with open(self.file_path, 'r') as f:
                return json.load(f)
        elif file_ext == '.txt':
            with open(self.file_path, 'r') as f:
                return f.read()         
        elif file_ext == '.env':
            with open(self.file_path, 'r') as f:
                dotenv_path = Path(self.file_path)
                load_dotenv(dotenv_path=dotenv_path)
                return os.getenv('CHECKPOINT')
        else:
            raise ValueError('File path is not specified')
    
    def _save_to_db(self, checkpoint_value):
        """To save checkpoint data if storage medium is database"""
        if self.db_conn is None:
            raise Exception("Database connection is not provided")

        try:
            conn = sqlite3.connect(self.db_conn, timeout=self.timeout)
            query = conn.cursor()
            query.execute("CREATE TABLE IF NOT EXISTS checkpoints (timestamp REAL, data TEXT)")
            query.execute("INSERT INTO checkpoints (timestamp, data) VALUES (?, ?)",
                      (datetime.datetime.timestamp(datetime.datetime.now()), str(checkpoint_value)))
            conn.commit()
        except Exception as e:
            raise Exception("Data insertion failed")
        finally:
            conn.close()

    def _get_from_db(self):
        """To load checkpoint data from database"""
        try:
          conn = sqlite3.connect(self.db_conn)
          c = conn.cursor()
          c.execute("SELECT * FROM checkpoints ORDER BY timestamp DESC LIMIT 1")
          result = c.fetchone()
          conn.close()
          if result:
              return result[1]
          else:
              raise Exception("No existing checkpoint")
        except Exception as e:
            raise Exception("Database Connectivity issue")


