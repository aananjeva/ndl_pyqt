// settingsDialog.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle{
    anchors.fill: parent
    color: "white" // Background color
    radius: 10 // Optional: rounded corners

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Text {
           text: "Account"
           font.pointSize: 24
           font.bold: true
           color: "black"
           horizontalAlignment: Text.AlignHCenter
           Layout.alignment: Qt.AlignLeft
        }

        Text {
           text: "Username: " + username
           font.pointSize: 18
           color: "black"
           Layout.alignment: Qt.AlignHCenter
        }


        Text {
           text: "Change the password"
           font.pointSize: 18
           color: "black"  // Change color to indicate it's clickable
           Layout.alignment: Qt.AlignLeft
           MouseArea {
               anchors.fill: parent  // Make the MouseArea fill the entire text area
               onClicked: {
                   changePasswordDialog.open()
               }
           }
        }

        Text {
           text: "Delete a profile"
           font.pointSize: 18
           color: "black"  // Change color to indicate it's clickable
           Layout.alignment: Qt.AlignLeft
           MouseArea {
               anchors.fill: parent  // Make the MouseArea fill the entire text area
               onClicked: {
                   // Handle the delete profile action here
                   console.log("Delete Profile clicked");
               }
           }
        }
    }
}