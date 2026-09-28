@echo off
setlocal EnableExtensions

REM Folder to zip, and output archive (relative to where you run this .bat)
set "SRC=docs"
set "OUT=lecture_notes.zip"

REM Check tools on PATH (tar ships with Windows 10 and later)
where tar >nul 2>&1 || (echo [ERROR] tar not found in PATH.& exit /b 1)

if not exist "%SRC%\" (
  echo [ERROR] Folder "%SRC%" not found. Nothing to do.
  exit /b 1
)

if exist "%OUT%" del /q "%OUT%"

REM -a picks the format from the extension (.zip)
tar -a -c -f "%OUT%" "%SRC%"
if errorlevel 1 (
  echo [FAIL] Could not create %OUT%
  exit /b 1
)

echo [OK]  Created %OUT% from %SRC%\
