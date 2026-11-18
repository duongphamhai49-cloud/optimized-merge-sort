@echo off
setlocal
echo =========================================================================
echo Compiling and executing Benchmark Suite...
echo =========================================================================
cd /d "%~dp0\..\.."
if not exist bin mkdir bin
javac -encoding UTF-8 -d bin src/main/java/com/mergesort/*.java benchmark/*.java
if %ERRORLEVEL% neq 0 (
    echo Compilation failed!
    exit /b %ERRORLEVEL%
)
java -Xms512m -Xmx2048m -cp bin com.mergesort.benchmark.BenchmarkRunner
endlocal
