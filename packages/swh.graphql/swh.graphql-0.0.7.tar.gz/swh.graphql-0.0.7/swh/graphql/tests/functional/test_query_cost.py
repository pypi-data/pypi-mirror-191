# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from . import utils
from ..data import get_snapshots


def test_valid_query(client):
    query_str = """
    query getOrigins {
      origins(first: 2) {
        nodes {
          url
        }
      }
    }
    """
    response, _ = utils.get_query_response(client, query_str)
    assert len(response["origins"]["nodes"]) == 2


def test_query_cost_simple(client):
    query_str = """
    query getOrigins {
      origins(first: 1000) {
        nodes {
          url
        }
      }
    }
    """
    errors = utils.get_error_response(client, query_str, response_code=400)
    assert (
        "The query exceeds the maximum cost of 100. Actual cost is 1000"
        in errors[0]["message"]
    )


def test_query_cost_with_no_limit(client, none_query_cost):
    # No cost validation
    query_str = """
    query getOrigins {
      origins(first: 1000) {
        nodes {
          url
        }
      }
    }
    """
    response, _ = utils.get_query_response(client, query_str)
    assert len(response["origins"]["nodes"]) == 2


def test_query_cost_origin(client):
    query_str = """
    query getOrigins {
      origins(first: 10) {
        nodes {
          url
          latestVisit {
            date
          }
          visits(first: 5) {
            nodes {
              date
              statuses {
                nodes {
                  date
                }
              }
            }
          }
          snapshots(first: 5) {
            nodes {
              swhid
            }
          }
        }
      }
    }
    """
    # Total cost here is 170
    # 10 (origin) + 10 (latestVisit) + 10*5 (visits) + 10 * 5 * 3 (status) +
    # 10 * 5*2 (snapshots) = 320
    errors = utils.get_error_response(client, query_str, response_code=400)
    assert (
        "The query exceeds the maximum cost of 100. Actual cost is 320"
        in errors[0]["message"]
    )


def test_query_cost_snapshots(client):
    query_str = """
    query getSnapshot($swhid: SWHID!) {
      snapshot(swhid: $swhid) {
        branches(first: 50) {
          nodes {
            target {
              node {
                ...on Revision {
                  swhid
                }
                ...on Directory {
                  swhid
                  entries(first: 3) {
                    nodes {
                      name {
                        text
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    # Total cost here is 157
    # 1 (snapshot) + 2 *50 (branches) + 50 * 1 (branch target)
    # + 50 * 1 (revision or Directory) +  3 * 2 = 207
    # parent multiplier is not applied when schema introspection is used
    # ie: directory entry connection cost is 3 * 2 and not 50 * 3 * 2
    errors = utils.get_error_response(
        client, query_str, swhid=str(get_snapshots()[0].swhid()), response_code=400
    )
    assert (
        "The query exceeds the maximum cost of 100. Actual cost is 207"
        in errors[0]["message"]
    )
