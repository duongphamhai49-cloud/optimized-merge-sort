@echo off
setlocal
echo =========================================================================
echo Compiling project and running Unit Correctness Tests...
echo =========================================================================
cd /d "%~dp0\..\.."
if not exist bin mkdir bin
javac -encoding UTF-8 -d bin src/main/java/com/mergesort/*.java src/test/java/com/mergesort/*.java
if %ERRORLEVEL% neq 0 (
    echo Compilation failed!
    exit /b %ERRORLEVEL%
)
java -cp bin com.mergesort.SortCorrectnessTest
endlocal
