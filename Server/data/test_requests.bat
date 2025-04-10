@echo off
echo === REGISTERING USERS WITH UNIQUE HASHED PASSWORDS ===
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user1\", \"email\": \"user1@example.com\", \"password\": \"5b722b307fce6c944905d132691d5e4a2214b7fe92b738920eb3fce3a90420a19511c3010a0e7712b054daef5b57bad59ecbd93b3280f210578f547f4aed4d25\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user2\", \"email\": \"user2@example.com\", \"password\": \"6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4fee5c9735d5a8336e8bd419ec4dd0e7848d3b4248fe13a3a1ab8f38e7ad3356a7\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user3\", \"email\": \"user3@example.com\", \"password\": \"2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881a7b7e29a5d8a8a075a57a2c4a857c5f5953097b0a3c8a1a4f1d5a5d5e5e5e5e\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user4\", \"email\": \"user4@example.com\", \"password\": \"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c922c4d4b5b5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user5\", \"email\": \"user5@example.com\", \"password\": \"0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90b5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user6\", \"email\": \"user6@example.com\", \"password\": \"6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user7\", \"email\": \"user7@example.com\", \"password\": \"d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab355e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user8\", \"email\": \"user8@example.com\", \"password\": \"4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user9\", \"email\": \"user9@example.com\", \"password\": \"4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register
curl -X POST -H "Content-Type: application/json" -d "{ \"username\": \"user10\", \"email\": \"user10@example.com\", \"password\": \"ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5\" }" http://localhost:8000/register

echo.
echo === GET ALL USERS ===
curl http://localhost:8000/users

echo.
echo === GET USER BY ID ===
curl http://localhost:8000/users/5