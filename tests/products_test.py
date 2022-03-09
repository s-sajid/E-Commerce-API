import pytest
from app import schemas


def test_get_all_products(authorized_client, test_products):
    res = authorized_client.get("/products/")

    assert len(res.json()) == len(test_products)
    assert res.status_code == 200
    

def test_unauthorized_user_get_all_products(client, test_products):
    res = client.get("/products/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_product(client, test_products):
    res = client.get(f"/products/{test_products[0].id}")

    assert res.status_code == 401


def test_get_one_product_not_exist(authorized_client, test_products):
    res = authorized_client.get(f"/products/-1")

    assert res.status_code == 404


def test_get_one_product(authorized_client, test_products):
    res = authorized_client.get(f"/products/{test_products[0].id}")
    product = schemas.ProductOut(**res.json())

    assert product.id == test_products[0].id
    assert product.prod_name == test_products[0].prod_name
    assert product.description == test_products[0].description
    assert product.company_name == test_products[0].company_name
    assert product.price == test_products[0].price


@pytest.mark.parametrize("prod_name, description, company_name, price, published", [
    ("product 1", "description 1", "company 1", 1.99, True),
    ("product 2", "description 2", "company 2", 2.99, False),
    ("product 3", "description 3", "company 3", 3.99, True)
])
def test_create_product(authorized_client, test_user, test_products, prod_name, description, company_name, price, published):    
    res = authorized_client.post(
        "/products/", json={"prod_name": prod_name, 
                        "description": description, 
                        "company_name": company_name, 
                        "price": price, 
                        "published": published})

    created_product = schemas.Product(**res.json())

    assert res.status_code == 201
    assert created_product.prod_name == prod_name
    assert created_product.description == description
    assert created_product.company_name == company_name
    assert created_product.price == price
    assert created_product.published == published
    assert created_product.owner_id == test_user['id']


def test_create_product_default_published_true(authorized_client, test_user, test_products):
    res = authorized_client.post(
        "/products/", json={"prod_name": "default prod_name", 
                        "description": "default description", 
                        "company_name": "default company_name", 
                        "price": 0.00})

    created_product = schemas.Product(**res.json())

    assert res.status_code == 201
    assert created_product.prod_name == "default prod_name"
    assert created_product.description == "default description"
    assert created_product.company_name == "default company_name"
    assert created_product.price == 0.00
    assert created_product.published == True
    assert created_product.owner_id == test_user['id']


def test_unauthorized_user_create_product(client, test_user, test_products):
    res = client.post(
        "/products/", json={"prod_name": "prod_name", 
                        "description": "description", 
                        "company_name": "company_name", 
                        "price": 0.00})

    assert res.status_code == 401


def test_unauthorized_user_delete_product(client, test_user, test_products):
    res = client.delete(
        f"/products/{test_products[0].id}")

    assert res.status_code == 401


def test_delete_product_success(authorized_client, test_user, test_products):
    res = authorized_client.delete(
        f"/products/{test_products[0].id}")

    assert res.status_code == 204


def test_delete_product_non_exist(authorized_client, test_user, test_products):
    res = authorized_client.delete(
        f"/products/-2")

    assert res.status_code == 404


def test_delete_other_user_product(authorized_client, test_user, test_products):
    res = authorized_client.delete(
        f"/products/{test_products[3].id}")

    assert res.status_code == 403


def test_update_product(authorized_client, test_user, test_products):
    data = {
        "prod_name": "updated prod_name",
        "description": "updated description",
        "company_name": "updated company_name",
        "price": 99.99,
        "id": test_products[0].id
    }

    res = authorized_client.put(f"/products/{test_products[0].id}", json=data)
    updated_product = schemas.Product(**res.json())

    assert res.status_code == 200
    assert updated_product.prod_name == data['prod_name']
    assert updated_product.description == data['description']
    assert updated_product.company_name == data['company_name']
    assert updated_product.price == data['price']


def test_update_other_user_product(authorized_client, test_user, test_user2, test_products):
    data = {
        "prod_name": "updated prod_name",
        "description": "updated description",
        "company_name": "updated company_name",
        "price": 99.99,
        "id": test_products[3].id

    }
    res = authorized_client.put(f"/products/{test_products[3].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_user_update_product(client, test_user, test_products):
    res = client.put(
        f"/products/{test_products[0].id}")

    assert res.status_code == 401


def test_update_product_non_exist(authorized_client, test_user, test_products):
    data = {
        "prod_name": "updated prod_name",
        "description": "updated description",
        "company_name": "updated company_name",
        "price": 99.99,
        "id": test_products[3].id
    }

    res = authorized_client.put(
        f"/products/-3", json=data)

    assert res.status_code == 404
