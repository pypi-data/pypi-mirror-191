import logging
import os
import argparse

import pluggy


__name__ = "llview"

logger = logging.getLogger(__name__)

hookimpl = pluggy.HookimplMarker("jumonc")


links = []

paths = []


@hookimpl
def needed_REST_paths():
    from jumonc.handlers.base import api_version_path
    return [api_version_path + "/llview",]


@hookimpl
def register_REST_path(requested_path, approved_path):
    from flask import jsonify, make_response
    
    from jumonc.handlers.base import check_version, RESTAPI, return_schema, get_return_schema_description
    from jumonc.authentication import scopes
    from jumonc.authentication.check import check_auth
    
    import jumonc.handlers.versionTree as tree
    
    tree.links["v1"].append({
                "link": "/v1/llview",
                "isOptional": True,
                "description": "Following this links leads to the llview jumonc plugin ",
                "parameters": [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
            })
    
    
    links.append({
                "link": "/v1/llview/paths",
                "isOptional": True,
                "description": "Following this links leads to the API paths to be used by LLVIEW",
                "parameters": [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
            })
    
    
    @RESTAPI.route(approved_path, methods=["GET"])
    @check_version
    @check_auth(scopes["see_links"])
    def llview_links(version):
        logger.debug("Accessed /v%i/llview/", version)
        return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)
    
    
    @RESTAPI.route(approved_path + "/paths", methods=["GET"])
    @check_version
    @check_auth(scopes["compute_data"])
    def llview_paths(version):
        return make_response(jsonify({"paths": paths}), 200)


@hookimpl
def startup_parameter_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=("jumonc llview plugin"), prog="jumonc --llview")

    parser.add_argument("--API-PATHS".lower(), 
                       dest="API_PATHS", 
                       help="Set API paths that can be querried by llview for the job reporting", 
                       default=[],
                       nargs='*',
                       type=str)
    return parser
    

@hookimpl
def evaluate_startup_parameter(parsed:argparse.Namespace) -> None:
    global paths
    
    paths = paths + parsed.API_PATHS
    

@hookimpl
def register_MPI(MPI_ID_min, MPI_ID_max):
    pass


@hookimpl
def selfcheck_is_working():
    return True
