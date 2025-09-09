# -*- coding: utf-8 -*-
"""
图层管理模块 - 负责底图加载和矢量数据管理
重构版本：使用新的服务模块
"""

from qgis.gui import QgsMapCanvas
from .services.basemap_service import BasemapService
from .core.data_manager import DataManager
from .core.map_engine import MapEngine

class LayerManager:
    """图层管理器 - 整合底图服务、数据管理和地图引擎"""
    
    def __init__(self, canvas: QgsMapCanvas):
        self.canvas = canvas
        # 初始化各个服务
        self.basemap_service = BasemapService(canvas)
        self.data_manager = DataManager(canvas)
        self.map_engine = MapEngine(canvas)
    
    def load_basemap_by(self, key: str) -> bool:
        """按键加载并切换底图（委托给底图服务）"""
        return self.basemap_service.load_basemap(key)
    
    def add_sample_vector_data(self):
        """添加示例矢量数据（委托给数据管理器）"""
        self.data_manager.create_sample_data()
    
    def set_canvas_extent(self):
        """设置画布显示范围（委托给地图引擎）"""
        self.map_engine.set_default_extent()
    
    def refresh_canvas(self):
        """刷新画布（委托给地图引擎）"""
        self.map_engine.refresh()
    
    def get_available_basemaps(self):
        """获取可用的底图列表"""
        return self.basemap_service.get_available_basemaps()
    
    def get_current_basemap(self):
        """获取当前底图"""
        return self.basemap_service.get_current_basemap()
    
    def debug_canvas_status(self):
        """调试画布状态"""
        print("\n=== 画布调试信息 ===")
        try:
            layers = self.canvas.layers()
            print(f"画布图层数量: {len(layers)}")
            
            for i, layer in enumerate(layers):
                print(f"图层 {i+1}: {layer.name()}")
                print(f"  类型: {layer.type()}")
                print(f"  有效: {layer.isValid()}")
                if hasattr(layer, 'extent'):
                    extent = layer.extent()
                    print(f"  范围: {extent.toString()}")
                    print(f"  范围有效: {not extent.isNull() and not extent.isEmpty()}")
            
            # 检查画布状态
            print(f"画布大小: {self.canvas.size().width()} x {self.canvas.size().height()}")
            
            # 检查坐标系统
            crs = self.canvas.mapSettings().destinationCrs()
            print(f"画布坐标系统: {crs.description()}")
            
        except Exception as e:
            print(f"调试信息获取失败: {e}")
