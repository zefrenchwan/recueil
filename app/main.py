import os
from falcon import App
from psycopg_pool import ConnectionPool
from resolvers import TagSolver
from atexit import register
import logging 

# logging
logger = logging.getLogger('recueil')
logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler('logs/recueil.log')
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# properties settings
db_url = os.getenv("DB_URL")
# build base objects
pool = ConnectionPool(min_size = 2, max_size = 4, open=True, conninfo=db_url)
register(pool.close)

# build core objects
tagSolver = TagSolver(pool)

# build app
app = App()
#app.add_route('/check/{value}/', )
app.add_route('/check/value/{value}/as/{tag}/', tagSolver)
#app.add_route('/add/value/{value}/as/{tag}/', )
#app.add_route('/link/child/{child}/to/parent/{parent}/', )
