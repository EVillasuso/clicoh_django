# clicoh_django
> Disclaimer: This public repository is a challenge project for the `ClicOh` company. All the models and data are fictional.

- @author: Carlos Emanuel Villasuso
- LinkedIn: https://www.linkedin.com/in/emanuelvillasuso/
- Contact: ema.villasuso@gmail.com
- Project Date: 2022-03-20 (YYYY-MM-dd).

## Project Definition
### Objectives
The system must contains the models:
- Product
  - id (pk)
  - name
  - price
  - stock

- Order
  - id (pk)
  - date_time

- OrderDetail
  - order (Order)
  - quantity (note)
  - product

### Requirements
- Register products.
- Edit products.
- Detail a product.
- List all products.
- Modify stock of product.
- Register Order with their OrderDetails.
- Edit Order with their OrderDetails.
- Delete Order with their OrderDetails.
- Detail an Order with their OrderDetails.
- List all Orders with their OrderDetails.
- Order class must expode an `get_total() -> Decimal` method.
- Order class must expode an `get_total_usd() -> Decimal` method.
  - To get the current USD price the code have to get the **"Dolar Blue"** value from **DolarSi API**.

### Extra considerations
- This APP must be deployed in Python Django.
- This app must use Django Rest Framework (DRF).
- Register a new order must impact on product's stock (according to the quantities of order details).
- Editing an existing order must impact on product's stock (according to the quantities of previous and new order details).
- Deleting an order must delete their Order Details and also update stock.
- The code must use DRF's `ModelViewSet` and `ModelSerializer`.
- This source code must be published on a public repository (GitHub here).
- The quantities of each OrderDetail product must be > 0.
- Products can't be repeated on the same Order.

## Versioning control and SCM
This proyect was developed using a public GitHub repository.

All the US are fictionally defined in Jira with the code **"NS-100X"**. 

Every Jira US will be declared in their own branch, the branches will be merged to `dev` once the PR is ready to merge.

When the release is ready, the branch `dev` will be merged to `main`.

Main branch must contains only stable builds, the production pipeline of **Heroku** automatically **builds & deploy** every push to `main`.

## Developer Notes
> All my notes and extra considerations will appear here.

### quantity attribute
The `quantity` attribute of `orders.OrderDetail.class` have a *typo* in the original activity. The original model call this attribute `cuantity`. For scalable and integrative reasons, it's a **good practice** to not propagate *typo's* in the API's, so if one app needs the attribute `cuantity` is better to change in that place and avoid returning bad json results in the backend API.

*(This is an small consideration, this attribute can simply be changed to `cuantity` without problems)*

### Endpoint protection
The original activity just says that Json Web Tokens (JWT) must be implemented. There's no explicit task that says if the ModelViewSet can be accessed onyl with an specific permission or only for logged users.

The current implementation require that the user is logged (you have to pass JWT access token), and no extra permissions are required.

### StaticFiles
Heroku runs the `python manage.py collectstatic --noinput` command, so we have to configure the `STATIC_ROOT` setting, even if the proyect didn't use (yet) the `Django StaticFiles` module.

### Heroku Dependencies
In requiremets.txt there are 2 dependencyes added for Heroku:
- gunicorn
- django-heroku

If you run `pip install -r requirements.txt` and that returns errors (like psycopg2 dependency) just comment both dependencies. 

requirements-dev.txt must be a good fit for this issue, but the Heroku AutoDeploy task in Production Pipeline always run only the `requirements.txt`.

This also add an extra import to `settings.py` and an extra line at the end of it. For running in local, you can just comment both.

### Make an Orders app
This is an personal decission. The modularity of the proyect is an important thing for many beneficts. Thats why I put the logic in an `orders` app.
### Decimal fields instead float
To manage fields thats stores currency is better to use `models.DecimalField`. That's why model and serializer (and their inner fuctions) works with python's `Decimal` values.
Float values have issues operating with comma values, making small imperfections in operations. This problem must be avoided in currency fields.
### Transaction atomic
This decorator runs all the transaction in a transaction block. If somewhere in the block the code raises an error, all the transaction will be rolled back.

Is it necesary to maintain the integrity of the data.
### Dockerization
Personally, i whoud prefer to make a docker container thats starts an dockerized instance of PostgreSQL, custom python version and all others extra packages that will needed in a future.
Then run with `sudo docker-compose build` to make initial configurations (such as install requirements).
To start the dockerized proyect just can use `sudo docker-compose up`.
To use `makemigrations` or other tasks to django, we can use `sudo docker ps`, copy the container ID and then `docker exec -it {container_ID} python manage.py makemigrations`.

We can simplyfy some tasks with a `Makefile`.

**Note**: For Heroku issues, docker was removed and not pushed to the code, and so on for the Makefile.

## How To Use: Quickstart guide
### #1: Use in deployment server
Link to Heroku's deployment server: https://clicoh-django-challenge.herokuapp.com/

API usage bellow.
### #2: Use in local
To use in local just clone this repository (make sure to clone always the `main` branch) and run `pip install -r requirements.txt`. The required Python version is 3.9.7 (you can use pyenv virtualenv, or conda).

If you receiving errors, just comment the last 2 dependencies in requirements file, and comment the first and last line of `settings.py` as explained before. 

Then migrate to database with `python manage.py migrate`.

To create a superuser run `python manage.py createsuperuser` and follow the steps in console.

Those steps was only for the first use, when all is set up, you can run the server with `python manage.py makemigrations`.

## API Usage
### Login with JWT (get tokens)
First, you need to login and get yout auth token from JWT:
- local:
  - curl -d "username={username}&password={password}" -X POST http://127.0.0.1:8000/api/JWT/token/
- curl -d "username={username}&password={password}" -X POST https://clicoh-django-challenge.herokuapp.com/api/JWT/token/

*Note: replace {username} and {password} with your own user data.*

*Note 2: In production, there's a custom user for clicoh interviewers, the user data was sent by email*

The response of that command will be an access token and a refresh token. Copy both in a text editor or save it in any place.

#### Refresh token
If your access token is expired, you can refresh it using your refresh token. The URI for refresh JWT tokens is: `/api/JWT/token/refresh/`.
#### Validate token
There's a view for validating tokens if you need, the URI is: `/api/JWT/token/verify/`.

### Accessing endpoints:
The enpoints are defined under the URI's:
- `/api/products/` for Products endpoint
- `/api/orders/` for Order endpoint

Both endpoints requires autentication.

Example for get the list of orders:
- curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ3ODY5MzcwLCJpYXQiOjE2NDc4NjkwNzAsImp0aSI6IjBlOTJjYTEzMzE4MTRlNmVhYjk3ODcxMzI1MDIwZGY0IiwidXNlcl9pZCI6MX0.LJU2XP903lfqoqha0Bp2QdXmNJ8m-aCQBhQYdOCAoCU" https://clicoh-django-challenge.herokuapp.com/api/orders/ 

To use the endpoints always pass at the header options an Authorization with 2 space-separated values: "Bearer {token}" where {token} is your valid access token that you get previously.