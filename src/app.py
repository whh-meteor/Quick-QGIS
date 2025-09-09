# -*- coding: utf-8 -*-
"""
主应用程序类 - 整合所有模块
"""

from qgis.core import QgsCoordinateReferenceSystem
from .ui_manager import UIManager
from .layer_manager import LayerManager
from .constants import DEFAULT_CRS, DEFAULT_WINDOW_TITLE

class QGISMapApp:
    """QGIS地图应用程序主类"""
    
    def __init__(self):
        """初始化应用程序"""
        self.ui_manager = None
        self.layer_manager = None
        self.canvas = None
        self.window = None
        
    def initialize(self):
        """初始化应用程序"""
        print("正在初始化QGIS地图应用程序...")
        
        # 创建UI管理器
        self.ui_manager = UIManager(self)
        
        # 创建主窗口和画布
        self.window, self.canvas = self.ui_manager.create_main_window()
        
        if not self.canvas:
            print("[ERROR] 画布创建失败")
            return False
        
        # 创建图层管理器
        self.layer_manager = LayerManager(self.canvas)
        
        # 设置地图
        self.setup_map()
        
        print("应用程序初始化完成")
        return True
        
    def setup_map(self):
        """设置地图图层和显示"""
        print("正在设置地图...")
        
        if not self.canvas:
            print("错误：画布未初始化")
            return
            
        # 设置画布的坐标系统（与矢量数据匹配）
        crs = QgsCoordinateReferenceSystem(DEFAULT_CRS)
        self.canvas.setDestinationCrs(crs)
        print(f"坐标系统设置为 {DEFAULT_CRS}")
        
        # 添加示例矢量数据
        self.layer_manager.add_sample_vector_data()
        
        # 设置画布显示范围
        self.layer_manager.set_canvas_extent()
        
        # 强制刷新画布
        self.canvas.refresh()
        print("地图设置完成")
        
        # 调试信息
        self.layer_manager.debug_canvas_status()
        
        # 默认加载 OSM 底图
        try:
            self.load_basemap_by("OSM")
        except Exception as e:
            print(f"[WARN] 初始底图加载失败: {e}")
        
        # 更新状态
        self.ui_manager.update_status("地图加载完成！")
    
    def load_basemap_by(self, key: str) -> bool:
        """加载底图（委托给图层管理器）"""
        if self.layer_manager:
            return self.layer_manager.load_basemap_by(key)
        return False
    
    def refresh_canvas(self):
        """刷新画布（委托给图层管理器）"""
        if self.layer_manager:
            self.layer_manager.refresh_canvas()
    
    def reset_canvas_extent(self):
        """重置画布范围（委托给图层管理器）"""
        if self.layer_manager:
            self.layer_manager.set_canvas_extent()
    
    def get_window(self):
        """获取主窗口"""
        return self.window
    
    def get_canvas(self):
        """获取地图画布"""
        return self.canvas
