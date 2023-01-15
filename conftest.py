import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app("mariadb://root:manager@localhost:3306/testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app



@pytest.fixture
def client(app):
    return app.test_client()


