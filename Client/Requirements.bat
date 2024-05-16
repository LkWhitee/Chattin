DOS
@echo off

rem Controlla se Python è installato
rem Se non lo è, scarica e installa Python 3.10
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python non è installato. Scaricando e installando Python 3.10...
    curl -sSL https://www.python.org/ftp/python/3.10.2/Python-3.10.2.exe | powershell -NoProfile -ExecutionPolicy Bypass -EncodedCommand 'Start-Process -FilePath "Python-3.10.2.exe" -Args "/InstallNow /ForAllUsers /AgreeToPLM"'
    PAUSE
    rem Attendere il completamento dell'installazione di Python
    echo Attendere il completamento dell'installazione di Python...
    timeout /t 60
)

rem Installa la libreria Requests
pip install requests
7
echo Libreria Requests installata correttamente.