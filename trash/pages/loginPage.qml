// loginPage.qml
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
           spacing: 20  // Space between elements

           Text {
               text: "Welcome to SmartLock"
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
                   id: usernameField
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
                   id: passwordField
                   placeholderText: "password"
                   anchors.fill: parent
                   padding: 10
                   font.pointSize: 18
                   echoMode: TextInput.Password
                   verticalAlignment: TextInput.AlignVCenter
               }
           }

           ColumnLayout {
               spacing: 10
               Layout.alignment: Qt.AlignHCenter

               Button {
                   text: "Login"
                   width: 300
                   height: 50
                   Layout.preferredWidth: 300
                   Layout.preferredHeight: 50
                   onClicked: {
                       python.on_login_button_click(
                            usernameField.text,
                            passwordField.text,
                       )
                   }
               }

               Text {
                   id: resetPasswordButton
                   text: "Forgot the password"
                   font.pointSize: 12
                   color: "black"  // Change text color to indicate it's clickable
                   Layout.alignment: Qt.AlignHCenter
                   MouseArea {
                       anchors.fill: parent  // Make the MouseArea fill the entire text area
                       onClicked: {

                       }
                   }
               }

               Text {
                   id: registerButton
                   text: "I do not have an acount"
                   font.pointSize: 12
                   color: "black"  // Change text color to indicate it's clickable
                   Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                   MouseArea {
                       anchors.fill: parent  // Make the MouseArea fill the entire text area
                       onClicked: {
                           stackView.push(registerPage) // Add the missing parenthesis here
                       }
                   }
               }
           }
      }
}