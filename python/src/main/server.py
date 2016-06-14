import falcon
import json


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class PythonUDFs(object):
    def getBody(self, udf):
        name = "modules." + udf['method']
        mod = __import__(name)
        return mod.post(*tuple(udf['params']))

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_501  # This is the default status
        resp.body = ('Unsupported operation: GET')

    def on_post(self, req, resp):


        try:
            body = req.stream.read()
            if not body:
                raise falcon.HTTPBadRequest('Empty request body',
                                            'A valid JSON document is required.')

            udf = json.loads(body, encoding='utf-8')
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = (self.getBody(udf))
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')


# falcon.API instances are callable WSGI apps
app = falcon.API()

# things will handle all requests to the '/things' URL path
app.add_route('/server', PythonUDFs())