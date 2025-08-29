import QtQuick 2.15

Item {
    width: 800
    height: 300

    Rectangle {
        id: header
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 56
        color: "#f5f5f5"
        border.color: "#cccccc"
        border.width: 1

        Row {
            anchors.fill: parent
            anchors.margins: 8
            spacing: 8

            Text {
                text: "QGIS地图应用"
                font.pixelSize: 16
                font.bold: true
                color: "#333333"
                anchors.verticalCenter: parent.verticalCenter
            }

            Item { width: 16; height: 1 }

            Rectangle {
                id: btnOSM
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { anchors.centerIn: parent; text: "OSM"; color: "#333333" }
                MouseArea {
                    anchors.fill: parent
                    onClicked: qgisBridge && qgisBridge.switchBasemap("OSM")
                }
            }

            Rectangle {
                id: btnGaode
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { anchors.centerIn: parent; text: "高德"; color: "#333333" }
                MouseArea {
                    anchors.fill: parent
                    onClicked: qgisBridge && qgisBridge.switchBasemap("GAODE")
                }
            }

            Rectangle {
                id: btnArcgis
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { anchors.centerIn: parent; text: "ArcGIS"; color: "#333333" }
                MouseArea {
                    anchors.fill: parent
                    onClicked: qgisBridge && qgisBridge.switchBasemap("ARCGIS")
                }
            }

            Item { width: 16; height: 1 }

            Rectangle {
                id: btnRefresh
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { anchors.centerIn: parent; text: "刷新"; color: "#333333" }
                MouseArea {
                    anchors.fill: parent
                    onClicked: qgisBridge && qgisBridge.refreshMap()
                }
            }

            Rectangle {
                id: btnReset
                width: 80; height: 32
                radius: 4
                color: "#ffffff"
                border.color: "#cccccc"
                anchors.verticalCenter: parent.verticalCenter
                Text { anchors.centerIn: parent; text: "重置"; color: "#333333" }
                MouseArea {
                    anchors.fill: parent
                    onClicked: qgisBridge && qgisBridge.resetView()
                }
            }
        }
    }

    Rectangle {
        anchors.top: header.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        color: "#fafafa"
        border.color: "#cccccc"
        border.width: 1
    }
}
