from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
from app import create_app
db = SQLAlchemy()

def create(scope="session"):
    app = create_app("mariadb://root:manager@localhost:3306/testing")

    # app =  Flask(__name__)
    # # Configurations for the app
    app.config['SQLALCHEMY_DATABASE_URI'] = "mariadb://root:manager@localhost:3306/testing"
    db.init_app(app)
    with app.app_context():
         db.create_all()
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    return app

# @pytest.fixture()
# def client(app):
#     return app.test_client()
@pytest.fixture(scope="session")
def client():
    app = create()
    return app.test_client()

@pytest.fixture(scope="session")
def created_store_id(client):
    response = client.post(
        "/mainstore",
        json={"name": "Test Store", "description": "my description"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    return response.json["mainstore_id"]


@pytest.fixture(scope="session")
def created_item_id(client, created_store_id):
    response = client.post(
        "/metastore",
        json={"name": "Test Item",
              "field_names": {"name":"chandu", "ids":"11470"},
              "trans_comments":"some comments",
              "source" : "somesource",
              "mainstore_id": created_store_id}
    )
    return response.json["metastore_id"]


@pytest.fixture(scope="session")
def created_tag_id(client, created_store_id):
    response = client.post(
        f"/mainstore/{created_store_id}/tag",
        json={"name": "Test Tag"},
    )
    return response.json()["tag_id"]


