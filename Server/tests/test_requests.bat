@echo off
cd /d "%~dp0"
 call 1_setup_users.bat
 call 2_users.bat
 call 3_chats.bat