@echo off
chcp 65001 > nul
setlocal
echo =========================================================================
echo Đang biên dịch và thực thi Toàn Bộ Framework Đo Đạc Benchmark (3000 lượt)...
echo =========================================================================
cd /d "%~dp0\..\.."
if not exist bin mkdir bin
javac -encoding UTF-8 -d bin src/main/java/com/mergesort/*.java benchmark/*.java
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Quá trình biên dịch benchmark thất bại!
    exit /b %ERRORLEVEL%
)
java -Xms512m -Xmx2048m -cp bin com.mergesort.benchmark.BenchmarkRunner
endlocal
