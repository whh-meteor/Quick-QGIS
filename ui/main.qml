import QtQuick 2.15
import QtQml 2.15

Item {
    anchors.fill: parent
    // 统一颜色计算，避免出现 undefined 到 QColor 的赋值错误
    function btnFillColor(hovered, pressed) {
        if (pressed === true) return Qt.rgba(0.85, 0.92, 0.98, 1)
        if (hovered === true) return Qt.rgba(0.95, 0.97, 1.0, 1)
        return Qt.rgba(1, 1, 1, 1)
    }
    function btnBorderColor(hovered) {
        if (hovered === true) return Qt.rgba(0.55, 0.75, 0.95, 1)
        return Qt.rgba(0.8, 0.8, 0.8, 1)
    }

    Rectangle {
        id: header
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 60
        visible: true

        // 叠加层背景透明（使用显式 RGBA，避免某些环境下字符串透明色不被识别）
        color: Qt.rgba(0, 0, 0, 0)
        border.color: Qt.rgba(0, 0, 0, 0)
        border.width: 0

        Row {
            anchors.fill: parent
            anchors.margins: 8
            spacing: 12

            Item { width: 16; height: 1 }
            Rectangle {
                id: btnOSM
                width: 92; height: 34
                radius: 6
                border.width: 1
                property bool hovered: false
                property bool pressed: false
                color: btnFillColor(hovered, pressed)
                border.color: btnBorderColor(hovered)
                anchors.verticalCenter: parent.verticalCenter
                
                Text { 
                    anchors.centerIn: parent
                    text: "OSM"
                    color: Qt.rgba(0.2, 0.2, 0.2, 1)
                }
                
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: btnOSM.hovered = true
                    onExited: { btnOSM.hovered = false; btnOSM.pressed = false }
                    onPressed: btnOSM.pressed = true
                    onReleased: btnOSM.pressed = false
                    onClicked: {
                        qgisBridge && qgisBridge.switchBasemap("OSM")
                    }
                }
            }

            Rectangle {
                id: btnGaode
                width: 92; height: 34
                radius: 6
                border.width: 1
                property bool hovered: false
                property bool pressed: false
                color: btnFillColor(hovered, pressed)
                border.color: btnBorderColor(hovered)
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "高德"
                    color: Qt.rgba(0.2, 0.2, 0.2, 1)
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: btnGaode.hovered = true
                    onExited: { btnGaode.hovered = false; btnGaode.pressed = false }
                    onPressed: btnGaode.pressed = true
                    onReleased: btnGaode.pressed = false
                    onClicked: {
                        qgisBridge && qgisBridge.switchBasemap("GAODE")
                    }
                }
            }

            Rectangle {
                id: btnArcgis
                width: 92; height: 34
                radius: 6
                border.width: 1
                property bool hovered: false
                property bool pressed: false
                color: btnFillColor(hovered, pressed)
                border.color: btnBorderColor(hovered)
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "ArcGIS"
                    color: Qt.rgba(0.2, 0.2, 0.2, 1)
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: btnArcgis.hovered = true
                    onExited: { btnArcgis.hovered = false; btnArcgis.pressed = false }
                    onPressed: btnArcgis.pressed = true
                    onReleased: btnArcgis.pressed = false
                    onClicked: {
                        qgisBridge && qgisBridge.switchBasemap("ARCGIS")
                    }
                }
            }

            Item { width: 16; height: 1 }

            Rectangle {
                id: btnRefresh
                width: 92; height: 34
                radius: 6
                border.width: 1
                property bool hovered: false
                property bool pressed: false
                color: btnFillColor(hovered, pressed)
                border.color: btnBorderColor(hovered)
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "刷新"
                    color: Qt.rgba(0.2, 0.2, 0.2, 1)
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: btnRefresh.hovered = true
                    onExited: { btnRefresh.hovered = false; btnRefresh.pressed = false }
                    onPressed: btnRefresh.pressed = true
                    onReleased: btnRefresh.pressed = false
                    onClicked: {
                        qgisBridge && qgisBridge.refreshMap()
                    }
                }
            }

            Rectangle {
                id: btnReset
                width: 92; height: 34
                radius: 6
                border.width: 1
                property bool hovered: false
                property bool pressed: false
                color: btnFillColor(hovered, pressed)
                border.color: btnBorderColor(hovered)
                anchors.verticalCenter: parent.verticalCenter
                Text { 
                    anchors.centerIn: parent
                    text: "重置"
                    color: Qt.rgba(0.2, 0.2, 0.2, 1)
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: btnReset.hovered = true
                    onExited: { btnReset.hovered = false; btnReset.pressed = false }
                    onPressed: btnReset.pressed = true
                    onReleased: btnReset.pressed = false
                    onClicked: {
                        qgisBridge && qgisBridge.resetView()
                    }
                }
            }

            Item { width: 16; height: 1 }

            // 状态文本，显示来自Python的状态
            Text {
                id: statusText
                text: ""
                color: Qt.rgba(0.4, 0.4, 0.4, 1)
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }

            // 通过 Connections 监听 Python 发射的信号
            Connections {
                target: qgisBridge
                onStatusChanged: function(msg) {
                    statusText.text = msg
                }
            }
        }
    }

}
