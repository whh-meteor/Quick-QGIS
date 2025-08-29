# -*- coding: utf-8 -*-
"""
QGIS地图显示应用程序 - 重构版
模块化设计，功能分离
"""

import sys
import os

# 设置QGIS环境
from src.config import setup_qgis_environment
setup_qgis_environment()

# ==================== 导入必要的库 ====================
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsApplication

# 导入应用程序模块
from src.app import QGISMapApp

def main():
    """主函数"""
    print("启动QGIS地图应用程序...")
    
    # 创建Qt应用程序
    app = QApplication(sys.argv)
    
    # 初始化QGIS
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    print("QGIS初始化完成")
    
    # 创建并初始化地图应用
    map_app = QGISMapApp()
    if not map_app.initialize():
        print("[ERROR] 应用程序初始化失败")
        return 1
    
    print("应用程序启动完成，进入事件循环...")
    
    # 运行应用程序
    exit_code = app.exec()
    
    # 清理QGIS
    qgs.exitQgis()
    
    print("应用程序退出")
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
