// firstUsedPage.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle{
    width: parent.width
    height: parent.height
    color: "white"

    ColumnLayout {
        spacing: 20
        anchors.centerIn: parent

        Text {
           text: "Be the first one"
           font.pointSize: 24
           font.bold: true
           horizontalAlignment: Text.AlignHCenter
        }

        TextField {
           id: nameInput
           placeholderText: "Enter your name"
           width: parent.width * 0.8
        }

        Button {
           text: "Add Pictures"
           font.pointSize: 15
           Layout.alignment: Qt.AlignHCenter


           onClicked: {
                // Call the function to open the camera
           }
        }
    }

}