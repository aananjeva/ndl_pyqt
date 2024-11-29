// mainPage.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle {
    width: parent.width
    height: parent.height
    color: "white"

    ColumnLayout {
       anchors.fill: parent
       anchors.margins: 20  // Margins around the ColumnLayout

        Text {
           id: settingsButton
           text: "☰"
           font.pointSize: 40
           color: "grey"
           Layout.alignment: Qt.AlignLeft
           MouseArea {
               anchors.fill: parent  // Make the MouseArea fill the entire text area
               onClicked: settingsDialog.open()
           }
        }

        Text {
           id: doorStatusText
           text: "The door is unlocked"
           font.bold: true
           font.pointSize: 24
           horizontalAlignment: Text.AlignHCenter
           color: "black"
           Layout.alignment: Qt.AlignHCenter
        }


        Switch {
           id: doorSwitch
           scale: 1.5
           onCheckedChanged: {
               doorStatusText.text = doorSwitch.checked ? "The door is locked" : "The door is unlocked"
           }
           Layout.alignment: Qt.AlignHCenter
        }

           // Active Users Header
        Text {
           text: "The last active users:"
           font.pointSize: 20
           color: "black"
           horizontalAlignment: Text.AlignHCenter
           Layout.alignment: Qt.AlignHCenter
        }

        ColumnLayout {
           spacing: 10  // Space between user entries
           Layout.alignment: Qt.AlignHCenter
           Row {
              spacing: 10
              Image {
                  source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/user_icon.png"
                  width: 30
                  height: 30
              }

              Text {
                  text: "name 1"
                  font.pointSize: 18
              }
           }

           Row {
               spacing: 10
               Image {
                   source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/user_icon.png"
                   width: 30
                   height: 30
               }
               Text {
                   text: "name 2"
                   font.pointSize: 18
               }
           }


           Row {
               spacing: 10
               Image {
                   source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/user_icon.png"
                   width: 30
                   height: 30
               }
               Text {
                   text: "name 3"
                   font.pointSize: 18
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
               onClicked: stackView.push()
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
               onClicked: stackView.push(membersPage)
               width: 250
               height: 80
               Layout.preferredWidth: 250
               Layout.preferredHeight: 80
           }
       }


    }
}
