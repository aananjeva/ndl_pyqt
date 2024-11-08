// registerPage.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle{
      anchors.fill: parent
      color: "white"

      ColumnLayout {
          anchors.horizontalCenter: parent.horizontalCenter
          anchors.verticalCenter: parent.verticalCenter
          spacing: 20   // Space between elements

          Button {
              text: "←"  // You can replace this with an icon if you prefer
              font.pointSize: 20
              background: Rectangle {
                  color: "white"
              }
              onClicked: {
                  stackView.pop()  // Go back to the login page
              }
          }

          Text {
              text: "Create an account"
              font.pointSize: 24
              font.bold: true
              color: "black"
              horizontalAlignment: Text.AlignHCenter
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

          Rectangle {
              width: 300
              height: 50
              color: "white"
              border.color: "gray"
              border.width: 1


              TextField {
                  id: registerPasswordField
                  placeholderText: "password"
                  anchors.fill: parent
                  padding: 10
                  font.pointSize: 18
                  echoMode: TextInput.Password
                  verticalAlignment: TextInput.AlignVCenter
              }
          }

          Rectangle {
              width: 300
              height: 50
              color: "white"
              border.color: "gray"
              border.width: 1


              TextField {
                  id: repeatPasswordField
                  placeholderText: "repeat password"
                  anchors.fill: parent
                  padding: 10
                  font.pointSize: 18
                  echoMode: TextInput.Password
                  verticalAlignment: TextInput.AlignVCenter
              }
          }

          Button {
              text: "Register"
              width: 600  // Set a specific width
              height: 300  // Set a specific height


              background: Rectangle {
                  radius: 10  // Round the corners
                  border.color: "gray"  // Set a border color
                  border.width: 1  // Set border width
              }

              Layout.alignment: Qt.AlignHCenter
              onClicked: {
                  python.on_register_button_click(
                      registerUsernameField.text,
                      registerPasswordField.text,
                      repeatPasswordField.text,
                      picturesArray
                  )
              }
          }
      }
}