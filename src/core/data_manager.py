# -*- coding: utf-8 -*-
"""
数据管理模块 - 负责矢量数据的创建和管理
"""

from qgis.core import (
    QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, 
    QgsProject, QgsRectangle
)
from ..constants import SAMPLE_CITIES, DEFAULT_EXTENT, DEFAULT_CRS

class DataManager:
    """数据管理器 - 负责矢量数据的创建和管理"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.vector_layers = []
    
    def create_sample_data(self):
        """创建示例数据"""
        print("数据管理器：正在创建示例数据...")
        
        try:
            layers = []
            
            # 创建城市点图层
            point_layer = self._create_city_points_layer()
            if point_layer:
                layers.append(point_layer)
            
            # 创建连接线图层
            line_layer = self._create_connection_lines_layer()
            if line_layer:
                layers.append(line_layer)
            
            # 创建区域面图层
            polygon_layer = self._create_sample_polygon_layer()
            if polygon_layer:
                layers.append(polygon_layer)
            
            # 将图层添加到画布
            if layers:
                self._add_layers_to_canvas(layers)
                self.vector_layers.extend(layers)
                print(f"数据管理器：{len(layers)} 个矢量图层已创建")
            else:
                print("数据管理器：没有有效的图层可以创建")
                
        except Exception as e:
            print(f"数据管理器：创建示例数据失败 - {e}")
    
    def _create_city_points_layer(self):
        """创建城市点图层"""
        try:
            point_layer = QgsVectorLayer(f"Point?crs={DEFAULT_CRS}", "中国主要城市", "memory")
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
            print("数据管理器：城市点图层创建成功")
            return point_layer
            
        except Exception as e:
            print(f"数据管理器：创建城市点图层失败 - {e}")
            return None
    
    def _create_connection_lines_layer(self):
        """创建连接线图层"""
        try:
            line_layer = QgsVectorLayer(f"LineString?crs={DEFAULT_CRS}", "城市连接线", "memory")
            line_provider = line_layer.dataProvider()
            
            # 添加北京到上海的连接线
            line_feature = QgsFeature()
            line_points = [QgsPointXY(116.4074, 39.9042), QgsPointXY(121.4737, 31.2304)]
            line_feature.setGeometry(QgsGeometry.fromPolylineXY(line_points))
            line_feature.setAttributes(["北京-上海"])
            line_provider.addFeatures([line_feature])
            
            line_layer.updateExtents()
            QgsProject.instance().addMapLayer(line_layer)
            print("数据管理器：连接线图层创建成功")
            return line_layer
            
        except Exception as e:
            print(f"数据管理器：创建连接线图层失败 - {e}")
            return None
    
    def _create_sample_polygon_layer(self):
        """创建示例区域面图层"""
        try:
            polygon_layer = QgsVectorLayer(f"Polygon?crs={DEFAULT_CRS}", "示例区域", "memory")
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
            print("数据管理器：区域面图层创建成功")
            return polygon_layer
            
        except Exception as e:
            print(f"数据管理器：创建区域面图层失败 - {e}")
            return None
    
    def _add_layers_to_canvas(self, layers):
        """将图层添加到画布"""
        current_layers = self.canvas.layers()
        all_layers = current_layers + layers
        self.canvas.setLayers(all_layers)
        self.canvas.refresh()
    
    def get_layers(self):
        """获取所有矢量图层"""
        return self.vector_layers
