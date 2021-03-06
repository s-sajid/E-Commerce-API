import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# Create/Destroy all tables per test
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database override for testing
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


# Test user 1
@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com",
                 "password": "test_password1",
                 "username": "test1"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


# Test user 2
@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com",
                 "password": "test_password2",
                 "username": "test2"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


# Access token
@pytest.fixture
def token(test_user):

    return create_access_token({"user_id": test_user['id']})


# Autherize token
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


# Create test posts and add to DB
@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first",
        "owner_id": test_user['id']
    }, {
        "title": "second title",
        "content": "second",
        "owner_id": test_user['id']
    },
        {
        "title": "third title",
        "content": "third",
        "owner_id": test_user['id']
    }, {
        "title": "fourth title",
        "content": "fourth",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()
    return posts


# Create test products and add to DB
@pytest.fixture
def test_products(test_user, test_user2, session):
    products_data = [{
        "prod_name": "first product",
        "description": "first description",
        "company_name": "first company",
        "price": 1.99,
        "owner_id": test_user['id']
    }, {
        "prod_name": "second product",
        "description": "second description",
        "company_name": "second company",
        "price": 2.99,
        "owner_id": test_user['id']
    },
        {
        "prod_name": "third product",
        "description": "third description",
        "company_name": "third company",
        "price": 3.99,
        "owner_id": test_user['id']
    }, {
        "prod_name": "fourth product",
        "description": "fourth description",
        "company_name": "fourth company",
        "price": 4.99,
        "owner_id": test_user2['id']
    }]

    def create_product_model(product):
        return models.Product(**product)

    product_map = map(create_product_model, products_data)
    products = list(product_map)

    session.add_all(products)

    session.commit()

    products = session.query(models.Product).all()
    return products
