// import QtQuick 2.15
// import QtQuick.Controls 2.15
//
// Rectangle {
//     id: notification
//     width: parent.width
//     height: 50
//     anchors.horizontalCenter: parent.horizontalCenter
//     color: "lightblue"
//     radius: 10
//     visible: false
//     opacity: 0.9
//
//     Text {
//         id: messageText
//         anchors.centerIn: parent
//         text: ""
//         color: "black"
//         font.pixelSize: 16
//     }
//
//     Timer {
//         id: hideTimer
//         interval: 3000  // Display for 3 seconds
//         running: false
//         repeat: false
//         onTriggered: notification.visible = false
//     }
//
//     function show(msg) {
//         messageText.text = msg;
//         notification.visible = true;
//         hideTimer.start();
//     }
// }
