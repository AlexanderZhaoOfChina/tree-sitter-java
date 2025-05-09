#!/bin/bash

# 设置JAVA_HOME（如果需要）
# export JAVA_HOME=/usr/java/jdk-11

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$SCRIPT_DIR/.."

# 设置程序目录
LIB_DIR="$BASE_DIR/lib"
CONF_DIR="$BASE_DIR/config"
LOGS_DIR="$BASE_DIR/logs"

# 设置Java选项
JAVA_OPTS="-Xms512m -Xmx1024m"

# 设置类路径
CLASS_PATH="$CONF_DIR:$LIB_DIR/*"

# 设置主类
MAIN_CLASS="com.asiainfo.cvd.daemon.CNVDDirectoryWatcherDaemon"

# 启动程序
echo "Starting CNVD Directory Watcher..."
java $JAVA_OPTS -cp "$CLASS_PATH" $MAIN_CLASS 