echo.
echo === CREATE CHAT BETWEEN USER 1 AND USER 2 (FIRST ATTEMPT) ===
curl -X POST -H "Content-Type: application/json" -d "{ \"user1_id\": 1, \"user2_id\": 2 }" http://localhost:8000/chats/start

echo.
echo === CREATE CHAT BETWEEN USER 1 AND USER 2 (SECOND ATTEMPT - SHOULD RETURN EXISTING CHAT) ===
curl -X POST -H "Content-Type: application/json" -d "{ \"user1_id\": 1, \"user2_id\": 2 }" http://localhost:8000/chats/start

echo.
echo === CREATE CHAT BETWEEN USER 2 AND USER 1 (SHOULD RETURN EXISTING CHAT) ===
curl -X POST -H "Content-Type: application/json" -d "{ \"user1_id\": 2, \"user2_id\": 1 }" http://localhost:8000/chats/start

echo.
echo === CREATE CHAT BETWEEN USER 3 AND USER 1 ===
curl -X POST -H "Content-Type: application/json" -d "{ \"user1_id\": 3, \"user2_id\": 1 }" http://localhost:8000/chats/start

echo.
echo === GET ALL CHATS FOR USER 1 ===
curl -X GET -H "Content-Type: application/json" -d "{ \"user_id\": 1 }" http://localhost:8000/chats

echo.
echo === GET ALL CHATS FOR USER 3 ===
curl -X GET -H "Content-Type: application/json" -d "{ \"user_id\": 3 }" http://localhost:8000/chats

echo.
echo === DELETE CHAT BETWEEN USER 3 AND USER 1 ===
curl -X DELETE -H "Content-Type: application/json" -d "{ \"user1_id\": 3, \"user2_id\": 1 }" http://localhost:8000/chats

echo.
echo === DELETE CHAT BETWEEN USER 3 AND USER 1 (SHOULD RETURN EXISTING CHAT) ===
curl -X DELETE -H "Content-Type: application/json" -d "{ \"user1_id\": 3, \"user2_id\": 1 }" http://localhost:8000/chats

echo.
echo === VERIFY CHAT BY USER 3 ===
curl -X GET -H "Content-Type: application/json" -d "{ \"user_id\": 3 }" http://localhost:8000/chats

echo.
echo === VERIFY CHAT BY USER 1 ===
curl -X GET -H "Content-Type: application/json" -d "{ \"user_id\": 1 }" http://localhost:8000/chats
