@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 自动获取版本号
for /f "tokens=2 delims==" %%a in ('findstr "__version__" src\main.py') do (
    set VERSION=%%a
    set VERSION=!VERSION:'=!
    set VERSION=!VERSION: =!
)

if not defined VERSION (
    echo 无法从main.py获取版本号，使用默认1.0.0
    set VERSION=1.0.0
)

:: 清理旧构建
echo [1/5] 正在清理旧构建文件...
if exist bin\ (
    echo 删除bin目录...
    rmdir /s /q bin
    if errorlevel 1 (
        echo 错误: 无法删除bin目录
        pause
        exit /b 1
    )
)

if exist build\ (
    echo 删除build目录...
    rmdir /s /q build
    if errorlevel 1 (
        echo 错误: 无法删除build目录
        pause
        exit /b 1
    )
)

if exist release\ (
    echo 删除release目录...
    rmdir /s /q release
    if errorlevel 1 (
        echo 错误: 无法删除release目录
        pause
        exit /b 1
    )
)
echo 清理完成

:: 安装依赖
echo [2/5] 正在安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)
echo 依赖安装成功

:: 打包程序
echo [3/5] 正在打包应用程序...
pyinstaller --onefile --windowed --name sles --distpath bin src\main.py
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)
echo 打包完成

:: 复制资源文件
echo [4/5] 正在复制资源文件...
if not exist bin\ (
    mkdir bin
)

if not exist bin\conf (
    mkdir bin\conf
) else (
    echo 警告: conf目录已存在，将覆盖现有文件
)

copy /y config.json bin\conf\ > nul
copy /y students.xlsx bin\conf\ > nul

if not exist absence.json (
    echo {"records": []} > absence.json
)
copy /y absence.json bin\conf\ > nul

if not exist bin\bakfiles (
    mkdir bin\bakfiles
)

:: 创建release目录并打包
echo [5/5] 正在创建发布包...
if not exist release (
    mkdir release
)

powershell -Command "Compress-Archive -Path 'bin\*' -DestinationPath 'release\sles_v%VERSION%.zip' -Force"
if errorlevel 1 (
    echo 错误: 创建发布包失败
    pause
    exit /b 1
)

echo 构建完成，版本号: %VERSION%
pause