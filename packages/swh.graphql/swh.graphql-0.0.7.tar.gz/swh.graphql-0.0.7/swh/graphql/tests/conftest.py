# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os

import pytest
from starlette.testclient import TestClient

from swh.graphql import server as app_server

from .data import populate_dummy_data, populate_search_data


@pytest.fixture(scope="session")
def test_app():
    os.environ["SWH_CONFIG_FILENAME"] = os.path.join(
        os.path.dirname(__file__), "../config/test.yml"
    )
    app = app_server.make_app_from_configfile()
    return app


@pytest.fixture(scope="session")
def storage(test_app):
    storage = app_server.get_storage()
    # populate the in-memory storage
    populate_dummy_data(storage)
    return storage


@pytest.fixture(scope="session")
def search(test_app):
    search = app_server.get_search()
    search.initialize()
    # populate the in-memory search
    populate_search_data(search)
    return search


@pytest.fixture(scope="session")
def client(test_app, storage, search):
    yield TestClient(test_app)


@pytest.fixture
def high_query_cost():
    query_cost = app_server.graphql_cfg["max_query_cost"]["anonymous"]
    app_server.graphql_cfg["max_query_cost"]["anonymous"] = 2000
    yield
    app_server.graphql_cfg["max_query_cost"]["anonymous"] = query_cost


@pytest.fixture
def none_query_cost():
    # There will not be any query cost limit in this case
    query_cost = app_server.graphql_cfg["max_query_cost"]["anonymous"]
    app_server.graphql_cfg["max_query_cost"]["anonymous"] = None
    yield
    app_server.graphql_cfg["max_query_cost"]["anonymous"] = query_cost
