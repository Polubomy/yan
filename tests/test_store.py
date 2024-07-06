class TestStore:

    def test_get_inventory(self, api_client):
        response = api_client.get("/store/inventory")
        assert response.status_code == 200


    def test_place_order(self, api_client):
        order = {
            "id": 9,
            "petId": 1,
            "quantity": 100,
            "shipDate": "2024-07-06T15:04:10.309Z",
            "status": "placed",
            "complete": True
        }
        response = api_client.post("/store/order", json=order)
        assert response.status_code == 200
        assert response.json()["id"] == 9

    def test_get_order_by_id(self, api_client):
        order_id = 9
        response = api_client.get(f"/store/order/{order_id}")
        assert response.status_code == 200
        assert response.json()["id"] == order_id

    def test_delete_order(self, api_client):
        order_id = 9
        response = api_client.delete(f"/store/order/{order_id}")
        assert response.status_code == 200
        response = api_client.get(f"/store/order/{order_id}")
        assert  response.status_code == 404

    def test_invalid_place_order(self, api_client):
        order = {
            "id": 24124,
            "petId": 6,
            "quantity": 100,
            "shipDate": "2024-07-06T15:04:10.309Z",
            "status": "placed",
            "complete": "2" # invalid type
        }
        response = api_client.post("/store/order", json=order)
        assert response.status_code >= 400

    def test_invalid2_place_order(self, api_client):
        order = {
            "id": 241624,
            "petId": 6,
            "quantity": 100,
            "shipDate": "2024-07-06T15:04:10.309Z",
            "status": "invalid", # not in list
            "complete": False
        }
        response = api_client.post("/store/order", json=order)
        assert response.status_code >= 400 # !in bug report

    def test_invalid3_place_order(self, api_client):
        order = {
            "id": 241254,
            "petId": 6,
            "quantity": 100,
            "shipDate": "18:17", # invalid data
            "status": "placed",
            "complete": False
        }
        response = api_client.post("/store/order", json=order)
        assert response.status_code >= 400

    def test_invalid_get_order_by_id(self, api_client):
        order_id = 4424112 #unknown id
        response = api_client.get(f"/store/order/{order_id}")
        assert response.status_code == 404 # order not found

    def test_invalid_delete_order(self, api_client):
        order_id = 2156125125 # unknown id
        response = api_client.delete(f"/store/order/{order_id}")
        assert response.status_code == 404
