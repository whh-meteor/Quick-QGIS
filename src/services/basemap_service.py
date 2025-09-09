# -*- coding: utf-8 -*-
"""
底图服务模块 - 负责底图的加载和切换
"""

from qgis.core import QgsRasterLayer, QgsProject
from ..constants import BASEMAP_SOURCES

class BasemapService:
    """底图服务 - 负责底图的加载和切换"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.basemap_layers = {}  # 存储底图图层引用
    
    def load_basemap(self, key: str) -> bool:
        """加载底图"""
        key = (key or "").upper()
        if key not in BASEMAP_SOURCES:
            print(f"底图服务：未知底图键 - {key}")
            return False

        src = BASEMAP_SOURCES[key]
        print(f"底图服务：切换底图 - {src['name']}")

        try:
            # 创建栅格图层
            layer = QgsRasterLayer(src['url'], src['name'], "wms")
            
            if not layer.isValid():
                print(f"底图服务：底图加载失败 - {src['name']}")
                print(f"错误信息：{layer.error().message()}")
                return False

            # 移除旧的底图图层
            self._remove_old_basemaps()
            
            # 添加新底图图层
            self._add_basemap_layer(layer, key)
            
            print(f"底图服务：底图已切换到 - {src['name']}")
            return True
            
        except Exception as e:
            print(f"底图服务：切换底图出错 - {e}")
            return False
    
    def _remove_old_basemaps(self):
        """移除旧的底图图层"""
        known_names = {v['name'] for v in BASEMAP_SOURCES.values()}
        current_layers = self.canvas.layers()
        
        def _get_name(lyr):
            try:
                return lyr.name()
            except Exception:
                return ""
        
        # 保留非底图图层
        kept_layers = [lyr for lyr in current_layers if _get_name(lyr) not in known_names]
        
        # 从项目中移除底图图层
        for layer in current_layers:
            if _get_name(layer) in known_names:
                QgsProject.instance().removeMapLayer(layer)
        
        # 更新画布图层
        self.canvas.setLayers(kept_layers)
    
    def _add_basemap_layer(self, layer, key: str):
        """添加底图图层"""
        # 添加到项目
        QgsProject.instance().addMapLayer(layer, True)
        
        # 添加到画布（底图置底）
        current_layers = self.canvas.layers()
        new_layers = current_layers + [layer]
        self.canvas.setLayers(new_layers)
        
        # 存储引用
        self.basemap_layers[key] = layer
        
        # 刷新画布
        self.canvas.refresh()
    
    def get_available_basemaps(self):
        """获取可用的底图列表"""
        return list(BASEMAP_SOURCES.keys())
    
    def get_current_basemap(self):
        """获取当前底图"""
        for key, layer in self.basemap_layers.items():
            if layer in self.canvas.layers():
                return key
        return None
