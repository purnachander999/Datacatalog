import pytest

@pytest.mark.run(order=18)
def test_create_item_in_store(client, created_store_id):
    response = client.post(
        "/metastore",
        json={"name": "Test Item1",
              "field_names": {"name": "chandu", "ids": "11470"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )

    assert response.status_code == 201
    assert response.json["name"] == "Test Item1"
    assert response.json["mainstore"]["mainstore_id"] == created_store_id
    assert response.json["mainstore"]["name"] == "Test Store"

@pytest.mark.run(order=19)
def test_create_item_with_store_id_not_found(client, created_store_id):
    # Note that this will fail if foreign key constraints are enabled.
    response = client.post(
        "/metastore",
        json={"name": "Main store id not exists",
              "field_names": {"Emp_id": "Integer", "Ename": "String"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id + "1"}
    )

    assert response.status_code == 500
@pytest.mark.run(order=20)
def test_create_item_with_unknown_data(client):
    response = client.post(
        "/metastore",
        json={
            "name": "Test Item",
            "price": 10.5,
            "store_id": 1,
            "unknown_field": "unknown",
        },
    )

    assert response.status_code == 422
    assert response.json["errors"]["json"]["unknown_field"] == ["Unknown field."]

@pytest.mark.run(order=21)
def test_delete_item(client, created_store_id):
    response = client.post(
        "/metastore",
        json={"name": "Test Item1",
              "field_names": {"name": "chandu", "ids": "11470"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )
    delete_metastore_id = response.json["metastore_id"]
    meta_response = client.delete(
        f"/metastore/{delete_metastore_id}"
    )

    assert meta_response.status_code == 200
    assert meta_response.json["message"] == "Metastore deleted"

@pytest.mark.run(order=22)
def test_update_item(client, created_store_id):
    response = client.post(
        "/metastore",
        json={"name": "Test Update",
              "field_names": {"name": "chandu", "ids": "11470"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )
    update_metastore_id = response.json["metastore_id"]

    response = client.put(
        f"/metastore/{update_metastore_id}",
        json={"name": "Test Item (updated)"},
    )

    assert response.status_code == 200
    assert response.json["name"] == "Test Item (updated)"

@pytest.mark.run(order=23)
def test_get_all_metastores(client, created_store_id):
    response = client.post(
        "/metastore",
        json={"name": "Test metastore list 1",
              "field_names": {"name": "chandu", "ids": "11470"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )
    response = client.post(
        "/metastore",
        json={"name": "Test metastore list 2",
              "field_names": {"name": "chandu", "ids": "11470"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )

    response = client.get(
        "/metastore",
    )

    assert response.status_code == 200
    assert len(response.json) > 1

@pytest.mark.run(order=24)
def test_get_all_items_empty(client):
    response = client.get(
        "/metastore",
    )

    assert response.status_code == 200
    assert len(response.json) > 0

@pytest.mark.run(order=25)
def test_get_item_details(client, created_item_id):
    response = client.get(
        f"/metastore/{created_item_id}",
    )

    assert response.status_code == 200
    assert response.json["name"] == "Test Item"

# @pytest.mark.run(order=26)
# def test_get_item_details_with_tag(client, created_item_id, created_tag_id):
#     client.post(f"/metastore/{created_item_id}/tag/{created_tag_id}")
#     response = client.get(
#         f"/metastore/{created_item_id}",
#     )
#
#     assert response.status_code == 200

@pytest.mark.run(order=26)
def test_get_item_detail_not_found(client):
    response = client.get(
        "/metastore/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}
