## Description

This project is a simple web application built using **FastAPI**, and it uses **SQLite** as the database. It is containerized using **Docker** for easy development and deployment. The project provides API endpoints to manage organizations, admin login, and dynamic database creation.

### Key Features:

- FastAPI-based RESTful API.
- Admin authentication with JWT tokens.
- SQLite for lightweight database management.
- Dynamic database creation for each organization.
- Dockerize for easy containerization and deployment.

## Components

1. **FastAPI**: The backend framework used to create and expose the APIs.
2. **SQLite**: The database used for storing organization and admin data.
3. **Docker**: The containerization tool used to build, run, and deploy the project.
4. **JWT Authentication**: Used for admin login and access control.
5. **DB Manager**: Manages the dynamic creation of SQLite databases for each organization.

## Local Installation and Setup

#### Run locally

1. **Clone the repository:**

   ```bash
   git clone git@github.com:Raman5837/navatech.git
   cd navatech
   ```

2. **Install the dependencies**

   ```
   python -m pip install -r requirements.txt
   ```

3. **Run the server**

   ```
   uvicorn app.main:app --reload
   ```

#### Run using Docker

1. **Clone the repository:**

   ```bash
   git clone git@github.com:Raman5837/navatech.git
   cd navatech
   ```

2. **Run the server**

   ```
   docker-compose up --build
   ```
