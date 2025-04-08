@echo off
echo === USER REGISTRATION ===
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"john_doe\", \"email\": \"john@example.com\", \"password\": \"secret\" }" http://localhost:8000/register

echo === USER AUTHORISATION ===
curl -X POST -H "Content-Type: application/json" -d "{ \"email\": \"john@example.com\", \"password\": \"secret\" }" http://localhost:8000/login

echo.
echo === GET ALL USERS ===
curl http://localhost:8000/users

echo.
echo === GET USER BY ID (1) ===
curl http://localhost:8000/users/1

echo.