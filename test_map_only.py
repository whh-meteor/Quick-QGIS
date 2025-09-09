#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试地图画布显示 - 不加载QML
"""

import sys
import os

# 设置QGIS环境
from src.config import setup_qgis_environment
setup_qgis_environment()

from qgis.PyQt.QtWidgets import QApplication, QWidget
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsApplication, QgsCoordinateReferenceSystem
from qgis.gui import QgsMapCanvas
from src.layer_manager import LayerManager

def test_map_canvas_only():
    """测试地图画布显示（不加载QML）"""
    print("开始测试地图画布显示...")
    
    # 创建Qt应用程序
    app = QApplication(sys.argv)
    
    # 初始化QGIS
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    # 创建主窗口
    window = QWidget()
    window.setWindowTitle("地图画布测试 - 无QML")
    window.resize(1200, 800)
    window.setStyleSheet("background-color: #1a1a1a;")
    
    # 创建地图画布
    canvas = QgsMapCanvas(window)
    canvas.setGeometry(0, 0, window.width(), window.height())
    canvas.setStyleSheet("border: none; background-color: #1a1a1a;")
    canvas.setCanvasColor(QColor("#1a1a1a"))
    
    # 设置坐标系统
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    canvas.setDestinationCrs(crs)
    
    # 创建图层管理器并添加数据
    layer_manager = LayerManager(canvas)
    layer_manager.add_sample_vector_data()
    layer_manager.set_canvas_extent()
    
    # 加载OSM底图
    layer_manager.load_basemap_by("OSM")
    
    # 显示窗口
    window.show()
    
    print("地图画布测试窗口已显示")
    print(f"画布大小: {canvas.size().width()} x {canvas.size().height()}")
    print(f"画布背景色: {canvas.canvasColor().name()}")
    print(f"图层数量: {len(canvas.layers())}")
    
    # 刷新画布
    canvas.refresh()
    
    # 运行应用程序
    exit_code = app.exec()
    
    # 清理QGIS
    qgs.exitQgis()
    
    print("测试完成")
    return exit_code

if __name__ == "__main__":
    exit_code = test_map_canvas_only()
    sys.exit(exit_code)