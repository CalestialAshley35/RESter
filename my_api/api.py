import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

class APIRequestHandler(BaseHTTPRequestHandler):
    routes = []
    
    def do_GET(self):
        self._handle_request('GET')
        
    def do_POST(self):
        self._handle_request('POST')
    
    def do_PUT(self):
        self._handle_request('PUT')

    def do_DELETE(self):
        self._handle_request('DELETE')
    
    def _handle_request(self, method):
        # Extract the route
        path = self.path.split('?')[0]
        
        # Check if the route is defined
        for route, handler in self.routes:
            match = route.match(path)
            if match and method == route.method:
                # Extract query parameters
                query_params = self._parse_query_params(self.path)
                # Extract dynamic path parameters
                path_params = match.groupdict()
                # Handle the request and get the response
                response_data = handler(self, query_params, **path_params)
                # Send response
                self._send_response(response_data)
                return
        
        # If no matching route found
        self._send_error(404, 'Route not found')

    def _parse_query_params(self, path):
        """ Parse query parameters from URL """
        query_string = urllib.parse.urlparse(path).query
        return urllib.parse.parse_qs(query_string)
    
    def _send_response(self, data, status_code=200):
        """ Send a JSON response """
        response = json.dumps(data)
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """ Send an error response with status code """
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode('utf-8'))

    @classmethod
    def add_route(cls, method, path, handler):
        """ Register a route with a handler """
        # Convert path to a regex pattern that supports dynamic parameters
        route_pattern = cls._convert_to_pattern(path)
        cls.routes.append((route_pattern, handler))

    @staticmethod
    def _convert_to_pattern(path):
        """ Convert route path to a regular expression pattern """
        # This pattern matches dynamic parameters in the path (e.g., /user/<id>)
        pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        pattern = f"^{pattern}$"  # Ensure the pattern matches the full path
        return re.compile(pattern)


class SimpleAPI:
    def __init__(self, host='localhost', port=8080):
        self.server_address = (host, port)
        self.httpd = HTTPServer(self.server_address, APIRequestHandler)
    
    def add_route(self, method, path, handler):
        APIRequestHandler.add_route(method, path, handler)
    
    def run(self):
        print(f"Starting server on {self.server_address[0]}:{self.server_address[1]}")
        self.httpd.serve_forever()


# Example usage of the API module:

# Define a handler for a GET request to "/hello"
def hello_handler(request, query_params, **path_params):
    return {"message": "Hello, world!"}

# Define a handler for a POST request to "/echo"
def echo_handler(request, query_params, **path_params):
    content_length = int(request.headers['Content-Length'])
    body = request.rfile.read(content_length)
    json_data = json.loads(body)
    return {"received": json_data}

# Define a handler for a GET request to "/users/<id>"
def user_handler(request, query_params, **path_params):
    user_id = path_params.get('id')
    return {"user": {"id": user_id, "name": f"User {user_id}"}}

# Define a handler for a GET request to "/items"
def items_handler(request, query_params, **path_params):
    return {"items": ["apple", "banana", "cherry"]}

# Create API instance
api = SimpleAPI()

# Register routes
api.add_route('GET', '/hello', hello_handler)
api.add_route('POST', '/echo', echo_handler)
api.add_route('GET', '/users/<id>', user_handler)
api.add_route('GET', '/items', items_handler)

# Start the server
api.run()
