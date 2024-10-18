from .resources.users.controller import user_ns
'''
common namespace doesn't have any endpoints and just has all the common marshals and parser
that we might need
'''
def register_endpoints_routes(api):
    """ "Routes "namespaces" Registration"""
    api.add_namespace(user_ns)
