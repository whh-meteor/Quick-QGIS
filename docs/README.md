# Quick-QGIS 文档

## 项目概述

Quick-QGIS 是一个基于 QGIS 的快速地图显示应用程序，采用模块化设计，支持多种在线地图源。

## 架构设计

### 模块划分

```
src/
├── core/                    # 核心模块
│   ├── map_engine.py       # 地图引擎
│   └── data_manager.py     # 数据管理器
├── services/               # 服务模块
│   └── basemap_service.py  # 底图服务
├── utils/                  # 工具模块
│   └── logger.py          # 日志工具
├── constants.py            # 常量定义
├── config.py              # 配置文件
├── app.py                 # 主应用程序
├── layer_manager.py       # 图层管理器
├── ui_manager.py          # UI管理器
└── bridge.py              # QML桥接
```

### 设计原则

1. **单一职责原则**: 每个模块只负责一个特定功能
2. **依赖注入**: 通过构造函数注入依赖
3. **接口分离**: 模块间通过明确的接口通信
4. **配置集中**: 所有配置集中在 constants.py 和 config.py

## 开发指南

### 添加新功能

1. 在相应的模块目录下创建新文件
2. 在 constants.py 中定义相关常量
3. 更新相关模块的导入
4. 更新文档

### 代码规范

- 使用中文注释
- 遵循 PEP 8 代码风格
- 使用类型提示
- 添加详细的文档字符串
