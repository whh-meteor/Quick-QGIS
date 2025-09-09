# -*- coding: utf-8 -*-
"""
地图引擎模块 - 负责地图的核心渲染和显示功能
"""

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsMapCanvas
from ..constants import DEFAULT_EXTENT, DEFAULT_CRS

class MapEngine:
    """地图引擎 - 负责地图的核心渲染功能"""
    
    def __init__(self, canvas: QgsMapCanvas):
        self.canvas = canvas
        self._setup_canvas()
    
    def _setup_canvas(self):
        """设置画布基本属性"""
        # 设置坐标系统
        crs = QgsCoordinateReferenceSystem(DEFAULT_CRS)
        self.canvas.setDestinationCrs(crs)
        print(f"地图引擎：坐标系统设置为 {DEFAULT_CRS}")
    
    def set_extent(self, xmin: float, ymin: float, xmax: float, ymax: float):
        """设置地图显示范围"""
        from qgis.core import QgsRectangle
        extent = QgsRectangle(xmin, ymin, xmax, ymax)
        self.canvas.setExtent(extent)
        self.canvas.refresh()
        print(f"地图引擎：设置显示范围 {extent.toString()}")
    
    def set_default_extent(self):
        """设置默认显示范围"""
        self.set_extent(
            DEFAULT_EXTENT["xmin"],
            DEFAULT_EXTENT["ymin"], 
            DEFAULT_EXTENT["xmax"],
            DEFAULT_EXTENT["ymax"]
        )
    
    def refresh(self):
        """刷新地图显示"""
        self.canvas.refresh()
    
    def get_canvas(self):
        """获取地图画布"""
        return self.canvas
