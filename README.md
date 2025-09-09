# Quick-QGIS

一个基于 QGIS 的快速地图显示应用程序，采用模块化设计，支持多种在线地图源。

## 项目结构

```
Quick-QGIS/
├── main.py                 # 主入口文件
├── src/                    # 源代码目录
│   ├── core/              # 核心模块
│   │   ├── map_engine.py  # 地图引擎
│   │   └── data_manager.py # 数据管理器
│   ├── services/          # 服务模块
│   │   └── basemap_service.py # 底图服务
│   ├── utils/             # 工具模块
│   │   └── logger.py      # 日志工具
│   ├── constants.py       # 常量定义
│   ├── config.py          # 配置文件
│   ├── app.py             # 主应用程序类
│   ├── layer_manager.py   # 图层管理器
│   ├── ui_manager.py      # UI管理器
│   └── bridge.py          # QML桥接
├── ui/                    # UI文件目录
│   └── main.qml          # QML界面文件
├── docs/                  # 文档目录
│   └── README.md         # 详细文档
├── tests/                 # 测试目录
│   └── test_basemap_service.py # 测试文件
├── scripts/               # 脚本目录
│   ├── build.py          # 构建脚本
│   └── run.py            # 运行脚本
├── data/                  # 数据目录
├── requirements.txt       # Python依赖
├── pyproject.toml        # 项目配置
└── README.md             # 项目说明
```

## 功能特性

- **模块化设计**: 采用分层架构，代码按功能分离，便于维护和扩展
- **多种地图源**: 支持 OpenStreetMap、高德地图、ArcGIS 等在线地图
- **QML 界面**: 现代化的用户界面，支持响应式设计
- **矢量数据**: 支持点、线、面等矢量数据展示和管理
- **坐标系统**: 支持 WGS84 坐标系统
- **服务化架构**: 底图服务、数据管理服务独立运行
- **日志系统**: 完整的日志记录和调试功能
- **测试支持**: 包含单元测试和集成测试

## 安装和配置

### 1. 环境要求

- Python 3.7+
- QGIS 3.x
- PyQt5/PyQt6

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 QGIS 路径

编辑 `src/config.py` 文件，修改 `QGIS_PREFIX_PATH` 为你的 QGIS 安装路径：

```python
QGIS_PREFIX_PATH = r"E:\Software\QGIS"  # 修改为你的QGIS安装路径
```

### 4. 运行应用程序

```bash
python main.py
```

## 架构设计

### 核心模块 (core/)

- **map_engine.py**: 地图引擎，负责地图的核心渲染和显示功能
- **data_manager.py**: 数据管理器，负责矢量数据的创建和管理

### 服务模块 (services/)

- **basemap_service.py**: 底图服务，负责底图的加载和切换

### 工具模块 (utils/)

- **logger.py**: 日志工具，提供统一的日志记录功能

### 配置模块

- **constants.py**: 常量定义，包含应用程序中使用的所有常量
- **config.py**: 配置文件，QGIS 环境配置

### 管理模块

- **layer_manager.py**: 图层管理器，整合底图服务、数据管理和地图引擎
- **ui_manager.py**: UI 管理器，负责主窗口和 QML 界面的创建
- **bridge.py**: QML 桥接对象，提供 QML 与 Python 的接口

### 应用模块

- **app.py**: 主应用程序类，整合所有模块，管理应用程序生命周期

## 使用说明

### 快速开始

1. **启动应用**: 运行 `python main.py` 或 `python scripts/run.py`
2. **切换底图**: 点击界面上的 OSM、高德、ArcGIS 按钮
3. **刷新地图**: 点击刷新按钮
4. **重置视图**: 点击重置按钮

### 构建和部署

```bash
# 构建应用程序
python scripts/build.py

# 运行测试
python -m pytest tests/

# 安装开发版本
pip install -e .
```

## 开发指南

### 添加新的地图源

在 `src/constants.py` 中的 `BASEMAP_SOURCES` 字典中添加新的地图源：

```python
BASEMAP_SOURCES = {
    "NEW_MAP": {
        "name": "新地图源",
        "url": "type=xyz&url=https://your-map-server/{z}/{x}/{y}.png"
    }
}
```

### 添加新的矢量数据

在 `src/core/data_manager.py` 中添加新的数据创建方法，并在 `create_sample_data()` 中调用。

### 添加新的服务

1. 在 `src/services/` 目录下创建新的服务文件
2. 在相应的管理器中集成新服务
3. 更新相关文档和测试

### 代码规范

- 使用中文注释和文档字符串
- 遵循 PEP 8 代码风格
- 使用类型提示
- 添加单元测试

## 故障排除

### 常见问题

1. **QGIS 路径错误**: 检查 `src/config.py` 中的 `QGIS_PREFIX_PATH` 设置
2. **地图不显示**: 检查网络连接和地图源 URL
3. **QML 加载失败**: 检查 `ui/main.qml` 文件路径
4. **模块导入错误**: 确保所有依赖已正确安装

### 调试模式

应用程序会输出详细的调试信息，包括：

- 图层加载状态
- 画布范围设置
- 服务状态信息
- 错误堆栈跟踪

### 日志查看

应用程序使用统一的日志系统，可以通过修改 `src/utils/logger.py` 来调整日志级别和输出格式。

## 版本历史

### v2.0.0 (当前版本)

- 重构为模块化架构
- 添加服务化设计
- 完善日志系统
- 添加测试支持
- 优化代码结构

### v1.0.0

- 基础地图显示功能
- QML 界面支持
- 多种地图源支持

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

### 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [GitHub Issues]
- 邮箱: \*\*\*\*
