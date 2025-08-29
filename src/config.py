# -*- coding: utf-8 -*-
"""
配置文件 - QGIS环境配置和地图源配置
"""

import os
import sys

# ==================== QGIS环境配置 ====================
# QGIS安装目录 - 请根据实际安装路径修改
QGIS_PREFIX_PATH = r"E:\Software\QGIS"

# 地图源配置
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

# 默认地图范围（中国东部区域）
DEFAULT_EXTENT = {
    "xmin": 110,
    "ymin": 20,
    "xmax": 130,
    "ymax": 45
}

# 示例城市数据
SAMPLE_CITIES = [
    ("北京", 116.4074, 39.9042),
    ("上海", 121.4737, 31.2304),
    ("广州", 113.2644, 23.1291),
    ("深圳", 114.0579, 22.5431),
    ("杭州", 120.1551, 30.2741)
]

def setup_qgis_environment():
    """设置QGIS环境变量和路径"""
    # 设置QGIS环境变量
    os.environ['QGIS_PREFIX_PATH'] = QGIS_PREFIX_PATH
    os.environ['PATH'] = (
        os.path.join(QGIS_PREFIX_PATH, "bin") + ";" +
        os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "bin") + ";" +
        os.environ['PATH']
    )

    # 添加QGIS Python路径
    qgis_python_path = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python")
    if qgis_python_path not in sys.path:
        sys.path.append(qgis_python_path)
    
    print(f"QGIS环境配置完成: {QGIS_PREFIX_PATH}")
