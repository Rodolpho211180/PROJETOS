@echo off
title Simulador de Estresse - Níveis Ajustáveis
color 0B
setlocal enabledelayedexpansion

:MENU
cls
echo ============================================
echo      SIMULADOR DE ESTRESSE CONTROLADO
echo ============================================
echo 1. Estressar CPU
echo 2. Estressar RAM
echo 3. Estressar Disco
echo 4. Estressar TUDO (CPU + RAM + Disco)
echo 5. Parar todos os testes
echo 0. Sair
echo ============================================
set /p opcao=Escolha uma opcao: 

if "%opcao%"=="1" goto SET_CPU
if "%opcao%"=="2" goto SET_RAM
if "%opcao%"=="3" goto SET_DISCO
if "%opcao%"=="4" goto SET_TODOS
if "%opcao%"=="5" goto PARAR
if "%opcao%"=="0" exit
goto MENU

:SET_CPU
set /p nivel=Digite o nivel de estresse de CPU (10-100): 
set /a cpuloop=nivel / 10
goto CPU

:SET_RAM
set /p nivel=Digite o nivel de estresse de RAM (10-100): 
set /a ramloop=nivel / 10
goto RAM

:SET_DISCO
set /p nivel=Digite o nivel de estresse de Disco (10-100): 
set /a discoloop=nivel / 10
goto DISCO

:SET_TODOS
set /p nivel=Digite o nivel de estresse total (10-100): 
set /a cpuloop=nivel / 10
set /a ramloop=nivel / 10
set /a discoloop=nivel / 10
call :CPU
call :RAM
call :DISCO
goto MENU

:CPU
echo Iniciando estresse de CPU: %nivel%% (%cpuloop% processos)...
for /l %%i in (1,1,%cpuloop%) do (
    powershell -WindowStyle Hidden -Command "Start-Process powershell -WindowStyle Hidden -ArgumentList 'while ($true) {}'"
)
timeout /t 2 >nul
goto MENU

:RAM
echo Iniciando estresse de RAM: %nivel%% (%ramloop% processos)...
for /l %%i in (1,1,%ramloop%) do (
    powershell -WindowStyle Hidden -Command "Start-Process powershell -WindowStyle Hidden -ArgumentList '$a = @(); while ($true) { $a += (\"A\" * 1000000); Start-Sleep -Milliseconds 100 }'"
)
timeout /t 2 >nul
goto MENU

:DISCO
echo Iniciando estresse de Disco: %nivel%% (%discoloop% arquivos)...
set "folder=%TEMP%\stress_disk"
mkdir "%folder%" >nul 2>&1
for /l %%i in (1,1,%discoloop%) do (
    powershell -WindowStyle Hidden -Command "Start-Process powershell -WindowStyle Hidden -ArgumentList 'while ($true) { Set-Content -Path \"%folder%\file%%i.txt\" -Value (\"A\" * 10000000) -Force }'"
)
timeout /t 2 >nul
goto MENU

:PARAR
echo Encerrando todos os processos de estresse...
taskkill /f /im powershell.exe >nul 2>&1
rd /s /q "%TEMP%\stress_disk" >nul 2>&1
echo Todos os testes foram encerrados.
pause
goto MENU
