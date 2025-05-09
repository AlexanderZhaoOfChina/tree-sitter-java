@echo off
setlocal EnableDelayedExpansion

rem 设置JAVA_HOME（如果需要）
rem set JAVA_HOME=C:\Program Files\Java\jdk-11

rem 设置程序目录
set BASE_DIR=%~dp0
set LIB_DIR=%BASE_DIR%lib
set CONF_DIR=%BASE_DIR%config
set LOGS_DIR=%BASE_DIR%logs

echo BASE_DIR: %BASE_DIR%
echo LIB_DIR: %LIB_DIR%
echo CONF_DIR: %CONF_DIR%
echo LOGS_DIR: %LOGS_DIR%

rem 设置Java选项
set JAVA_OPTS=-Xms512m -Xmx1024m

rem 设置类路径
set CLASS_PATH="%BASE_DIR%cvd-1.0-SNAPSHOT.jar;%CONF_DIR%;%LIB_DIR%\*"

echo CLASS_PATH: %CLASS_PATH%

rem 设置主类
set MAIN_CLASS=com.asiainfo.cvd.daemon.CNVDDirectoryWatcherDaemon

rem 启动程序
echo Starting CNVD Directory Watcher...
echo Command: java %JAVA_OPTS% -cp %CLASS_PATH% %MAIN_CLASS%
java %JAVA_OPTS% -cp %CLASS_PATH% %MAIN_CLASS%

endlocal 