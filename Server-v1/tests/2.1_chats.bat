echo.
echo === CREATE GROUP CHAT NAMED "Test Group" ===
curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"Test Group\" }" http://localhost:8000/chats
