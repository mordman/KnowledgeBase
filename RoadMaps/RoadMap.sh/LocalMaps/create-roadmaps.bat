@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "ROOT=%~dp0"
set "TARGET=%ROOT%roadmaps"

echo.
echo === Создание папки: %TARGET% ===
if not exist "%TARGET%" mkdir "%TARGET%"

set FILES=machine-learning.json^
 ml-engineer-3dqvu.json^
 postgresql-dba.json^
 redis.json^
 mongodb.json^
 elasticsearch.json^
 typescript.json^
 code-review-best-practices.json^
 backend-performance-best-practices.json^
 aws.json^
 api-security-best-practices.json^
 frontend-performance-best-practices.json^
 python.json^
 sql.json^
 c-sharp-he09r.json^
 ai-engineer.json^
 backend.json

echo.
echo === Создание пустых JSON-файлов ===
for %%F in (%FILES%) do (
    if exist "%TARGET%\%%F" (
        echo   [SKIP] %%F
    ) else (
        type nul > "%TARGET%\%%F"
        echo   [OK]   %%F
    )
)

REM ============================================================
REM  Генерация manifest.json со списком карт
REM ============================================================
echo.
echo === Генерация manifest.json ===

set "MANIFEST=%TARGET%\manifest.json"
(
echo {
echo   "maps": [
echo     { "file": "machine-learning.json",                  "title": "Machine Learning" },
echo     { "file": "ml-engineer-3dqvu.json",                 "title": "ML Engineer (AI)" },
echo     { "file": "postgresql-dba.json",                    "title": "PostgreSQL DBA" },
echo     { "file": "redis.json",                             "title": "Redis" },
echo     { "file": "mongodb.json",                           "title": "MongoDB" },
echo     { "file": "elasticsearch.json",                     "title": "Elasticsearch" },
echo     { "file": "typescript.json",                        "title": "TypeScript" },
echo     { "file": "code-review-best-practices.json",        "title": "Code Review" },
echo     { "file": "backend-performance-best-practices.json","title": "Backend Performance" },
echo     { "file": "aws.json",                               "title": "AWS" },
echo     { "file": "api-security-best-practices.json",       "title": "API Security" },
echo     { "file": "frontend-performance-best-practices.json","title": "Frontend Performance" },
echo     { "file": "python.json",                            "title": "Python" },
echo     { "file": "sql.json",                               "title": "SQL" },
echo     { "file": "c-sharp-he09r.json",                     "title": "C# (AI)" },
echo     { "file": "ai-engineer.json",                       "title": "AI Engineer" },
echo     { "file": "backend.json",                           "title": "Backend" }
echo   ]
echo }
) > "%MANIFEST%"

echo   [OK] manifest.json

echo.
echo ============================================================
echo  Готово. Файлы в: %TARGET%
echo ============================================================
pause
endlocal