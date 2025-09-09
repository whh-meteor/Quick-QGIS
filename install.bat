@echo off
cd /d "%~dp0"
echo 当前目录: %CD%

REM 检查main.py是否存在
if not exist main.py (
    echo 错误：main.py 文件不存在！
    exit /b 1
)

REM 设置QGIS环境
set QGIS_PATH=E:\Software\QGIS
set PATH=%QGIS_PATH%\bin;%PATH%

REM 执行PyInstaller命令
"%QGIS_PATH%\bin\python-qgis.bat" -m PyInstaller -w ^
--hidden-import pyproj ^
--collect-binaries=tables ^
--add-data="%QGIS_PATH%\apps\qgis\plugins;qgis\plugins" ^
--add-data="%QGIS_PATH%\apps\Python312\Lib\site-packages\PyQt5\*.pyd;PyQt5" ^
--add-data="%QGIS_PATH%\apps\qt5\plugins\styles;PyQt5\Qt\plugins\styles" ^
--add-data="%QGIS_PATH%\apps\qt5\plugins\iconengines;PyQt5\Qt\plugins\iconengines" ^
--add-data="%QGIS_PATH%\apps\qt5\plugins\imageformats;PyQt5\Qt\plugins\imageformats" ^
--add-data="%QGIS_PATH%\apps\qt5\plugins\platforms;PyQt5\Qt\plugins\platforms" ^
--add-data="%QGIS_PATH%\apps\qt5\plugins\platformthemes;PyQt5\Qt\plugins\platformthemes" ^
--add-data="ui;ui" ^
main.py

if %ERRORLEVEL% NEQ 0 (
    echo 打包失败！
    exit /b 1
)

echo 打包完成！
pause 