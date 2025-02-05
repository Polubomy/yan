import pprint
import requests

URL = "https://petstore.swagger.io/v2"

class TestUser:
    def test_create_user(self):
        new_user = {
            "id": 1432,
            "username": "test",
            "firstName": "Max",
            "lastName": "D",
            "email": "polubomy.max@gmail.com",
            "password": "qwerty",
            "phone": "+79307005593",
            "userStatus": 0
        }
        response = requests.post(f"{URL}/user", json=new_user)
        assert response.status_code == 200

    def test_get_user_by_username(self):
        username = "test"
        response = requests.get(f"{URL}/user/{username}")
        # pprint.pprint(response.json())
        assert response.status_code == 200
        assert response.json()["username"] == username

    def test_delete_user(self):
        username = "test"
        response = requests.delete(f"{URL}/user/{username}")
        assert response.status_code == 200

    def test_create_array_and_list_user(self):
        array_of_user = [
            {
                "id": 11,
                "username": "11",
                "firstName": "f11",
                "lastName": "l11",
                "email": "11@mail.ru",
                "password": "qwerty11",
                "phone": "111111",
                "userStatus": 0
            },
            {
                "id": 12,
                "username": "12",
                "firstName": "f12",
                "lastName": "l12",
                "email": "12@mail.ru",
                "password": "qwerty12",
                "phone": "12121212",
                "userStatus": 1
            }

        ]
        response = requests.post(f"{URL}/user/createWithList", json=array_of_user)
        assert response.status_code == 200

        id1, id2 = array_of_user[0]["id"], array_of_user[1]["id"]
        res1 = requests.get(f"{URL}/user/{id1}")
        res2 = requests.get(f"{URL}/user/{id2}")
            # pprint.pprint(res1.json())
            # pprint.pprint(res2.json())
        assert res1.json()["id"] == id1
        assert res2.json()["id"] == id2

    def test_update_user(self):
        username = "12"
        new_user = {
                "id": 12,
                "username": username,
                "firstName": "f_new",
                "lastName": "l_new",
                "email": "new@mail.ru",
                "password": "new_pass",
                "phone": "new_phone",
                "userStatus": 1
            }
        response = requests.put(f"{URL}/user/{username}", json=new_user)
        assert response.status_code == 200

        res1 = requests.get(f"{URL}/user/{username}")
        assert res1.status_code == 200
        # pprint.pprint(res1.json())
        firstName = new_user["firstName"]
        lastName = new_user["lastName"]
        password = new_user["password"]
        assert res1.json()["firstName"] == firstName
        assert res1.json()["lastName"] == lastName
        assert res1.json()["password"] == password

    def test_user_login(self):
        username = "test"
        password = "qwerty"

        user = {
            "username": username,
            "password": password
        }
        response = requests.get(f"{URL}/user/login", params=user)
        assert response.status_code == 200

        expires = response.headers.get("X-Expires-After")
        rate = response.headers.get("X-Rate-Limit")
        assert expires is not None
        assert rate is not None

    def test_logout_user(self):
        response = requests.get(f"{URL}/user/logout")
        assert response.status_code == 200 # ?

    def test_logout2_user(self):
        data = {
            "username": "test"
        }
        response = requests.get(f"{URL}/user/logout", json=data)
        assert response.status_code == 200

    def test_logout3_user(self):
            data = {
                "username": "2344bfegnbdtyu45645h64"
            }
            response = requests.get(f"{URL}/user/logout", json=data)
            assert response.status_code == 200 # ?

    def test_invalid_get_user_by_username(self):
        username = "**ASDH#SAD"
        response = requests.get(f"{URL}/user/{username}")
        assert response.status_code == 404 # User not found

    def test_invalid_delete_user(self):
        username = "**ASDH#SAD"
        response = requests.delete(f"{URL}/user/{username}")
        assert response.status_code == 404 # User not found

    def test_invalid_username_update(self):
        username = "kh1jkASDjH#SAD"
        new_user_inv = {
            "id": 99999,
            "username": username,
            "firstName": "newM",
            "lastName": "NewL",
            "email": "NewMail",
            "password": "newPass",
            "phone": "NewPhone",
            "userStatus": 0
        }
        get_empty_username = requests.get(f"{URL}/user/{username}")
        assert get_empty_username.status_code == 404 # User not found

        response = requests.put(f"{URL}/user/{username}", json=new_user_inv)
        assert response.status_code == 200

        get_empty_username_after_put = requests.get(f"{URL}/user/{username}")
        assert get_empty_username_after_put.status_code == 404 #При обновлении не добавился новый!

    def test_invalid_user_login(self):
        username = "fgdj65h*etj"
        password = "412dgh124124"

        user = {
            "username": username,
            "password": password
        }

        response_watch = requests.get(f"{URL}/user/{username}")
        assert response_watch.status_code == 404 # # User not found

        response = requests.get(f"{URL}/user/login", params=user)
        assert response.status_code == 200 # (400) bug. Логинит несуществующий логин и пароль

