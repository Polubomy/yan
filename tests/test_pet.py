class TestPet:

    def test_add_pet(self, api_client):
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
        response = api_client.post("/pet", json=new_pet)
        assert response.status_code == 200
        assert response.json()["name"] == "Max"

    def test_add_pet_photo(self, api_client):
        pet_id = 1
        response = api_client.get(f"/pet/{pet_id}")
        assert response.status_code == 200

        with open("image/test_image.jpg", "rb") as image_file:
            files = {"file": image_file}
            response = api_client.post(f"/pet/{pet_id}/uploadImage", files=files)
            # print(f"POST /pet/{pet_id}/uploadImage - Response: {response.text}")
        assert response.status_code == 200

    def test_update_pet(self, api_client):
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
        response = api_client.put(f"/pet", json=updated_pet)
        assert response.status_code == 200
        assert response.json()["name"] == "Goat"

    def test_find_pet_byStatus(self, api_client):
        params = {"status": ["sold", "available"]}
        response = api_client.get(f"/pet/findByStatus", params=params)
        assert response.status_code == 200

    def test_get_pet_by_id(self, api_client):
        pet_id = 1
        response = api_client.get(f"/pet/{pet_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Goat"
        assert response.json()["id"] == pet_id

    def test_ipdate_pet_with_form_data(self, api_client):
        pet_id = 1
        data = {
            "petid": pet_id,
            "name": "Pet",
            "status": "pending"
            }
        response = api_client.post(f"/pet/{pet_id}", data=data)
        assert response.status_code == 200

        response = api_client.get(f"/pet/{pet_id}")
        # pprint.pprint(response.json())
        assert response.json()["id"] == pet_id
        assert response.json()["name"] == "Pet"
        assert response.json()["status"] == "pending"

    def test_delete_pet(self, api_client):
        pet_id = 1
        # response = api_client.get(f"/pet/{pet_id}")
        # pprint.pprint(response.json())
        response = api_client.delete(f"/pet/{pet_id}")
        assert response.status_code == 200

    def test_add_only_id_pet(self, api_client):
        new_pet = {
            "id": 2199,
        }
        response1 = api_client.post("/pet", json=new_pet)
        response = api_client.get(f"/pet/2199")
        #  pprint.pprint(response.json())
        assert response1.status_code == 200
        assert response.json()["id"] == 2199

    def test_invalid_pet(self, api_client):
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
        api_client.post("/pet", json=pet)
        response = api_client.get(f"/pet/{pet_id}")
        # pprint.pprint(response.json())
        assert response.status_code == 404

    def test_invalid_update_pet(self, api_client):
        pet_id = 9745867
        response = api_client.get(f"/pet/{pet_id}")
        assert response.status_code == 404
        assert response.json()["message"] == "Pet not found"  # тест проходит

        updated_pet = {
            "id": pet_id,
            "name": "Empty",
        }
        response = api_client.put(f"/pet", json=updated_pet)
        # pprint.pprint(response.json())
        assert response.status_code >= 400  # при обновлении пета, если его нет, то создается новый !bug report

    def test_delete_invalid_pet(self, api_client):
        pet_id = 9745868
        response = api_client.delete(f"/pet/{pet_id}")
        assert response.status_code == 404