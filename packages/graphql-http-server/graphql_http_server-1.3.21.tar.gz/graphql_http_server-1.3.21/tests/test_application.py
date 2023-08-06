import threading
import time
import urllib
from datetime import datetime

import pytest
from context_helper import ctx
from graphql_api import field
from requests import request, ConnectTimeout, ReadTimeout
from werkzeug import Response
from werkzeug.test import EnvironBuilder, Client
from werkzeug.wrappers import Request

from graphql_http_server import GraphQLHTTPServer
from graphql_http_server.service.context import ServiceContextMiddleware
from graphql_http_server.service.manager import \
    ServiceConnection, \
    ServiceManager


def is_graphql_api_installed():
    try:
        import graphql_api
        assert graphql_api
    except ImportError:
        return False

    return True


def available(url, method="GET"):
    try:
        response = request(
            method,
            url,
            headers={"Accept": "text/html"},
            timeout=5,
            verify=False
        )
    except (ConnectionError, ConnectTimeout, ReadTimeout):
        return False

    if response.status_code == 400 or response.status_code == 200:
        return True

    return False


class TestApplication:

    def test_dispatch(self, schema):
        server = GraphQLHTTPServer(schema=schema)

        builder = EnvironBuilder(method='GET', query_string="query={hello}")

        request = Request(builder.get_environ())
        response = server.dispatch(request=request)

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_app(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().get('/?query={hello}')

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_health_endpoint(self, schema):
        server = GraphQLHTTPServer(schema=schema, health_path="/health")
        response = server.client().get('/health')

        assert response.status_code == 200
        assert response.data == b'OK'

    def test_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().get('/', headers={"Accept": "text/html"})

        assert response.status_code == 200
        assert b'GraphiQL' in response.data

    def test_no_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema, serve_graphiql=False)
        response = server.client().get('/', headers={"Accept": "text/html"})

        assert response.status_code == 200

    def test_run_app_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema)

        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()

        time.sleep(0.5)

        req = urllib.request.Request(
            "http://localhost:5000",
            headers={"Accept": "text/html"}
        )
        response = urllib.request.urlopen(req).read()

        assert b'GraphiQL' in response

    @pytest.mark.skipif(
        not is_graphql_api_installed(),
        reason="GraphQL-API is not installed"
    )
    def test_graphql_api(self):
        from graphql_api import GraphQLAPI

        api = GraphQLAPI()

        @api.type(root=True)
        class RootQueryType:

            @api.field
            def hello(self, name: str) -> str:
                return f"hey {name}"

        server = GraphQLHTTPServer.from_api(api=api)

        response = server.client().get('/?query={hello(name:"rob")}')

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"hey rob"}}'

    utc_time_api_url = \
        "https://europe-west2-parob-297412.cloudfunctions.net/utc_time"

    # noinspection DuplicatedCode,PyUnusedLocal
    @pytest.mark.skipif(
        not available(utc_time_api_url),
        reason=f"The UTCTime API '{utc_time_api_url}' is unavailable"
    )
    @pytest.mark.skipif(
        not is_graphql_api_installed(),
        reason="GraphQL-API is not installed"
    )
    def test_service_manager(self):
        from graphql_api import GraphQLAPI

        class UTCTimeServiceStub:

            @field
            def now(self) -> str:
                pass

        connections = [ServiceConnection(
            name="utc_time",
            api_url=self.utc_time_api_url,
            schema=UTCTimeServiceStub
        )]

        service_manager = ServiceManager(
            name="gateway",
            api_version="0.0.1",
            connections=connections
        )

        api = GraphQLAPI()

        @api.type(root=True)
        class RootQueryType:

            @api.field
            def hello(self, name: str) -> str:
                utc_time: UTCTimeServiceStub = ctx.services["utc_time"]

                return f"hey {name}, the time is {utc_time.now()}"

        server = GraphQLHTTPServer.from_api(api=api)

        client = Client(
            ServiceContextMiddleware(
                server.app(),
                service_manager,
                "/service"
            ),
            Response
        )

        response = client.get('/service?query={logs}')

        assert response.status_code == 200
        assert "ServiceState = OK" in response.text

        response = client.get('/?query={hello(name:"rob")}')

        assert response.status_code == 200
        assert "rob" in response.text
        assert datetime.today().strftime('%Y-%m-%d') in response.text
