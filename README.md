## Products Reviews API

**Task:**

1. Based on the Django REST framework, create an endpoint API (GET) that will return data in json format of the following content:
   By product id, return information about this product (ASIN, Title) and Reviews of this product with pagination.
   It is advisable to create caching for the GET endpoint.

2. Create a second API endpoint (POST) that will write a new Review for the product (by its id) to the database.

**Stack:**

- Django/Django REST Framework
- Python
- Postgres DB
- Docker

## Installation

- Clone the repository

```bash
git clone https://github.com/ruslan-kornich/product-reviews-django-api.git
cd product-reviews-django-api
cp .env-example .env

```

- Run docker build:

```bash
$ docker-compose up --build
```

- After build create migrations and add products to DB

```bash
$ docker-compose run django python manage.py migrate
```

```bash
$ docker-compose run django python add_products.py
```

- The Web App will run on: http://0.0.0.0:8000/


## Tests:
- Additionally, you can run tests 
```bash
$ docker-compose run django pytest -v
```

## API:

Supports GET, POST, requests for interaction with applications


### API Operation Description

#### GET /api/v1/products/{product_id}

```jsx
// Response
{
    "id": 1,
    "title": "JVC Blue and Red Wireless Water Resistant Pivot Motion Sport Headphone with Locking Ear Fit HA-ET50BTA",
    "asin": "B06X14Z8JP",
    "reviews": [
        {
            "id": 1,
            "title": "Don’t waste your money!!!",
            "review": "Horrible product!!! Hasn’t lasted 8 weeks! Battery does not hold a charge. Do Not Buy This Product!!!!",
            "product": 1
        },
```
}
### POST /api/v1/reviews/create/

```jsx
// Request Body
{
    "title": "string",
    "review": "string",
    "product": <id_product>
}

```

