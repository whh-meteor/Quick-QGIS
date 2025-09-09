# -*- coding: utf-8 -*-
"""
配置文件 - QGIS环境配置
"""

import os
import sys
from .constants import BASEMAP_SOURCES, DEFAULT_EXTENT, SAMPLE_CITIES

# ==================== QGIS环境配置 ====================
# QGIS安装目录 - 请根据实际安装路径修改
QGIS_PREFIX_PATH = r"E:\Software\QGIS"
from qgis.PyQt.QtCore import QCoreApplication

def setup_qgis_environment():
    """设置QGIS环境变量和路径"""
    # 注意：QGIS环境配置已注释，因为当前版本可能不需要手动设置
    # 如果需要手动配置QGIS环境，请取消注释以下代码并修改路径
    
    # os.environ['QGIS_PREFIX_PATH'] = QGIS_PREFIX_PATH
    # os.environ['QGIS_PLUGINPATH'] = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "plugins")
    # os.environ['QT_PLUGIN_PATH'] = os.path.join(QGIS_PREFIX_PATH, "apps", "Qt6", "plugins")
    # os.environ['GDAL_DATA'] = os.path.join(QGIS_PREFIX_PATH, "share", "gdal")
    # os.environ['PROJ_LIB'] = os.path.join(QGIS_PREFIX_PATH, "share", "proj")
    # os.environ['PATH'] = (
    #     os.path.join(QGIS_PREFIX_PATH, "bin") + ";" +
    #     os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "bin") + ";" +
    #     os.path.join(QGIS_PREFIX_PATH, "apps", "Qt6", "bin") + ";" +
    #     os.environ['PATH']
    # )
    # qgis_python = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python")
    # if qgis_python not in sys.path:
    #     sys.path.append(qgis_python)
    # QCoreApplication.addLibraryPath(os.environ['QGIS_PLUGINPATH'])
    # QCoreApplication.addLibraryPath(os.environ['QT_PLUGIN_PATH'])
    
    pass  # 当前版本使用默认QGIS环境配置
