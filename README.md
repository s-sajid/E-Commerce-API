# E-Commerce API

---
## Table of Contents

1. [Introduction](#Introduction)
2. [Documentation](#Docs)
3. [Technology](#Tech)
4. [Additional Notes](#Notes)
5. [Improvements](#Improvements)
6. [References](#References)

---
## Introduction <a name="Introduction"></a>

This is an application programming interface (API) that is designed for a business-to-business e-commerce platform.

---
## Documentation <a name="Docs"></a>

To view the fully interactive API documentation, please visit one of the following links listed below:

* https://heroku-ecommerce-api.herokuapp.com/docs

* https://heroku-ecommerce-api.herokuapp.com/redoc
  
---
## Technology <a name="Tech"></a>

The technologies used for this project include :

* [Python](https://www.python.org/)
  * Used as the primary development language
* [FastAPI](https://fastapi.tiangolo.com/)
  * Used as the primary development framework
* [PostgreSQL](https://www.postgresql.org/)
  * Used as the primary database system
* [Postman](https://www.postman.com/)
  * Used to design and test the API
* [Docker](https://www.docker.com/)
  * Used to containerize the API
* [Digital Ocean](https://www.digitalocean.com/)
  * Used to host the Linux based deployment
* [Heroku](https://www.heroku.com/)
  * Used to deploy the API
  
---
## Additional Notes <a name="Notes"></a>


To ensure that the code runs properly on your local machine, follow the steps outlined below.

Start by creating a virtual environment in your terminal : 

```
py -3 -m venv <name>
```

After activating the virtual environement, install the dependencies listed in the requirement.txt file.

```
pip install -r requirements.txt
```

A .env file will need to be created on your local machine with the following variables :
```
DATABASE_HOSTNAME
DATABASE_PORT
DATABASE_PASSWORD
DATABASE_NAME
DATABASE_USERNAME
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```
To upgrade to the most recent database version use the following command :
```
alembic upgrade head
```
Finally, for individual testing using pytest, use the following command:
```
pytest tests\<filename.py> -v -s
```

---
## Improvements <a name="Improvements"></a>

Further improvements to this project may include :

* API Design
  * Add cart/checkout options
  * Add user notification options for posts
* Bug Fixes
  * Investigate schema validation inconsistency issues
* Testing
  * Increase the scope of current tests

---
## References <a name="References"></a>

* [Youtube: Project Reference](https://www.youtube.com/watch?v=0sOvCWFmrtA)
* [IBM: What is an API?](https://www.ibm.com/cloud/learn/api)