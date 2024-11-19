// membersPage.qml
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
          anchors.fill: parent
          spacing: 20  // Space between elements
          anchors.margins: 20  // Margins around the ColumnLayout

          Text {
               text: "All the members"
               font.pointSize: 24
               font.bold: true
               horizontalAlignment: Text.AlignHCenter
               color: "black"
               Layout.alignment: Qt.AlignHCenter
          }

          //List of users
          ColumnLayout {
              Layout.alignment: Qt.AlignHCenter
              spacing: 10  // Space between user entries

              Repeater {
                   spacing: 10
                   Layout.alignment: Qt.AlignHCenter
                   // Profile Icon
                   Image {
                       source: "qtt"
                       width: 24
                       height: 24
                   }
                   // User Name
                   Text {
                       text: "User " + (index + 1)  // Replace with actual user data
                       font.pointSize: 18
                       color: "black"
                   }
                   // Edit Button
                   Button {
                       text: "Edit"
                       onClicked: {
                           console.log("Editing User " + (index + 1))
                           onClicked: editUserDialog.open()  // Open the edit user page
                       }
                   }
              }
          }

          // + Button to open the dialog
          RowLayout {
              Layout.alignment: Qt.AlignLeft
              Text {
                  id: settingsButton
                  text: "+"
                  font.pointSize: 40
                  color: "grey"
                  Layout.alignment: Qt.AlignLeft
                  MouseArea {
                      anchors.fill: parent  // Make the MouseArea fill the entire text area
                      onClicked: newUserDialog.open()
                  }
              }
          }

          RowLayout {
              Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
              anchors.margins: 20  // Margins for the navigation bar

              Button {
                   icon.source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/home.png"
                   icon.width: 35
                   icon.height: 35
                   icon.color: "grey"
                   onClicked: stackView.push(mainPage)
                   width: 250
                   height: 80
                   Layout.preferredWidth: 250
                   Layout.preferredHeight: 80
              }

              Button {
                   icon.source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/team.png"
                   icon.width: 35
                   icon.height: 35
                   icon.color: "grey"
                   onClicked: stackView.push()
                   width: 250
                   height: 80
                   Layout.preferredWidth: 250
                   Layout.preferredHeight: 80
              }
          }
      }
}