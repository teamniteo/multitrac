from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from multitrac.models import initialize_sql


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'multitrac:static')
    config.scan('multitrac')
    config.add_route('root', '/')
    config.add_route('settings', '/settings')
    config.add_route('tickets', '/tickets')
    config.add_route('hours', '/hours')
    return config.make_wsgi_app()
