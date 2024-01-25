# Assignment Project

## Overview

This project is a Django-based web application that involves user registration, stock data management, and financial transactions. The goal is to implement various endpoints, integrate Redis for caching, use Swagger for documentation, and provide a Docker setup.

## Table of Contents

- [Database](#database)
- [Endpoints](#endpoints)
- [Instructions](#instructions)
- [Unit Tests](#unit-tests)
- [Docker Setup](#docker-setup)

## Database

### Users Table

- user_id
- username
- balance

### StockData Table

- ticker
- open_price
- close_price
- high
- low
- volume
- timestamp

### Transactions Table

- transaction_id
- user_id
- ticker
- transaction_type (buy/sell)
- transaction_volume
- transaction_price
- timestamp

## Endpoints

- **POST /users/:** Register a new user with a username and initial balance.
- **GET /users/{username}/:** Retrieve user data. Utilize Redis for caching.
- **POST /stocks/:** Ingest stock data and store it in the Postgres database.
- **GET /stocks/:** Retrieve all stock data. Use Redis for caching.
- **GET /stocks/{ticker}/:** Retrieve specific stock data. Employ Redis for caching.
- **POST /transactions/:** Post a new transaction. Calculate transaction_price based on the current stock price and update the user's balance.
- **GET /transactions/{user_id}/:** Retrieve all transactions of a specific user.


## Basic Setup to Get Started

### 1. Create a Virtual Environment:
Open the VS CODE terminal and navigate to the project directory. In the terminal, enter:
- On Windows: `python -m venv venv`
- On Linux/macOS: `python3 -m venv venv`

### 2. Activate the Virtual Environment:
On Windows: `.\venv\Scripts\activate`
On Linux/macOS: `source venv/bin/activate`
Your terminal prompt should change, indicating that the virtual environment is now active.

### 3. Install Django:
While the virtual environment is active, install Django using pip:
pip install django

### 4. Create a Django Project:
django-admin startproject your_project_name
This will create a new directory with your project's name. Navigate into this directory.
cd your_project_name

### 5. Create a Django App:
Inside your project directory, create a Django app.
python manage.py startapp your_app_name


### 6. Install Required Packages:
Install any additional packages you need. For example, you may want to install djangorestframework:
pip install djangorestframework


### 7. Apply Migrations:
Apply migrations to set up your database.
python manage.py migrate


### 8. Run the Development Server:
Start the development server to see if everything is working.
python manage.py runserver
Visit http://localhost:8000 in your web browser to see the default Django welcome page.









## Instructions Implemented

1. Build the Given data models and Creative the given API Endpoints. 
2. Utilize Redis for caching user and stock data to reduce database load.
3. Write unit tests for the implemented API Endpoints.
4. Integrate Swagger. 
5. Document all steps, APIs, data models, setup guide, and assumptions in the GitHub repository README.md file.
6. Integrate your project with Docker and run through Docker Container.  


## Docker 

To run the project with Docker, follow these steps:
Note: Put all your dependencies in requirements.txt file so that can be installed for stable versioning across docker container. 

  docker-compose build


## Run the Project
After we have build the docker container using "docker-compose build"
Run "docker-compose up"
to start the API and Test through postman. 


Note : It is important for virtual environment to be activated for this project to run. 
if not activated run "venv/scrips/activate" in the terminal. 
