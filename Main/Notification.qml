// Notification.qml
import QtQuick 6.0
import QtQuick.Controls 6.0

Rectangle {
    id: notification
    width: parent.width * 0.7
    height: 30
    radius: 10
    color: "gray"
    opacity: 0
    visible: false
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.bottom: parent.bottom
    anchors.bottomMargin: 20

    Text {
        id: notificationText
        text: ""
        anchors.centerIn: parent
        color: "white"
        font.pixelSize: 13
    }

    // Animation to fade in and out
    SequentialAnimation {
        id: showAnimation
        PropertyAnimation { target: notification; property: "opacity"; to: 1; duration: 500 }
        PauseAnimation { duration: 3000 } // Duration the notification stays visible
        PropertyAnimation { target: notification; property: "opacity"; to: 0; duration: 500 }
        onFinished: notification.visible = false
    }

    function show(message) {
        notificationText.text = message
        visible = true
        showAnimation.start()
    }
}
