from .resources.configrations.controller import configuration_ns
from .resources.battery.controller import battery_ns
'''
common namespace doesn't have any endpoints and just has all the common marshals and parser
that we might need
'''
def register_endpoints_routes(api):
    """ "Routes "namespaces" Registration"""
    api.add_namespace(battery_ns)
    api.add_namespace(configuration_ns)