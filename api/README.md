# API

## TOC

- [Configuration](#configuration)
- [Using the API](#using-the-api)\
-- [Container](#container)\
-- [Python from .venv](#python-from-venv)
- [OpenAPI docs](#openapi-docs)

## Overview

The API is a lightweight abstraction and supports RESTful operations for JSON encoded objects.

## Configuration API

### Structure

Multiple sets of configurations can be managed by naming different _instances_.  Within an instance, multiple _sections_ can be defined.

The value associated with a key is encoded as a JSON object and not validated beyond being valid JSON.  Lightweight abstraction means the responsibility for validating and understanding encoded JSON data rests with the consumers of the API for the value part of anything stored in KVS.

If _section_ is not specified in the API call, the operation will assume _section_ to be a wildcard and potentially match multiple _sections_ within the same _instance_ if they exist. Each section is returned as a numbered enumeration of the resulting array.  The response message in the body of the request indicates number of sections were matched with the property _"sections:"_ with an integer value.

If _instance_ is not specified in the API call, the operation will assume _instance_ to be a wildcard and potentially match multiple _instances_. Each instance is returned as a numbered enumeration of the resulting array. The response message in the body of the request indicates number of instances were matched with the property _"instances:"_ with an integer value.


### Backend

Configuration is stored in a [Redis](redis.io)-compatible key-value store ([KVS](https://en.wikipedia.org/wiki/Key%E2%80%93value_database)). Keys are encoded in KVS as _config:\<instance\>:\<section\>_, like _config_:_ak7vv_:_n0nbh_ for a configuration section _n0nbh_ within the instance _ak7vv_.  The KVS is always assumed to be local unless specified otherwise (REDIS_HOST, REDIS_PORT environment variables).  A single API instance can only be associated with a single KVS endpoint.

One example of a consumer of the API are the CLI commands in [../cli](../cli) that invoke REST API calls to implement the CLI backend.  Components integrated with Hamframe can use the API to retrieve or modify configuration sections.

## Using the API

The API is implemented as a Docker container running [FastAPI](https://fastapi.tiangolo.com/).  By default, the API will open 65432/tcp unless you specify LISTENER_PORT environment variable to be something else. The API will listen on localhost unless you specify something else with LISTENER_HOST environment variable.  If you need access from outside the host, specify the LISTENER_HOST to be the IP address or DNS name of a single interface or 0.0.0.0 to listen on all.

The API is versioned as, for example, "/v1/configuration" to allow for what would otherwise be breaking changes over time.  The intent is to support GET, PUT, PATCH, and DELETE for all objects, but the completeness may vary.  Root "/" has no significance.

### Container

This repo will trigger a GitHub Actions workflow to build a new container (for linux/amd64 and linux/arm64) and push a successful build to [Docker Hub ak7vv/hamframe-api](https://hub.docker.com/r/ak7vv/hamframe-api) if anything that runs in the container is modified in the repo.

You can run this container with

```shell
    docker run \
        --name api \
        --publish 65432:65432 \
        ak7vv/hamframe-api
```

and optionally you can pass environment variables like

```shell
    docker run \
        --name api \
        --env LOG_LEVEL=debug \
        --env LISTENER_HOST=0.0.0.0 \
        --publish 65432:65432 \
        ak7vv/hamframe-api
```

Remember that the environment variables always have to be defined before the container name and not after.

### python from .venv:

You can also run the API by starting it directly from python inside a virtual environment.  This is mainly intended for dev:

```shell
    python api.py
```

and optionally you can pass environment variables like

```shell
    export LOG_LEVEL=debug \
    export LISTENER_HOST=0.0.0.0 \
    python api.py
```

Use the Container if you intend to use this code.

## Testing

/tests contains the [pytest](https://docs.pytest.org/en/stable/) testing framework [integrated with FastAPI](https://fastapi.tiangolo.com/tutorial/testing/) and will be expanded over time. Run with 'pytest'.

You can find the beginnings in [tests/test_api.py](tests/test_api.py).

Test coverage is poor at this time. (Issue #)

## OpenAPI docs

FastAPI is self-documenting as [OpenAPI](https://www.openapis.org/) (the artist formerly known as Swagger), which can be found at

http://_host_ip_:65432/openapi.json

You can also find human-readable variants here:

http://_host_ip_:65432/docs\
http://_host_ip_:65432/redoc

where you can learn about the API verbs and attributes as well as exercise the API.
