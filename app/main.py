import os
from falcon import App
from psycopg_pool import ConnectionPool
from atexit import register
from resolvers import Resolver

# properties settings
user = os.getenv("USERNAME")
pwd = os.getenv("PASSWORD")
# build base objects
connection=f"postgresql://{user}:{pwd}@localhost:5432/recueil".format(user=user,pwd=pwd)
pool = ConnectionPool(min_size = 2, max_size = 4, open=False, conninfo=connection)
register(pool.close)

# build core objects

class Echo:

    def on_get(self, req, resp):
        resp.media = "ping"


# build app
app = App()
app.add_route('/echo/', Echo())

#app.add_route('/resolve/{value}/', )
#app.add_route('/resolve/tag/{tag}/value/{value}/', )
#app.add_route('/add/value/{value}/as/{tag}', )
#app.add_route('/link/child/{child}/to/parent/{parent}/', )
