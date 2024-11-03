class APIRoute:
    def __init__(self, route):
        self.route = route

    def __str__(self):
        return f" - {self.route}"

class APIRoutes:
    def __init__(self, routes):
        self.routes = [APIRoute(route) for route in routes]

    def __str__(self):
        return "\n".join(str(route) for route in self.routes)