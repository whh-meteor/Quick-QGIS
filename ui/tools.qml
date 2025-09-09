import QtQuick 2.15

Item {
    id: toolsRoot
    anchors.fill: parent     // 覆盖父级区域，便于在任意角落定位

    // 容器：右下角
    Rectangle {
        id: container
        width: 56
        color: Qt.rgba(0,0,0,0)
        border.color: Qt.rgba(0,0,0,0)
        border.width: 0
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 16

        Column {
            id: col
            spacing: 10

            // 1) 放大
            Rectangle {
                width: 44; height: 44; radius: 22
                property bool hovered: false
                property bool pressed: false
                color: hovered ? (pressed ? Qt.rgba(0.94,0.97,1,0.98) : Qt.rgba(1,1,1,0.98)) : Qt.rgba(1,1,1,0.92)
                border.width: 1; border.color: Qt.rgba(0,0,0,0.15)
                Text { anchors.centerIn: parent; text: "＋";   color: Qt.rgba(0.2,0.2,0.2,1) }
                MouseArea { anchors.fill: parent; hoverEnabled: true
                    onEntered: parent.hovered = true
                    onExited: { parent.hovered=false; parent.pressed=false }
                    onPressed: parent.pressed = true
                    onReleased: parent.pressed = false
                    onClicked: { qgisBridge && qgisBridge.zoomIn() }
                }
            }

            // 2) 缩小
            Rectangle {
                width: 44; height: 44; radius: 22
                property bool hovered: false
                property bool pressed: false
                color: hovered ? (pressed ? Qt.rgba(0.94,0.97,1,0.98) : Qt.rgba(1,1,1,0.98)) : Qt.rgba(1,1,1,0.92)
                border.width: 1; border.color: Qt.rgba(0,0,0,0.15)
                Text { anchors.centerIn: parent; text: "－";   color: Qt.rgba(0.2,0.2,0.2,1) }
                MouseArea { anchors.fill: parent; hoverEnabled: true
                    onEntered: parent.hovered = true
                    onExited: { parent.hovered=false; parent.pressed=false }
                    onPressed: parent.pressed = true
                    onReleased: parent.pressed = false
                    onClicked: { qgisBridge && qgisBridge.zoomOut() }
                }
            }

            // 3) 回到默认范围
            Rectangle {
                width: 44; height: 44; radius: 22
                property bool hovered: false
                property bool pressed: false
                color: hovered ? (pressed ? Qt.rgba(0.94,0.97,1,0.98) : Qt.rgba(1,1,1,0.98)) : Qt.rgba(1,1,1,0.92)
                border.width: 1; border.color: Qt.rgba(0,0,0,0.15)
                Text { anchors.centerIn: parent; text: "⌖";   color: Qt.rgba(0.2,0.2,0.2,1) }
                MouseArea { anchors.fill: parent; hoverEnabled: true
                    onEntered: parent.hovered = true
                    onExited: { parent.hovered=false; parent.pressed=false }
                    onPressed: parent.pressed = true
                    onReleased: parent.pressed = false
                    onClicked: { qgisBridge && qgisBridge.resetView() }
                }
            }

            // 4) 全屏/退出
            Rectangle {
                width: 44; height: 44; radius: 22
                property bool hovered: false
                property bool pressed: false
                color: hovered ? (pressed ? Qt.rgba(0.94,0.97,1,0.98) : Qt.rgba(1,1,1,0.98)) : Qt.rgba(1,1,1,0.92)
                border.width: 1; border.color: Qt.rgba(0,0,0,0.15)
                Text { anchors.centerIn: parent; text: "⛶";   color: Qt.rgba(0.2,0.2,0.2,1) }
                MouseArea { anchors.fill: parent; hoverEnabled: true
                    onEntered: parent.hovered = true
                    onExited: { parent.hovered=false; parent.pressed=false }
                    onPressed: parent.pressed = true
                    onReleased: parent.pressed = false
                    onClicked: { qgisBridge && qgisBridge.toggleFullscreen() }
                }
            }

            // 5) 清屏（刷新）
            Rectangle {
                width: 44; height: 44; radius: 22
                property bool hovered: false
                property bool pressed: false
                color: hovered ? (pressed ? Qt.rgba(0.94,0.97,1,0.98) : Qt.rgba(1,1,1,0.98)) : Qt.rgba(1,1,1,0.92)
                border.width: 1; border.color: Qt.rgba(0,0,0,0.15)
                Text { anchors.centerIn: parent; text: "🧹";   color: Qt.rgba(0.2,0.2,0.2,1) }
                MouseArea { anchors.fill: parent; hoverEnabled: true
                    onEntered: parent.hovered = true
                    onExited: { parent.hovered=false; parent.pressed=false }
                    onPressed: parent.pressed = true
                    onReleased: parent.pressed = false
                    onClicked: { qgisBridge && qgisBridge.clearCanvas() }
                }
            }

            // 6) 测量（占位）
            Rectangle {
                width: 44; height: 44; radius: 22
                property bool hovered: false
                property bool pressed: false
                color: hovered ? (pressed ? Qt.rgba(0.94,0.97,1,0.98) : Qt.rgba(1,1,1,0.98)) : Qt.rgba(1,1,1,0.92)
                border.width: 1; border.color: Qt.rgba(0,0,0,0.15)
                Text { anchors.centerIn: parent; text: "📏";   color: Qt.rgba(0.2,0.2,0.2,1) }
                MouseArea { anchors.fill: parent; hoverEnabled: true
                    onEntered: parent.hovered = true
                    onExited: { parent.hovered=false; parent.pressed=false }
                    onPressed: parent.pressed = true
                    onReleased: parent.pressed = false
                    onClicked: { /* 预留测量 */ }
                }
            }
        }
    }
}
