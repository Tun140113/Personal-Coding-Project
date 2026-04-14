@echo off
REM Build chrome_lock.cpp into chrome_lock.exe using MSVC or MinGW g++.

cd /d "%~dp0"
SETLOCAL ENABLEDELAYEDEXPANSION

REM Option 1: Use user-defined MinGW path if set.
IF DEFINED MINGW_HOME (
    IF EXIST "%MINGW_HOME%\bin\g++.exe" (
        set "MINGW_GPP=%MINGW_HOME%\bin\g++.exe"
    )
)

REM Option 2: Try Downloads\mingw64 if it exists.
IF NOT DEFINED MINGW_GPP (
    IF EXIST "%USERPROFILE%\Downloads\mingw64\bin\g++.exe" (
        set "MINGW_GPP=%USERPROFILE%\Downloads\mingw64\bin\g++.exe"
    )
)

REM Option 3: Use g++ from PATH.
IF NOT DEFINED MINGW_GPP (
    where g++.exe >nul 2>nul && set "MINGW_GPP=g++.exe"
)

REM Option 4: Use cl.exe if available.
IF NOT DEFINED MINGW_GPP IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio" (
    echo Building with MSVC...
    cl /EHsc /std:c++17 chrome_lock.cpp /link /OUT:chrome_lock.exe
    IF ERRORLEVEL 1 (
        echo MSVC build failed with error %ERRORLEVEL%.
        exit /b %ERRORLEVEL%
    ) ELSE (
        echo Build succeeded: chrome_lock.exe
        ENDLOCAL
        exit /b 0
    )
)

IF DEFINED MINGW_GPP (
    echo Building with MinGW: !MINGW_GPP!
    "!MINGW_GPP!" -std=c++17 -municode -mwindows -static-libgcc -static-libstdc++ chrome_lock.cpp -o chrome_lock.exe
    IF ERRORLEVEL 1 (
        echo MinGW build failed with error !ERRORLEVEL!.
        exit /b !ERRORLEVEL!
    ) ELSE (
        echo Build succeeded: chrome_lock.exe
        ENDLOCAL
        exit /b 0
    )
)

echo No supported compiler found.
echo If you have MinGW installed in %USERPROFILE%\Downloads\mingw64, set MINGW_HOME to that folder or add its bin directory to PATH.
echo Example: setx MINGW_HOME "%USERPROFILE%\Downloads\mingw64"
exit /b 1
