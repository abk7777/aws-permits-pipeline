import os
import logging
import json
import psycopg2
from libs.sql_queries import permits_raw_copy #, titanic_data_copy

DB_ENDPOINT = os.environ['DB_ENDPOINT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def load_data(event, context):

    logger.info(event)
    
    file = event['Records'][0]['s3']['object']['key']
    logger.info(file)

    try:
        logger.info("Attempting connection...")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                                password=DB_PASSWORD, 
                                host=DB_ENDPOINT)
        cur = conn.cursor()
        logger.info(f'Connected to "{DB_NAME}" at "{DB_ENDPOINT}"')
    except Exception as err:
        logger.error(f'Connection Error: "{err}"')
        return -1
        
    logger.info(f'Executing query: "COPY"')
    logger.debug(permits_raw_copy.format(FILE=file))
    # logger.debug(titanic_data_copy.format(FILE=file))
    try:
        # permits data
        cur.execute(permits_raw_copy.format(FILE=file))
        logger.info(f'Query successful')
        logger.debug(permits_raw_copy.format(FILE=file))

        # # titanic data for testing
        # cur.execute(titanic_data_copy.format(FILE=file))
        # logger.info(f'Query successful')
        # logger.debug(titanic_data_copy.format(FILE=file))

        conn.commit()
        cur.close()
        logger.info(f'Closed connection to "{DB_NAME}" at "{DB_ENDPOINT}')
    except Exception as err:
        logger.error(f'Error: "{err}"')
        cur.close()
        logger.info(f'Closed connection to "{DB_NAME}" at "{DB_ENDPOINT}')
        return -1

    return 0


if __name__ == "__main__":
    load_db("", "")