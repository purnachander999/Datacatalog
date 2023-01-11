import pytest
import requests


api_url = "http://127.0.0.1:5000/store"
todo = {"name": "chandu", "description": "Buy milk"}
headers =  {"Content-Type":"application/json"}
response = requests.post(api_url, json=todo)
print(response.json())

# @pytest.fixture()
# def created_store_id(client):
#     response = client.post(
#         "/store",
#         json={"name1": "Test Store", "description": "Some Description"}
#     )
#
#     return response.json["id"]

#
# @pytest.fixture()
# def created_item_id(client, created_store_id):
#     response = client.post(
#         "/item",
#         json={"name": "Test Item", "price": 10.5, "store_id": created_store_id},
#     )
#
#     return response.json["id"]
#
#
# @pytest.fixture()
# def created_tag_id(client, created_store_id):
#     response = client.post(
#         f"/store/{created_store_id}/tag",
#         json={"name": "Test Tag"},
#     )
#
#     return response.json["id"]
