import os
from falcon import App
from psycopg_pool import ConnectionPool
from resolvers import Resolver

# properties settings
user = os.getenv("USERNAME")
pwd = os.getenv("PASSWORD")
# build base objects
connection=f"postgresql://{user}:{pwd}@localhost:5432/recueil".format(user=user,pwd=pwd)
pool = ConnectionPool(min_size = 2, max_size = 4, open=False, conninfo=connection)
resolver = Resolver(pool)

# build app
app = App()
app.add_route('/resolve/{value}', resolver)