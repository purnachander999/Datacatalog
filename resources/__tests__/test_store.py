

def test_all_store_before_creation(client):
    response = client.get(
        "/mainstore",
    )

    assert response.status_code == 200
    assert type(response.json) == list

def test_get_store(client, created_store_id):
    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200
    # assert response.json["name"] == "Test Store"
    # assert response.json["description"] == "my description"

def test_get_store_name(client, created_store_id):
    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["name"] == "Test Store"

def test_get_store_description(client, created_store_id):
    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["description"] == "my description"


def test_get_store_description_again(client, created_store_id):
    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["description"] == "my description"


def test_get_store_not_found(client):
    response = client.get(
        "/mainstore/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_get_store_with_item(client, created_store_id):
    client.post(
        "/metastore",
        json={"name": "store with item",
              "field_names": {"Emp_id": "Integer", "Ename": "String"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )

    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["metastore"][0]["name"] == "store with item"


def test_get_store_with_tag(client, created_store_id):
    client.post(
        f"/mainstore/{created_store_id}/tag",
        json={"name": "Test Tag"},
    )

    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["tags"][0]["name"] == "Test Tag"


def test_create_store(client):
    response = client.post(
        "/mainstore",
        json={"name": "Creating new store", "description": "new description"},
    )

    assert response.status_code == 201
    assert response.json["name"] == "Creating new store"


def test_create_store_with_items(client, created_store_id):
    client.post(
        "/metastore",
        json={"name": "store with items",
              "field_names": {"Emp_id": "Integer", "Ename": "String"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": created_store_id}
    )

    # Get the store with id 1 and check the items contains the newly created item
    response = client.get(
        f"/mainstore/{created_store_id}",
    )

    assert response.status_code == 200


def test_delete_store(client):
    response = client.post(
        "/mainstore",
        json={"name": "Creating new store for deletion ", "description": "new description for deletion"},
    )

    assert response.status_code == 201
    del_obj = response.json["mainstore_id"]


    response = client.delete(
        f"/mainstore/{del_obj}",
    )

    assert response.status_code == 200
    assert response.json == {"message": "Store deleted"}


def test_delete_store_doesnt_exist(client):
    response = client.delete(
        "/mainstore/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}




def test_get_store_list_single(client):
    resp = client.post(
        "/mainstore",
        json={"name": "Single store", "description":"Single description"}
    )

    get_single_store = resp.json["mainstore_id"]

    response = client.get(
         f"/mainstore/{get_single_store}"
    )

    assert response.status_code == 200


def test_get_store_list_multiple(client):
    client.post(
        "/mainstore",
        json={"name": "Test Store 11"},
    )
    client.post(
        "/mainstore",
        json={"name": "Test Store 22"},
    )

    response = client.get(
        "/mainstore",
    )

    assert response.status_code == 200

def test_get_store_list_with_items(client):
    simple_strore = client.post(
        "/mainstore",
        json={"name": "Just Store", "description":"store description"},
    )

    simple_store_id = simple_strore.json["mainstore_id"]

    client.post(
        "/metastore",
        json={"name": "store with item",
              "field_names": {"Dept_id": "Integer", "Dname": "String"},
              "trans_comments": "some comments",
              "source": "somesource",
              "mainstore_id": simple_store_id}
    )
    response = client.get(
        "/mainstore",
    )

    assert response.status_code == 200
    assert type(response.json) == list


def test_get_store_list_with_tags(client):
    resp = client.post(
        "/mainstore",
        json={"name": "Test Store Tags", "description": "just a short description"},
    )
    client.post(
        f"/mainstore/{resp.json['mainstore_id']}/tag",
        json={"name": "Test Tag"},
    )
    response = client.get(
        "/mainstore",
    )

    assert response.status_code == 200
    assert type(response.json) == list

def test_create_store_duplicate_name(client):
    client.post(
        "/mainstore",
        json={"name": "Test Store Already exists", "description" : "Small description"},
    )

    response = client.post(
        "/mainstore",
        json={"name": "Test Store Already exists", "description" : "Small description"},
    )
    assert response.status_code == 400
    assert response.json["message"] == "A store with that name already exists."
