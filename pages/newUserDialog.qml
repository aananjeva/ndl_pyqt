// newUserDialog.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle {
    width: 400
    height: 599
    modal: true
    anchors.centerIn: parent

    Rectangle {
        id: overlay
        anchors.fill: parent
        color: "white"
        radius: 10
    }

    ColumnLayout {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        spacing: 20   // Space between elements

        Text {
            text: "Create a new member"
            font.pointSize: 24
            font.bold: true
            color: "black"
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
        }

        Rectangle {
            width: 300
            height: 50
            color: "white"
            border.color: "gray"
            border.width: 1

            TextField {
                id: registerUsernameField
                placeholderText: "username"
                anchors.fill: parent
                padding: 10
                font.pointSize: 18
                verticalAlignment: TextInput.AlignVCenter
            }
        }

        Button {
            text: "Add Photos"
            width: 150
            height: 50
            Layout.preferredWidth: 150
            Layout.preferredHeight: 50
            onClicked: {
                // Logic to open the camera
                console.log("Open camera to add photos")
                // You would need to implement the actual camera logic here
            }
        }
    }

    Button {
      text: "Create"
      width: 150  // Set a specific width
      height: 50  // Set a specific height
      Layout.preferredWidth: 150
      Layout.preferredHeight: 50


      background: Rectangle {
          radius: 10  // Round the corners
          border.color: "gray"  // Set a border color
          border.width: 1  // Set border width
      }

      Layout.alignment: Qt.AlignHCenter
      onClicked: {
        python.on_create_member_button_click(
            registerUsernameField.text,
            picturesArray
        )
      }
    }
}