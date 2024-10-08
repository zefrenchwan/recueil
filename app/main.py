import os
import sys
from falcon import App
from psycopg_pool import ConnectionPool
from processors import *
from bootstrapper import Bootstrapper
from dao import Dao
from atexit import register
import logging 
import traceback

# logging
logging.basicConfig(format='%(levelname)s %(asctime)s \t %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('recueil')
logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler('logs/recueil.log')
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# properties settings
db_url = os.getenv("DB_URL")
# build base objects
pool = ConnectionPool(min_size = 1, max_size = 4, open=True, conninfo=db_url)
register(pool.close)
dao = Dao(pool, logger)
logger.info("database pool is up and running")

# build core objects
tag_solver = TagSolver(dao, logger)
unbouded_solver = UnboundedSolver(dao, logger)
values_appender = ValuesAppender(dao, logger)
tags_linker = TagsLinker(dao, logger)

#bootstrap app data
logger.info("Loading base data")
loader = Bootstrapper(dao, logger)
try:
    loader.load("/storage/bootstrap/")
except Exception as e: 
    logger.fatal("loading failed")
    logger.fatal(str(e))
    logger.fatal(traceback.format_exc())
    sys.exit(3)       


# build app
app = App()
logger.info("Starting routes")
app.add_route('/check/value/{value}/', unbouded_solver)
app.add_route('/check/value/{value}/as/{tag}/', tag_solver)
app.add_route('/add/value/{value}/as/{tag}/', values_appender)
app.add_route('/link/child/{child}/to/parent/{parent}/', tags_linker)
logger.info("Server is up")