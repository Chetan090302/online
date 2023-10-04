import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from src.components.mongo_db import MongoDBConnection

if __name__ == '__main__':
    db_conn = MongoDBConnection(username='lokesh',password='lokesh')
    db_conn.connect()
    df = db_conn.read_data_from_mongodb("delivery_time_pred", "dtp_collection",os.path.join('notebooks/data','importedData.csv'))
    logging.info(df)