# -*- coding: utf-8 -*-
"""
UI管理模块 - 负责主窗口和QML界面的创建
"""

import os
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QLabel

from PyQt5.QtQuickWidgets import QQuickWidget
QML_AVAILABLE = True
 
from qgis.PyQt.QtCore import QUrl
from qgis.gui import QgsMapCanvas
from .bridge import QmlBridge
from .constants import DEFAULT_WINDOW_TITLE

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
        # 显示启动画面
        self._show_splash_screen()
        # 创建主窗口
        self.window = QWidget()
        self.window.setWindowTitle(DEFAULT_WINDOW_TITLE)
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
        # 立即关闭启动画面
        self.close_splash_screen()
        
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
            self.qml_widget.setMinimumHeight(80)   # 设置最小高度
            self.qml_widget.setMaximumHeight(100)  # 设置最大高度
            
            # 设置QML源文件路径
            qml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "main.qml")
            
            # 检查QML文件是否存在
            if not os.path.exists(qml_path):
                print(f"[WARN] QML文件不存在: {qml_path}")
                self._create_fallback_interface(layout)
                return
            
            # 创建桥接对象
            self.bridge = QmlBridge(self.app_ref)
            #setContextProperty：将Python对象暴露给QML
            self.qml_widget.engine().rootContext().setContextProperty("qgisBridge", self.bridge)
            
            # 加载QML文件
            self.qml_widget.setSource(QUrl.fromLocalFile(qml_path))
            
            # 检查QML加载状态
            if self.qml_widget.status() == QQuickWidget.Error:
                print(f"[ERROR] QML加载错误: {self.qml_widget.errors()}")
                self._create_fallback_interface(layout)
                return
            
            layout.addWidget(self.qml_widget)
            print(f"QML界面创建完成，状态: {self.qml_widget.status()}")
            print(f"QML文件路径: {qml_path}")
            print(f"QML文件存在: {os.path.exists(qml_path)}")
            
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
    def _show_splash_screen(self):
        """显示启动画面"""
        try:
            from PyQt5.QtWidgets import QSplashScreen
            from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
            from PyQt5.QtCore import Qt, QTimer
            import os
            
            # 获取背景图片路径
            background_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         "assets", "images", "first-screen.png")
            
            # 创建启动画面
            splash_pixmap = QPixmap(800, 600)  # 增大尺寸以匹配QGIS风格
            
            # 尝试加载背景图片
            if os.path.exists(background_path):
                background_pixmap = QPixmap(background_path)
                if not background_pixmap.isNull():
                    # 缩放背景图片以填充启动画面
                    scaled_background = background_pixmap.scaled(
                        splash_pixmap.size(), 
                        Qt.KeepAspectRatioByExpanding, 
                        Qt.SmoothTransformation
                    )
                    # 将背景图片绘制到启动画面上
                    painter = QPainter(splash_pixmap)
                    painter.drawPixmap(0, 0, scaled_background)
                else:
                    # 如果图片加载失败，使用默认背景
                    splash_pixmap.fill(QColor(0, 100, 0))  # 深绿色背景
                    painter = QPainter(splash_pixmap)
            else:
                # 如果没有背景图片，使用默认背景
                splash_pixmap.fill(QColor(0, 100, 0))  # 深绿色背景
                painter = QPainter(splash_pixmap)
            
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 添加半透明遮罩层，让文字更清晰
            painter.fillRect(splash_pixmap.rect(), QColor(0, 0, 0, 100))
            
            # 绘制主标题 - 大号白色粗体
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Microsoft YaHei", 26, QFont.Bold))
            main_title_rect = splash_pixmap.rect().adjusted(0, 150, 0, -200)
            painter.drawText(main_title_rect, Qt.AlignCenter, 
                           "海洋移动监测路径规划系统")
            
            # 绘制副标题 - 中等白色字体
            painter.setFont(QFont("Microsoft YaHei", 18, QFont.Normal))
            subtitle_rect = splash_pixmap.rect().adjusted(0, 220, 0, -150)
            painter.drawText(subtitle_rect, Qt.AlignCenter, "v1.0.0")
            
            painter.end()
            
            # 创建启动画面
            self.splash = QSplashScreen(splash_pixmap)
            self.splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
            self.splash.show()
            
            # 底部状态消息 - 白色文字
            self.splash.showMessage("正在初始化系统...", Qt.AlignBottom | Qt.AlignCenter, 
                                  QColor(255, 255, 255))
            
            print("启动画面显示成功")
            

        except Exception as e:
            print(f"显示启动画面失败: {e}")
            self.splash = None
    
    def close_splash_screen(self):
        """关闭启动画面"""
        try:
            if hasattr(self, 'splash') and self.splash:
                self.splash.close()
                self.splash = None
                print("启动画面已关闭")
        except Exception as e:
            print(f"关闭启动画面失败: {e}")
    

