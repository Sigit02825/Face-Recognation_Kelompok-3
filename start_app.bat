@echo off
title Aplikasi Face Recognition FaceNet512
color 0b
echo ======================================================================
echo    APLIKASI PENGENALAN WAJAH (FACE RECOGNITION) FACENET512 + RETINAFACE
echo    Berdasarkan Eksperimen Google Colab & Dataset Mahasiswa Udinus
echo ======================================================================
echo.
echo [1/2] Memeriksa instalasi Node.js...
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js tidak ditemukan! Harap pasang Node.js terlebih dahulu.
    pause
    exit /b
)

echo [2/2] Menjalankan server aplikasi di http://localhost:3000 ...
echo.
echo ======================================================================
echo  Server aktif! Buka tautan berikut di peramban (browser) Anda:
echo  >>>  http://localhost:3000  <<<
echo ======================================================================
echo  Tekan Ctrl+C untuk menghentikan server.
echo.

start http://localhost:3000
node server.js
pause
