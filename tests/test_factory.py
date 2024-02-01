from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient
from example_app.factory import AppConfig, create_app


def test_index_page():
    config = AppConfig(debug=True)
    app = create_app(config)
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK
