# QGIS 地图显示应用程序

一个基于 QGIS 的 Python 地图显示应用程序，采用模块化设计，支持多种在线地图源。

## 项目结构

```
withQGIS/
├── main.py                 # 主入口文件
├── src/                    # 源代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── config.py           # 配置文件（QGIS环境、地图源配置）
│   ├── bridge.py           # QML桥接对象
│   ├── layer_manager.py    # 图层管理模块
│   ├── ui_manager.py       # UI管理模块
│   └── app.py              # 主应用程序类
├── ui/                     # UI文件目录
│   └── main.qml           # QML界面文件
├── data/                   # 数据目录
├── requirements.txt        # Python依赖
├── pyproject.toml         # 项目配置
└── README.md              # 项目说明
```

## 功能特性

- **模块化设计**: 代码按功能分离，便于维护和扩展
- **多种地图源**: 支持 OpenStreetMap、高德地图、ArcGIS 等
- **QML 界面**: 现代化的用户界面
- **矢量数据**: 支持点、线、面等矢量数据展示
- **坐标系统**: 支持 WGS84 坐标系统

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

## 模块说明

### config.py

- QGIS 环境配置
- 地图源配置
- 默认参数设置

### bridge.py

- QML 与 Python 的桥接对象
- 提供地图切换、刷新等功能接口

### layer_manager.py

- 图层管理核心模块
- 底图加载和切换
- 矢量数据创建和管理
- 画布范围设置

### ui_manager.py

- UI 界面管理
- QML 界面加载
- 备用界面创建

### app.py

- 主应用程序类
- 整合所有模块
- 应用程序生命周期管理

## 使用说明

1. **启动应用**: 运行 `python main.py`
2. **切换底图**: 点击界面上的 OSM、高德、ArcGIS 按钮
3. **刷新地图**: 点击刷新按钮
4. **重置视图**: 点击重置按钮

## 扩展开发

### 添加新的地图源

在 `src/config.py` 中的 `BASEMAP_SOURCES` 字典中添加新的地图源：

```python
BASEMAP_SOURCES = {
    "NEW_MAP": {
        "name": "新地图源",
        "url": "type=xyz&url=https://your-map-server/{z}/{x}/{y}.png"
    }
}
```

### 添加新的矢量数据

在 `layer_manager.py` 中添加新的数据创建方法，并在 `add_sample_vector_data()` 中调用。

## 故障排除

### 常见问题

1. **QGIS 路径错误**: 检查 `config.py` 中的 `QGIS_PREFIX_PATH` 设置
2. **地图不显示**: 检查网络连接和地图源 URL
3. **QML 加载失败**: 检查 `ui/main.qml` 文件路径

### 调试模式

应用程序会输出详细的调试信息，包括：

- 图层加载状态
- 画布范围设置
- 错误信息

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。
