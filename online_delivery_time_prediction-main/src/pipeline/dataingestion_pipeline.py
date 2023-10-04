import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from src.components.mongo_db import MongoDBConnection

if __name__=='__main__':
    db_conn = MongoDBConnection(username='lokesh',password='lokesh')
    db_conn.connect()
    db_database=db_conn.create_database('delivery_time_pred')
    db_collection = db_conn.create_collection(db = db_database,collection_name='dtp_collection')
    db_conn.insert_csv_data(collection=db_collection,csv_path=os.path.join('notebooks/data','newly_createdData.csv'))
