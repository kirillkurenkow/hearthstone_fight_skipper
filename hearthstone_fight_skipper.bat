@echo off
chcp 65001 >nul
:: ======================= CONFIG ======================
set "RULE_NAME=hs_fight_skip"
set "HS_PATH=D:\Battle.net\Hearthstone\Hearthstone.exe"
set "DURATION=5"
:: =====================================================

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Запрос прав администратора...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title Hearthstone Battlegrounds Skip
cls

:loop
echo Нажмите ЛЮБУЮ КЛАВИШУ для переподключения (или Ctrl+C для выхода)...
pause >nul

:: Disconnect
echo [%time%] Отключение ...
netsh advfirewall firewall add rule name="%RULE_NAME%" dir=out action=block program="%HS_PATH%" >nul

:: Sleep
echo Ожидание %DURATION% секунд...
timeout /t %DURATION% /nobreak >nul

:: Connect
echo [%time%] Подключение ...
netsh advfirewall firewall delete rule name="%RULE_NAME%" >nul

goto loop
