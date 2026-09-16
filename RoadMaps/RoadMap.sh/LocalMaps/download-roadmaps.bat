@echo off
chcp 65001 >nul
setlocal

set "ROOT=%~dp0"
set "TARGET=%ROOT%roadmaps"

if not exist "%TARGET%" mkdir "%TARGET%"

echo.
echo === Скачивание JSON с roadmap.sh ===
echo.

call :download machine-learning
call :download postgresql-dba
call :download redis
call :download mongodb
call :download elasticsearch
call :download typescript
call :download code-review-best-practices
call :download backend-performance-best-practices
call :download aws
call :download api-security-best-practices
call :download frontend-performance-best-practices
call :download python
call :download sql
call :download ai-engineer
call :download backend

echo.
echo ============================================================
echo  Готово. Файлы в: %TARGET%
echo ============================================================
pause
exit /b

:download
set "SLUG=%~1"
echo   [GET] %SLUG%.json
curl -sSL -o "%TARGET%\%SLUG%.json" "https://roadmap.sh/%SLUG%.json"
exit /b