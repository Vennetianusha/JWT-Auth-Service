# Secure JWT Authentication Service (RS256)

A secure authentication service that implements **JWT-based authentication using RSA (RS256)** with **refresh tokens**, **bcrypt password hashing**, and **rate limiting**. The application is fully **containerized using Docker and Docker Compose**.

---

## Features

- User Registration & Login
- JWT Access Tokens (RS256)
- Refresh Token mechanism
- Secure password hashing with bcrypt
- Protected API endpoints
- Token verification endpoint
- Logout with refresh token invalidation
- Rate limiting for login endpoint
- Dockerized setup with PostgreSQL

---

## Tech Stack

- Backend: Node.js / Express (or your framework)
- Database: PostgreSQL
- Authentication: JWT (RS256)
- Security: bcrypt
- Containerization: Docker, Docker Compose

---

## Project Structure


.
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── generate-keys.sh
├── test-auth-flow.sh
├── README.md
├── keys/
└── src/


---

## Environment Variables

- Create a `.env` file using `.env.example`.


API_PORT=8080
DATABASE_URL=postgresql://user:password@db:5432/authdb
JWT_PRIVATE_KEY_PATH=./keys/private.pem
JWT_PUBLIC_KEY_PATH=./keys/public.pem


---

## Generate RSA Keys


- chmod +x generate-keys.sh
./generate-keys.sh


- This will create:


keys/private.pem
keys/public.pem


---

## Run the Application

- Start all services using Docker:


docker-compose up --build


---

## API Endpoints

| Method | Endpoint | Description |
|------|------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive tokens |
| POST | `/auth/refresh` | Generate new access token |
| GET | `/api/profile` | Protected user profile |
| GET | `/api/verify-token` | Verify JWT token |
| POST | `/auth/logout` | Logout and revoke refresh token |

---

## Test Authentication Flow

- Run the test script:


chmod +x test-auth-flow.sh
./test-auth-flow.sh


This script tests:
- User registration
- Login
- Protected API access
- Token refresh
- Logout

---

## Security

- JWT signed with **RSA (RS256)**
- **bcrypt** password hashing (10 salt rounds)
- **Access Token:** 15 minutes
- **Refresh Token:** 7 days
- **Rate limiting:** 5 login attempts per minute
