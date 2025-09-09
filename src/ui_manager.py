# -*- coding: utf-8 -*-
"""
UI管理模块 - 负责主窗口和QML界面的创建
"""

import os
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout

from PyQt5.QtQuick import QQuickView, QQuickWindow
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import Qt
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
        self.qml_view = None
        self.qml_container = None
        self.qml_overlay = None
    
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
        
        # 创建地图画布
        self._create_map_canvas(layout)

        # 在地图之上创建QML控制叠加层
        self._create_qml_overlay()
        
        # 显示窗口
        self.window.show()
        # 立即关闭启动画面
        self.close_splash_screen()
        
        print("主窗口创建完成")
        return self.window, self.canvas
    
    def _create_qml_interface(self, layout):
        """创建QML界面"""
        if not QML_AVAILABLE:
            print("[INFO] QML不可用，请启用QML环境后重试")
            return
            
        try:
            # QQuickView + createWindowContainer 更稳定，避免与OpenGL原生窗口的堆叠问题
            self.qml_view = QQuickView()
            # 创建桥接对象并暴露给QML
            self.bridge = QmlBridge(self.app_ref)
            self.qml_view.rootContext().setContextProperty("qgisBridge", self.bridge)

            # 设置QML源文件路径
            qml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "main.qml")
            if not os.path.exists(qml_path):
                print(f"[ERROR] QML文件不存在: {qml_path}")
                return

            self.qml_view.setSource(QUrl.fromLocalFile(qml_path))

            if self.qml_view.status() == QQuickView.Error:
                print(f"[ERROR] QML加载错误: {self.qml_view.errors()}")
                return

            # 将 QQuickView 包装为 QWidget 容器
            from qgis.PyQt.QtWidgets import QWidget as QtWidget
            self.qml_container = QtWidget.createWindowContainer(self.qml_view, self.window)
            self.qml_container.setMinimumHeight(60)
            self.qml_container.setMaximumHeight(60)
            self.qml_container.setFocusPolicy(False)

            layout.addWidget(self.qml_container)
            print("QML界面创建完成 (QQuickView + createWindowContainer)")
            print(f"QML文件路径: {qml_path}")
            
        except Exception as e:
            print(f"[ERROR] 创建QML界面失败: {e}")
            # 不再创建备用界面，保持纯QML控制
            return
    
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

    def _create_qml_overlay(self):
        """创建叠加在地图上的QML控制层"""
        try:
            if self.canvas is None:
                return

            # 使用 QQuickWidget 作为透明叠加层
            # 启用默认 Alpha 缓冲，保证透明像素不会被黑底替代
            try:
                QQuickWindow.setDefaultAlphaBuffer(True)
            except Exception:
                pass
            self.qml_overlay = QQuickWidget(self.window)
            self.qml_overlay.setResizeMode(QQuickWidget.SizeRootObjectToView)
            self.qml_overlay.setAttribute(Qt.WA_TranslucentBackground)
            self.qml_overlay.setClearColor(Qt.transparent)
            # 避免被其他子部件覆盖，同时确保自身背景不绘制
            self.qml_overlay.setAttribute(Qt.WA_AlwaysStackOnTop)
            try:
                self.qml_overlay.setStyleSheet("background: transparent;")
            except Exception:
                pass

            # 桥接对象（与应用共享）
            if self.bridge is None:
                self.bridge = QmlBridge(self.app_ref)
            self.qml_overlay.rootContext().setContextProperty("qgisBridge", self.bridge)

            # 作为画布子组件并置顶
            self.qml_overlay.setParent(self.canvas)
            self.qml_overlay.raise_()

            # 加载 QML（顶部控制条）
            qml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "main.qml")
            if not os.path.exists(qml_path):
                print(f"[WARN] 叠加QML文件不存在: {qml_path}")
                return
            self.qml_overlay.setSource(QUrl.fromLocalFile(qml_path))

            # 同步几何尺寸到画布顶部 60 像素
            def _sync_overlay_geometry():
                if self.canvas and self.qml_overlay:
                    self.qml_overlay.setGeometry(0, 0, self.canvas.width(), 60)
                    self.qml_overlay.raise_()

            _sync_overlay_geometry()

            # 监听画布尺寸变化
            original_resize = getattr(self.canvas, 'resizeEvent', None)

            def wrapped_resize(event):
                try:
                    if callable(original_resize):
                        original_resize(event)
                finally:
                    _sync_overlay_geometry()

            self.canvas.resizeEvent = wrapped_resize

            print("QML叠加控制层创建完成，位于地图之上")

        except Exception as e:
            print(f"[ERROR] 创建QML叠加层失败: {e}")
    
    def update_status(self, message: str):
        """更新状态信息：通过桥接发射信号到QML"""
        if self.bridge:
            try:
                self.bridge.updateStatus(message)
            except Exception as e:
                print(f"[WARN] 状态更新失败: {e}")
    
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
    

