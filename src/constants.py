# -*- coding: utf-8 -*-
"""
常量定义模块 - 定义应用程序中使用的常量
"""

# 应用程序信息
APP_NAME = "Quick-QGIS"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "基于QGIS的快速地图显示应用程序"

# 窗口设置
DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HEIGHT = 700
DEFAULT_WINDOW_TITLE = f"{APP_NAME} - {APP_VERSION}"

# 地图设置
DEFAULT_CRS = "EPSG:4326"  # WGS84坐标系统
DEFAULT_EXTENT = {
    "xmin": 110,
    "ymin": 20,
    "xmax": 130,
    "ymax": 45
}

# 底图配置
BASEMAP_SOURCES = {
    "OSM": {
        "name": "OpenStreetMap",
        "url": "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    },
    "GAODE": {
        "name": "高德街道图",
        "url": "type=xyz&url=https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}"
    },
    "ARCGIS": {
        "name": "ArcGIS中国地图",
        "url": "type=xyz&url=https://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}"
    }
}

# 示例城市数据
SAMPLE_CITIES = [
    ("北京", 116.4074, 39.9042),
    ("上海", 121.4737, 31.2304),
    ("广州", 113.2644, 23.1291),
    ("深圳", 114.0579, 22.5431),
    ("杭州", 120.1551, 30.2741)
]

# 日志级别
LOG_LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40
}
