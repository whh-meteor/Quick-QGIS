# -*- coding: utf-8 -*-
"""
测试导入脚本 - 验证所有模块的导入是否正常
"""

import sys
import os

print("=== 测试导入脚本 ===")

# 1. 测试QGIS环境配置
print("\n1. 测试QGIS环境配置...")
try:
    from src.config import setup_qgis_environment
    setup_qgis_environment()
    print("✓ QGIS环境配置成功")
except Exception as e:
    print(f"✗ QGIS环境配置失败: {e}")

# 2. 测试基础QGIS模块
print("\n2. 测试基础QGIS模块...")
try:
    from qgis.core import QgsApplication, QgsProject, QgsRasterLayer, QgsVectorLayer
    from qgis.gui import QgsMapCanvas
    print("✓ 基础QGIS模块导入成功")
except Exception as e:
    print(f"✗ 基础QGIS模块导入失败: {e}")

# 3. 测试PyQt模块
print("\n3. 测试PyQt模块...")
try:
    from qgis.PyQt.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
    print("✓ QGIS PyQt Widgets导入成功")
except Exception as e:
    print(f"✗ QGIS PyQt Widgets导入失败: {e}")

try:
    from qgis.PyQt.QtCore import QObject, pyqtSlot
    print("✓ QGIS PyQt Core导入成功")
except Exception as e:
    print(f"✗ QGIS PyQt Core导入失败: {e}")

# 4. 测试QQuickWidget
print("\n4. 测试QQuickWidget...")
qml_available = False
try:
    from qgis.PyQt.QtQuickWidgets import QQuickWidget
    print("✓ QGIS QQuickWidget导入成功")
    qml_available = True
except ImportError:
    try:
        from PyQt5.QtQuickWidgets import QQuickWidget
        print("✓ PyQt5 QQuickWidget导入成功")
        qml_available = True
    except ImportError:
        try:
            from PyQt6.QtQuickWidgets import QQuickWidget
            print("✓ PyQt6 QQuickWidget导入成功")
            qml_available = True
        except ImportError:
            print("✗ QQuickWidget不可用")

# 5. 测试自定义模块
print("\n5. 测试自定义模块...")
try:
    from src.bridge import QmlBridge
    print("✓ Bridge模块导入成功")
except Exception as e:
    print(f"✗ Bridge模块导入失败: {e}")

try:
    from src.layer_manager import LayerManager
    print("✓ LayerManager模块导入成功")
except Exception as e:
    print(f"✗ LayerManager模块导入失败: {e}")

try:
    from src.ui_manager import UIManager
    print("✓ UIManager模块导入成功")
except Exception as e:
    print(f"✗ UIManager模块导入失败: {e}")

try:
    from src.app import QGISMapApp
    print("✓ App模块导入成功")
except Exception as e:
    print(f"✗ App模块导入失败: {e}")

# 6. 测试QML文件
print("\n6. 测试QML文件...")
qml_path = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
if os.path.exists(qml_path):
    print(f"✓ QML文件存在: {qml_path}")
else:
    print(f"✗ QML文件不存在: {qml_path}")

print(f"\n=== 测试结果 ===")
print(f"QML可用: {qml_available}")
print("如果所有测试都通过，应用程序应该可以正常运行。")
