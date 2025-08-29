# -*- coding: utf-8 -*-
"""
UI管理模块 - 负责主窗口和QML界面的创建
"""

import os
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QLabel
try:
    from qgis.PyQt.QtQuickWidgets import QQuickWidget
    QML_AVAILABLE = True
except ImportError:
    try:
        from PyQt5.QtQuickWidgets import QQuickWidget
        QML_AVAILABLE = True
    except ImportError:
        try:
            from PyQt6.QtQuickWidgets import QQuickWidget
            QML_AVAILABLE = True
        except ImportError:
            QML_AVAILABLE = False
            print("[WARN] QQuickWidget不可用，将使用备用界面")

from qgis.PyQt.QtCore import QUrl
from qgis.gui import QgsMapCanvas
from .bridge import QmlBridge

class UIManager:
    """UI管理器"""
    
    def __init__(self, app_ref):
        self.app_ref = app_ref
        self.window = None
        self.canvas = None
        self.bridge = None
        self.qml_widget = None
    
    def create_main_window(self):
        """创建主窗口和地图画布"""
        print("正在创建主窗口...")
        
        # 创建主窗口
        self.window = QWidget()
        self.window.setWindowTitle("QGIS地图显示 - 重构版")
        self.window.resize(1000, 700)
        
        # 创建垂直布局
        layout = QVBoxLayout(self.window)
        
        # 创建QML界面
        self._create_qml_interface(layout)
        
        # 创建地图画布
        self._create_map_canvas(layout)
        
        # 添加状态标签
        self._create_status_label(layout)
        
        # 显示窗口
        self.window.show()
        
        print("主窗口创建完成")
        return self.window, self.canvas
    
    def _create_qml_interface(self, layout):
        """创建QML界面"""
        if not QML_AVAILABLE:
            print("[INFO] QML不可用，使用备用界面")
            self._create_fallback_interface(layout)
            return
            
        try:
            # 创建 QQuickWidget，加载 QML 界面
            self.qml_widget = QQuickWidget(self.window)
            self.qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
            
            # 设置QML源文件路径
            qml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "main.qml")
            
            # 检查QML文件是否存在
            if not os.path.exists(qml_path):
                print(f"[WARN] QML文件不存在: {qml_path}")
                self._create_fallback_interface(layout)
                return
            
            # 创建桥接对象
            self.bridge = QmlBridge(self.app_ref)
            self.qml_widget.engine().rootContext().setContextProperty("qgisBridge", self.bridge)
            
            # 加载QML文件
            self.qml_widget.setSource(QUrl.fromLocalFile(qml_path))
            
            layout.addWidget(self.qml_widget)
            print("QML界面创建完成")
            
        except Exception as e:
            print(f"[ERROR] 创建QML界面失败: {e}")
            # 如果QML加载失败，创建一个简单的按钮界面
            self._create_fallback_interface(layout)
    
    def _create_fallback_interface(self, layout):
        """创建备用界面（当QML加载失败时）"""
        from qgis.PyQt.QtWidgets import QHBoxLayout, QPushButton
        
        # 创建水平布局容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # 创建按钮
        osm_btn = QPushButton("OSM")
        gaode_btn = QPushButton("高德")
        arcgis_btn = QPushButton("ArcGIS")
        refresh_btn = QPushButton("刷新")
        reset_btn = QPushButton("重置")
        
        # 连接信号
        osm_btn.clicked.connect(lambda: self.app_ref.load_basemap_by("OSM"))
        gaode_btn.clicked.connect(lambda: self.app_ref.load_basemap_by("GAODE"))
        arcgis_btn.clicked.connect(lambda: self.app_ref.load_basemap_by("ARCGIS"))
        refresh_btn.clicked.connect(lambda: self.app_ref.refresh_canvas())
        reset_btn.clicked.connect(lambda: self.app_ref.reset_canvas_extent())
        
        # 添加到布局
        button_layout.addWidget(osm_btn)
        button_layout.addWidget(gaode_btn)
        button_layout.addWidget(arcgis_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        
        layout.addWidget(button_container)
        print("备用界面创建完成")
    
    def _create_map_canvas(self, layout):
        """创建地图画布"""
        try:
            # 创建地图画布
            self.canvas = QgsMapCanvas(self.window)
            layout.addWidget(self.canvas)
            print("地图画布创建完成")
            
        except Exception as e:
            print(f"[ERROR] 创建地图画布失败: {e}")
            self.canvas = None
    
    def _create_status_label(self, layout):
        """创建状态标签"""
        try:
            self.status_label = QLabel("正在加载地图...")
            layout.addWidget(self.status_label)
            print("状态标签创建完成")
            
        except Exception as e:
            print(f"[ERROR] 创建状态标签失败: {e}")
    
    def update_status(self, message: str):
        """更新状态信息"""
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.setText(message)
    
    def refresh_canvas(self):
        """刷新画布"""
        if self.canvas:
            self.canvas.refresh()
    
    def get_bridge(self):
        """获取桥接对象"""
        return self.bridge
