// changePasswordDialog.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle{
    anchors.fill: parent
    color: "white"
    radius: 10

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Text {
            text: "Change Password"
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
                id: currentPasswordField
                placeholderText: "Current Password"
                anchors.fill: parent
                padding: 10
                font.pointSize: 18
                echoMode: TextInput.Password
            }
        }

        Rectangle {
            width: 300
            height: 50
            color: "white"
            border.color: "gray"
            border.width: 1

            TextField {
                id: newPasswordField
                placeholderText: "New Password"
                anchors.fill: parent
                padding: 10
                font.pointSize: 18
                echoMode: TextInput.Password
            }
        }

        Rectangle {
            width: 300
            height: 50
            color: "white"
            border.color: "gray"
            border.width: 1

            TextField {
                id: repeatNewPasswordField
                placeholderText: "Repeat New Password"
                anchors.fill: parent
                padding: 10
                font.pointSize: 18
                echoMode: TextInput.Password
            }
        }

        Button {
            text: "Change Password"
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                if (newPasswordField.text === repeatNewPasswordField.text) {
                    python.on_change_password(
                        currentPasswordField.text,
                        newPasswordField.text
                    )
                    changePasswordDialog.close()
                } else {
                    console.log("New passwords do not match")
                    // Optionally show an error message to the user
                }
            }
        }

        Text {
            text: "Cancel"
            font.pointSize: 12
            color: "black"
            Layout.alignment: Qt.AlignHCenter
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    changePasswordDialog.close()
                }
            }
        }


    }


}