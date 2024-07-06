import requests
URL = "https://petstore.swagger.io/v2"
class TestPet:

    def test_add_pet(self):
        new_pet = {
            "id": 1,
            "category": {
                "id": 1,
                "name": "Dogs"},
            "name": "Max",
            "photoUrls": [],
            "tags": [ {
                "id": 0,
                "name": "Cute"}],
            "status": "available"
        }
        response = requests.post(f"{URL}/pet", json=new_pet)
        assert response.status_code == 200
        assert response.json()["name"] == "Max"

    def test_add_pet_photo(self):
        pet_id = 1
        response = requests.get(f"{URL}/pet/{pet_id}")
        assert response.status_code == 200

        with open("image/test_image.jpg", "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(f"{URL}/pet/{pet_id}/uploadImage", files=files)
            # print(f"POST /pet/{pet_id}/uploadImage - Response: {response.text}")
        assert response.status_code == 200

    def test_update_pet(self):
        pet_id = 1
        updated_pet = {
            "id": pet_id,
            "category": {
                "id": 1,
                "name": "Dogs"},
            "name": "Goat", # update Name
            "photoUrls": ["link.example.com/goat.png"], # update photo
            "tags": [ {
                "id": 2, # ipdate tags
                "name": "Smile"}],
            "status": "sold" # update status
        }
        response = requests.put(f"{URL}/pet", json=updated_pet)
        assert response.status_code == 200
        assert response.json()["name"] == "Goat"

    def test_find_pet_byStatus(self):
        params = {"status": ["sold", "available"]}
        response = requests.get(f"{URL}/pet/findByStatus", params=params)
        assert response.status_code == 200

    def test_get_pet_by_id(self):
        pet_id = 1
        response = requests.get(f"{URL}/pet/{pet_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Goat"
        assert response.json()["id"] == pet_id

    def test_ipdate_pet_with_form_data(self):
        pet_id = 1
        data = {
            "petid": pet_id,
            "name": "Pet",
            "status": "pending"
            }
        response = requests.post(f"{URL}/pet/{pet_id}", data=data)
        assert response.status_code == 200

        response = requests.get(f"{URL}/pet/{pet_id}")
        # pprint.pprint(response.json())
        assert response.json()["id"] == pet_id
        assert response.json()["name"] == "Pet"
        assert response.json()["status"] == "pending"

    def test_delete_pet(self):
        pet_id = 1
        # response = api_client.get(f"{URL}/pet/{pet_id}")
        # pprint.pprint(response.json())
        response = requests.delete(f"{URL}/pet/{pet_id}")
        assert response.status_code == 200

    def test_add_only_id_pet(self):
        new_pet = {
            "id": 2199,
        }
        response1 = requests.post(f"{URL}/pet", json=new_pet)
        response = requests.get(f"{URL}/pet/2199")
        #  pprint.pprint(response.json())
        assert response1.status_code == 200
        assert response.json()["id"] == 2199

    def test_invalid_pet(self):
        pet_id = 'str'
        pet = {
            "id": pet_id,
            "category": {
                "id": 1,
                "name": "Dogs"},
            "name": 7,
            "photoUrls": [],
            "tags": [{
                "id": 567,
                "name": "Cute"}],
            "status": "inv"
        }
        requests.post(f"{URL}/pet", json=pet)
        response = requests.get(f"{URL}/pet/{pet_id}")
        # pprint.pprint(response.json())
        assert response.status_code == 404

    def test_invalid_update_pet(self):
        pet_id = 974567
        response = requests.get(f"{URL}/pet/{pet_id}")
        assert response.status_code == 404
        assert response.json()["message"] == "Pet not found"  # тест проходит

        updated_pet = {
            "id": pet_id,
            "name": "Empty",
        }
        response = requests.put(f"{URL}/pet", json=updated_pet)
        # pprint.pprint(response.json())
        assert response.status_code == 200  # при обновлении пета, если его нет, то создается новый !bug report

    def test_delete_invalid_pet(self):
        pet_id = 97451468
        response = requests.delete(f"{URL}/pet/{pet_id}")
        assert response.status_code == 404