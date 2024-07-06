import requests

URL = "https://petstore.swagger.io/v2"
class TestStore:

    def test_get_inventory(self):
        response = requests.get(f"{URL}/store/inventory")
        assert response.status_code == 200

    def test_place_order(self,):
        order = {
            "id": 9,
            "petId": 1,
            "quantity": 100,
            "shipDate": "2024-07-06T15:04:10.309Z",
            "status": "placed",
            "complete": True
        }
        response = requests.post(f"{URL}/store/order", json=order)
        assert response.status_code == 200
        assert response.json()["id"] == 9

    def test_get_order_by_id(self):
        order_id = 9
        response = requests.get(f"{URL}/store/order/{order_id}")
        assert response.status_code == 200
        assert response.json()["id"] == order_id

    def test_delete_order(self):
        order_id = 9
        response = requests.delete(f"{URL}/store/order/{order_id}")
        assert response.status_code == 200
        response = requests.get(f"{URL}/store/order/{order_id}")
        assert  response.status_code == 404

    def test_invalid_place_order(self):
        order = {
            "id": 24124,
            "petId": 6,
            "quantity": 100,
            "shipDate": "2024-07-06T15:04:10.309Z",
            "status": "placed",
            "complete": "2" # invalid type
        }
        response = requests.post(f"{URL}/store/order", json=order)
        assert response.status_code >= 400

    def test_invalid2_place_order(self):
        order = {
            "id": 241624,
            "petId": 6,
            "quantity": 100,
            "shipDate": "2024-07-06T15:04:10.309Z",
            "status": "invalid", # not in list
            "complete": False
        }
        response = requests.post(f"{URL}/store/order", json=order)
        assert response.status_code == 200 # !in bug report, должна быть ошибка

    def test_invalid3_place_order(self):
        order = {
            "id": 241254,
            "petId": 6,
            "quantity": 100,
            "shipDate": "18:17", # invalid data
            "status": "placed",
            "complete": False
        }
        response = requests.post(f"{URL}/store/order", json=order)
        assert response.status_code >= 400

    def test_invalid_get_order_by_id(self):
        order_id = 4424112 #unknown id
        response = requests.get(f"{URL}/store/order/{order_id}")
        assert response.status_code == 404 # order not found

    def test_invalid_delete_order(self):
        order_id = 2156125125 # unknown id
        response = requests.delete(f"{URL}/store/order/{order_id}")
        assert response.status_code == 404
