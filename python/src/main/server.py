import falcon
import json
import logging

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class PythonUDFs():

    def __init__(self):
        self.secret = 'mysecret'
        logging.basicConfig(format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S %z")

        file = None
        try:
            file = open('secret', 'r')
            secret = file.read()
        except:
            logging.error("Did not find secret file...")
        finally:
            if file is not None:
                file.close()

    def get_body(self, udf):
        name = "modules." + udf['module']
        mod = __import__(name)
        return mod.method(*tuple(udf['params']))

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_501  # This is the default status
        resp.body = ('Unsupported operation: GET')

    def on_post(self, req, resp):
        try:
            if not req.client_accepts_json:
                raise falcon.HTTPBadRequest('Client does accept JSON',
                    'A valid Accept header is required.')
            elif not req.content_type == "application/json":
                raise falcon.HTTPBadRequest('Contents are not in JSON',
                    'A valid Content-Type header is required.')
            elif not req.get_header("Secret") == self.secret:
                raise falcon.HTTPBadRequest('Secret does not match',
                    'The correct secret should be present in the header.')


            body = req.stream.read()
            if not body:
                raise falcon.HTTPBadRequest('Empty request body',
                    'A valid JSON document is required.')

            udf = json.loads(body, encoding='utf-8')
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = (self.get_body(udf))
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')



# falcon.API instances are callable WSGI apps
app = falcon.API()

# things will handle all requests to the '/things' URL path
app.add_route('/server', PythonUDFs())