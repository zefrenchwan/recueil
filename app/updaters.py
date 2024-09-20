import json 
import falcon 


class ValuesAppender:

    def __init__(self, pool):
        self.pool = pool

    def on_post(self, req, resp, value, tag):
        doc = '{}'
        if req.content_length:
            doc = json.load(req.stream)
        with self.pool.connection() as conn:
            payload = json.dumps(doc)
            with conn.cursor() as cursor:
                cursor.execute('call entities.insert_value(%s, %s, %s);', (value, payload, tag))
            conn.commit()
        resp.status = falcon.HTTP_200 
                