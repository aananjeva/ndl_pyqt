// editUserDialog.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle{
    modal: true
    width: 400
    height: 599
    anchors.centerIn: parent

    Rectangle {
       id: overlay2
       anchors.fill: parent
       color: "white"
       radius: 10
    }

    ColumnLayout {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        spacing: 10

        Text {
           id: editUserText
           font.pointSize: 20
           horizontalAlignment: Text.AlignHCenter
        }

        Rectangle {
           width: 300
           height: 50
           color: "white"
           border.color: "gray"
           border.width: 1


           TextField {
               id: editUserField
               placeholderText: "New Name"
               anchors.fill: parent
               padding: 10
               font.pointSize: 18
               verticalAlignment: TextInput.AlignVCenter
           }
        }

        Button {
           text: "Save"
           width: 100  // Set a specific width
           height: 30  // Set a specific height
           Layout.preferredWidth: 100
           Layout.preferredHeight: 30

           background: Rectangle {
               radius: 10  // Round the corners
               border.color: "gray"  // Set a border color
               border.width: 1  // Set border width
           }

           Layout.alignment: Qt.AlignHCenter
           onClicked: {

           }
        }

        Text {
           id: cancelButton
           text: "Cancel"
           font.pointSize: 12
           color: "black"  // Change text color to indicate it's clickable
           Layout.alignment: Qt.AlignHCenter
           MouseArea {
               anchors.fill: parent  // Make the MouseArea fill the entire text area
               onClicked: {
                   editUserDialog.close()
               }
           }
        }
    }

    onOpened: {
      editUserText.text = "Editing: " + editUserDialog.userName // Update dialog title
      editUserField.text = editUserDialog.userName // Pre-fill the field
    }
}