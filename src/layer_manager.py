# -*- coding: utf-8 -*-
"""
图层管理模块 - 负责底图加载和矢量数据管理
"""

from qgis.core import (
    QgsRasterLayer, QgsVectorLayer, QgsProject, QgsFeature, 
    QgsGeometry, QgsPointXY, QgsRectangle
)
from qgis.gui import QgsMapCanvas
from .config import BASEMAP_SOURCES, SAMPLE_CITIES, DEFAULT_EXTENT

class LayerManager:
    """图层管理器"""
    
    def __init__(self, canvas: QgsMapCanvas):
        self.canvas = canvas
        self.basemap_layers = {}  # 存储底图图层引用
    
    def load_basemap_by(self, key: str) -> bool:
        """按键加载并切换底图"""
        key = (key or "").upper()
        if key not in BASEMAP_SOURCES:
            print(f"[WARN] 未知底图键: {key}")
            return False

        src = BASEMAP_SOURCES[key]
        print(f"切换底图: {src['name']}")
        print(f"底图URL: {src['url']}")

        # 检查可用的数据提供者
        from qgis.core import QgsProviderRegistry
        providers = QgsProviderRegistry.instance().providerList()
        print(f"可用的数据提供者: {providers}")
        print(f"WMS提供者可用: {'wms' in providers}")

        try:
            # 创建栅格图层 - 对于XYZ瓦片，使用gdal数据提供者
            layer = QgsRasterLayer(src['url'], src['name'], "wms")
            print(f"图层创建状态: {layer.isValid()}")
            print(f"图层错误信息: {layer.error().summary()}")
            print(f"图层错误详情: {layer.error().message()}")
            
            if not layer.isValid():
                print(f"[FAIL] 底图加载失败: {src['name']}")
                print(f"错误代码: {layer.error()}")
                print(f"错误摘要: {layer.error().summary()}")
                print(f"错误消息: {layer.error().message()}")
                return False

            # 移除旧的底图图层
            self._remove_old_basemaps()
            
            # 添加新底图图层
            self._add_basemap_layer(layer, key)
            
            print(f"[SUCCESS] 底图已切换到: {src['name']}")
            return True
            
        except Exception as e:
            print(f"[ERROR] 切换底图出错: {e}")
            import traceback
            traceback.print_exc()
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
    
    def add_sample_vector_data(self):
        """添加示例矢量数据"""
        print("正在添加示例矢量数据...")
        
        try:
            layers = []
            
            # 1. 创建城市点图层
            point_layer = self._create_city_points_layer()
            if point_layer:
                layers.append(point_layer)
            
            # 2. 创建连接线图层
            line_layer = self._create_connection_lines_layer()
            if line_layer:
                layers.append(line_layer)
            
            # 3. 创建区域面图层
            polygon_layer = self._create_sample_polygon_layer()
            if polygon_layer:
                layers.append(polygon_layer)
            
            # 将图层添加到画布
            if layers:
                current_layers = self.canvas.layers()
                all_layers = current_layers + layers
                self.canvas.setLayers(all_layers)
                self.canvas.refresh()
                print(f"[SUCCESS] {len(layers)} 个矢量图层已添加到画布")
            else:
                print("[ERROR] 没有有效的图层可以添加到画布")
                
        except Exception as e:
            print(f"[ERROR] 添加示例数据失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_city_points_layer(self):
        """创建城市点图层"""
        try:
            point_layer = QgsVectorLayer("Point?crs=EPSG:4326", "中国主要城市", "memory")
            point_provider = point_layer.dataProvider()
            
            # 添加城市点
            for name, lon, lat in SAMPLE_CITIES:
                feature = QgsFeature()
                point = QgsPointXY(lon, lat)
                feature.setGeometry(QgsGeometry.fromPointXY(point))
                feature.setAttributes([name])
                point_provider.addFeatures([feature])
            
            point_layer.updateExtents()
            QgsProject.instance().addMapLayer(point_layer)
            print("[SUCCESS] 城市点图层添加成功")
            return point_layer
            
        except Exception as e:
            print(f"[ERROR] 创建城市点图层失败: {e}")
            return None
    
    def _create_connection_lines_layer(self):
        """创建连接线图层"""
        try:
            line_layer = QgsVectorLayer("LineString?crs=EPSG:4326", "城市连接线", "memory")
            line_provider = line_layer.dataProvider()
            
            # 添加北京到上海的连接线
            line_feature = QgsFeature()
            line_points = [QgsPointXY(116.4074, 39.9042), QgsPointXY(121.4737, 31.2304)]
            line_feature.setGeometry(QgsGeometry.fromPolylineXY(line_points))
            line_feature.setAttributes(["北京-上海"])
            line_provider.addFeatures([line_feature])
            
            line_layer.updateExtents()
            QgsProject.instance().addMapLayer(line_layer)
            print("[SUCCESS] 连接线图层添加成功")
            return line_layer
            
        except Exception as e:
            print(f"[ERROR] 创建连接线图层失败: {e}")
            return None
    
    def _create_sample_polygon_layer(self):
        """创建示例区域面图层"""
        try:
            polygon_layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "示例区域", "memory")
            polygon_provider = polygon_layer.dataProvider()
            
            # 添加一个矩形区域（覆盖中国东部）
            polygon_feature = QgsFeature()
            ring_points = [
                QgsPointXY(DEFAULT_EXTENT["xmin"], DEFAULT_EXTENT["ymin"]),  # 左下
                QgsPointXY(DEFAULT_EXTENT["xmax"], DEFAULT_EXTENT["ymin"]),  # 右下
                QgsPointXY(DEFAULT_EXTENT["xmax"], DEFAULT_EXTENT["ymax"]),  # 右上
                QgsPointXY(DEFAULT_EXTENT["xmin"], DEFAULT_EXTENT["ymax"]),  # 左上
                QgsPointXY(DEFAULT_EXTENT["xmin"], DEFAULT_EXTENT["ymin"])   # 闭合
            ]
            polygon_feature.setGeometry(QgsGeometry.fromPolygonXY([ring_points]))
            polygon_feature.setAttributes(["中国东部区域"])
            polygon_provider.addFeatures([polygon_feature])
            
            polygon_layer.updateExtents()
            QgsProject.instance().addMapLayer(polygon_layer)
            print("[SUCCESS] 区域面图层添加成功")
            return polygon_layer
            
        except Exception as e:
            print(f"[ERROR] 创建区域面图层失败: {e}")
            return None
    
    def set_canvas_extent(self):
        """设置画布显示范围"""
        print("正在设置画布显示范围...")
        
        try:
            # 获取所有图层
            layers = self.canvas.layers()
            print(f"画布当前有 {len(layers)} 个图层")
            
            if layers:
                # 计算所有图层的总范围
                total_extent = None
                for i, layer in enumerate(layers):
                    extent = layer.extent()
                    extent_valid = not extent.isNull() and not extent.isEmpty()
                    print(f"图层 {i+1}: {layer.name()}, 范围有效: {extent_valid}")
                    if extent_valid:
                        if total_extent is None:
                            total_extent = QgsRectangle(extent)
                        else:
                            total_extent.combineExtentWith(extent)
                
                if total_extent and (not total_extent.isNull()) and (not total_extent.isEmpty()):
                    self.canvas.setExtent(total_extent)
                    print(f"[SUCCESS] 画布范围设置完成: {total_extent.toString()}")
                else:
                    self._set_default_extent()
            else:
                self._set_default_extent()
                
            # 强制刷新画布
            self.canvas.refresh()
            print("[INFO] 画布已刷新")
                
        except Exception as e:
            print(f"[ERROR] 设置画布范围失败: {e}")
    
    def _set_default_extent(self):
        """设置默认范围"""
        default_extent = QgsRectangle(
            DEFAULT_EXTENT["xmin"], 
            DEFAULT_EXTENT["ymin"], 
            DEFAULT_EXTENT["xmax"], 
            DEFAULT_EXTENT["ymax"]
        )
        self.canvas.setExtent(default_extent)
        print("[SUCCESS] 使用默认中国东部区域范围")
    
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
