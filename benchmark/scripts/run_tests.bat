@echo off
chcp 65001 > nul
setlocal
echo =========================================================================
echo Đang biên dịch mã nguồn và chạy Bộ Kiểm Thử Đúng Đắn (70 Tests)...
echo =========================================================================
cd /d "%~dp0\..\.."
if not exist bin mkdir bin
javac -encoding UTF-8 -d bin src/main/java/com/mergesort/*.java src/test/java/com/mergesort/*.java
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Quá trình biên dịch thất bại!
    exit /b %ERRORLEVEL%
)
java -cp bin com.mergesort.SortCorrectnessTest
endlocal
