# module provides functions to import toml to redis and export redis to toml
#
# logger : defines which logging instance should be used
# instance_name : prescriptive info as to which instance this configuration table should apply to
# table_name : prescriptive info as to what table should be written in redis
# toml_dict : dictionary with toml data for table table_name

import sys
import json

def toml_import(logger, instance_name, table_name, toml_dict):
    
    logger.debug("> " + sys._getframe().f_code.co_name + "()")
    logger.debug("instance_name: " + instance_name)
    logger.debug("table_name: " + table_name)
    # dump the dict we're supposed to write to kv store as JSON
    logger.debug(json.dumps(str(toml_dict)))

    logger.debug("< " + sys._getframe().f_code.co_name + "()")
    return



def toml_export(logger, instance_name, table_name):

    logger.debug("> " + sys._getframe().f_code.co_name + "()")
    logger.debug("instance_name: " + instance_name)
    logger.debug("table_name: " + table_name)

    # initialize toml_dict dict since it doesn't exist here

    toml_dict = {}

    # dump the dict retrieved from kv store as JSON
    logger.debug(json.dumps(str(toml_dict)))

    logger.debug("< " + sys._getframe().f_code.co_name + "()")
    return toml_dict
