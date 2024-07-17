# implement REST API using FastAPI

import sys
from fastapi import FastAPI
import uvicorn

import tooling

from routers.configuration.operations import init_router as init_configuration_router
from routers.database.operations import init_router as init_database_router
from routers.internal.operations import init_router as init_swissarmy_router
# from routers.test.operations import router as test_router

# Define API app as 'api'

api = FastAPI()

if __name__ == '__main__':

    # stubs follow, this should be read from redis kvs for instance, section 'hamframe'

    # see https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes for comment on worker counts

    # logger = tooling.logger_init('DEBUG')
    logger = tooling.logger_init()
    
    # check env and use defaults if not present

    env = tooling.check_env_vars()

    # set logger level based on what we got back
    
    tooling.set_log_level(env['LOG_LEVEL'])

    # dump environment we care about

    for var in env:
        logger.debug(f'env: {var}={env[var]}')

    # add REST routes

    api.include_router(router=init_configuration_router, prefix='/config')
    logger.debug('/config route added')
    api.include_router(router=init_database_router, prefix='/db')
    logger.debug('/db route ad')
    api.include_router(router=init_swissarmy_router, prefix='/internal', include_in_schema=False) # undocumented
    logger.debug('/internal route added (undocumented)')
    # api.include_router(test_router, prefix='/test')
    # logger.debug('/test route defined.')

    # start API

    uvicorn.run(
        app='__main__:api', 
        host=str(env['LISTENER_HOST']),
        port=int(env['LISTENER_PORT']),
        workers=int(env['LISTENER_WORKERS']),
        log_level=str(env['LOG_LEVEL'])
    )

