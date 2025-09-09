# -*- coding: utf-8 -*-
"""
QML桥接对象 - 供QML调用的Python接口
"""


from qgis.PyQt.QtCore import QObject, pyqtSlot, pyqtSignal


class QmlBridge(QObject):
    """供 QML 调用的桥接对象"""
    
    # 供QML绑定的状态信号
    statusChanged = pyqtSignal(str)

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

    @pyqtSlot(str)
    def updateStatus(self, message):
        """由Python调用，通知QML状态变化"""
        self.statusChanged.emit(message)

    # 视图控制：提供给 QML 调用
    @pyqtSlot()
    def zoomIn(self):
        if self._app:
            self._app.zoom_in()

    @pyqtSlot()
    def zoomOut(self):
        if self._app:
            self._app.zoom_out()

    @pyqtSlot()
    def clearCanvas(self):
        """清屏：仅刷新（如需清除图层，可扩展）"""
        if self._app and self._app.layer_manager:
            # 这里先简单刷新，如需真正移除图层可在 layer_manager 增加清理函数
            self._app.refresh_canvas()

    @pyqtSlot()
    def toggleFullscreen(self):
        if self._app and self._app.get_window():
            w = self._app.get_window()
            if w.isFullScreen():
                w.showNormal()
            else:
                w.showFullScreen()
