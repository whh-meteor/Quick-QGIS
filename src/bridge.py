# -*- coding: utf-8 -*-
"""
QML桥接对象 - 供QML调用的Python接口
"""

try:
    from qgis.PyQt.QtCore import QObject, pyqtSlot
except ImportError:
    try:
        from PyQt5.QtCore import QObject, pyqtSlot
    except ImportError:
        from PyQt6.QtCore import QObject, pyqtSlot

class QmlBridge(QObject):
    """供 QML 调用的桥接对象"""
    
    def __init__(self, app_ref):
        super().__init__()
        self._app = app_ref
    #@pyqtSlot：装饰器，标记方法可以被QML调用
    @pyqtSlot(str)
    def switchBasemap(self, key):
        """切换底图"""
        if self._app:
            self._app.load_basemap_by(key)
    
    @pyqtSlot()
    def refreshMap(self):
        """刷新地图"""
        if self._app:
            self._app.refresh_canvas()
    
    @pyqtSlot()
    def resetView(self):
        """重置视图"""
        if self._app:
            self._app.reset_canvas_extent()
