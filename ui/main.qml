// 导入QtQuick模块，版本2.15
// QtQuick是Qt的声明式UI框架，用于创建现代化的用户界面
import QtQuick 2.15

// 根元素：Item是一个基础的容器元素，不提供视觉外观
// anchors.fill: parent 表示这个Item会填充其父容器的整个区域
Item {
    anchors.fill: parent

    // 头部区域：使用Rectangle创建可见的矩形区域
    Rectangle {
        id: header  // 唯一标识符，用于在QML中引用这个元素
        // 定位属性：设置矩形的位置和大小
        anchors.left: parent.left      // 左边界对齐到父容器左边界
        anchors.right: parent.right    // 右边界对齐到父容器右边界
        anchors.top: parent.top        // 顶部对齐到父容器顶部
        height: 80                     // 固定高度80像素
        
        // 视觉属性
        color: "#f5f5f5"               // 背景颜色（浅灰色）
        border.color: "#cccccc"        // 边框颜色（灰色）
        border.width: 1                // 边框宽度1像素

        // 水平布局容器：Row用于水平排列子元素
        Row {
            anchors.fill: parent       // 填充整个父容器
            anchors.margins: 8         // 设置8像素的外边距
            spacing: 8                 // 子元素之间的间距

            // 标题文本
            Text {
                text: "QGIS地图应用"    // 显示的文本内容
                font.pixelSize: 16     // 字体大小16像素
                font.bold: true        // 粗体显示
                color: "#333333"       // 文本颜色（深灰色）
                anchors.verticalCenter: parent.verticalCenter  // 垂直居中对齐
            }

            // 间隔元素：用于在组件之间添加空白间距
            Item { width: 16; height: 1 }

            // OSM地图按钮
            Rectangle {
                id: btnOSM             // 按钮的唯一标识符
                width: 80; height: 32  // 按钮尺寸
                radius: 4              // 圆角半径
                color: "#ffffff"       // 背景颜色（白色）
                border.color: "#cccccc" // 边框颜色
                anchors.verticalCenter: parent.verticalCenter  // 垂直居中
                
                // 按钮文本
                Text { 
                    anchors.centerIn: parent  // 文本在按钮中居中
                    text: "OSM"               // 显示文本
                    color: "#333333"          // 文本颜色
                }
                
                // 鼠标区域：处理鼠标点击事件
                MouseArea {
                    anchors.fill: parent      // 填充整个按钮区域
                    onClicked: {
                        // 点击时调用Python后端的switchBasemap方法
                        // qgisBridge是Python对象在QML中的引用
                        // && 是逻辑与操作符，确保qgisBridge存在才调用方法
                        qgisBridge && qgisBridge.switchBasemap("OSM")
                    }
                }
            }

            // 高德地图按钮
            Rectangle {
                id: btnGaode
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "高德"
                    color: "#333333"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        // 切换到高德地图底图
                        qgisBridge && qgisBridge.switchBasemap("GAODE")
                    }
                }
            }

            // ArcGIS地图按钮
            Rectangle {
                id: btnArcgis
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "ArcGIS"
                    color: "#333333"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        // 切换到ArcGIS地图底图
                        qgisBridge && qgisBridge.switchBasemap("ARCGIS")
                    }
                }
            }

            // 另一个间隔元素
            Item { width: 16; height: 1 }

            // 刷新按钮
            Rectangle {
                id: btnRefresh
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "刷新"
                    color: "#333333"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        // 刷新地图显示
                        qgisBridge && qgisBridge.refreshMap()
                    }
                }
            }

            // 重置按钮
            Rectangle {
                id: btnReset
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "重置"
                    color: "#333333"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        // 重置地图视图到默认状态
                        qgisBridge && qgisBridge.resetView()
                    }
                }
            }
        }
    }

    // 地图显示区域：这是地图实际显示的地方
    Rectangle {
        // 定位：位于头部下方，填充剩余空间
        anchors.top: header.bottom     // 顶部对齐到header的底部
        anchors.left: parent.left      // 左边界对齐到父容器
        anchors.right: parent.right    // 右边界对齐到父容器
        anchors.bottom: parent.bottom  // 底部对齐到父容器底部
        
        // 视觉属性
        color: "#fafafa"               // 背景颜色（非常浅的灰色）
        border.color: "#cccccc"        // 边框颜色
        border.width: 1                // 边框宽度
        
        // 注意：这里应该添加地图组件（如QQuickWidget或WebView）
        // 用于显示QGIS地图内容
    }
}
