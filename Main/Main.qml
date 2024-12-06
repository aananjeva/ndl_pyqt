import QtQuick
import QtQml
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia
import QtQuick.Dialogs


ApplicationWindow {
    id: mainWindow
    width: 600
    height: 750
    visible: true
    title: "SmartLock"

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: introPage
    }

    // Notification {
    //     id: notification
    //     anchors.bottom: parent.bottom
    //     anchors.horizontalCenter: parent.horizontalCenter
    //     width: parent.width * 0.8
    // }
    //
    // Connections {
    //     target: guiBackend
    //     onNotificationSignal: notification.show(message)
    // }


    Component {
        id: introPage

        Rectangle {
            width: parent.width
            height: parent.height
            color: "white"

            Text {
                text: "SmartLock"
                font.pointSize: 32
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: stackView.push(loginPage)
            }
        }
    }

    Component {
        id: loginPage

        Rectangle {
            anchors.fill: parent
            color: "white"


            ColumnLayout {
                anchors.centerIn: parent
                spacing: 20

                Text {
                    text: "Welcome to SmartLock"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    font.pointSize: 24
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }

                Rectangle {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
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
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
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
                            python.login(
                                usernameField.text,
                                passwordField.text
                            )
                        }
                    }

                    Text {
                        id: forgotPasswordButton
                        text: "Forgot the password"
                        font.pointSize: 12
                        color: "black"  // Change text color to indicate it's clickable
                        Layout.alignment: Qt.AlignHCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                stackView.push(defaultPasswordPage)
                            }
                        }
                    }

                    Text {
                        id: registerButton
                        text: "I do not have an account"
                        font.pointSize: 12
                        color: "black"  // Change text color to indicate it's clickable
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                stackView.push(registerPage)
                            }
                        }
                    }
                }

                MessageDialog {
                    id: messageDialog
                    title: "Attention"
                    text: "Please press the button on the lock manually."
                    visible: false
                    onAccepted: console.log("Message dialog accepted")
                }

            }
        }
    }


    Component {
        id: defaultPasswordPage

        Rectangle {
            anchors.fill: parent
            color: "white"
            Button {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: "←"  // You can replace this with an icon if you prefer
                font.pointSize: 20
                anchors.left: parent.left
                anchors.top: parent.top
                background: Rectangle {
                    color: "white"
                }
                onClicked: {
                    stackView.pop()
                }
            }

            ColumnLayout {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                spacing: 20
                anchors.centerIn: parent


                Text {
                    text: "Default Login"
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
                        id: defaultUsernameField
                        placeholderText: "default username"
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
                        id: defaultPasswordField
                        placeholderText: "default password"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 18
                        verticalAlignment: TextInput.AlignVCenter
                    }
                }

                Button {
                    text: "Enter"
                    width: 600
                    height: 300

                    background: Rectangle {
                        radius: 10
                        border.color: "gray"
                        border.width: 1
                    }

                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        stackView.push(mainPage)
                    }
                }
            }
        }
    }

    Component {
        id: registerPage

        Rectangle {
            anchors.fill: parent
            color: "white"
            Button {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: "←"  // You can replace this with an icon if you prefer
                font.pointSize: 20
                anchors.left: parent.left
                anchors.top: parent.top
                background: Rectangle {
                    color: "white"
                }
                onClicked: {
                    stackView.pop()
                }
            }

            ColumnLayout {
                spacing: 20   // Space between elements
                anchors.centerIn: parent

                Text {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    text: "Create an account"
                    font.pointSize: 24
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }

                Rectangle {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
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
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
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
                        python.register(
                            registerUsernameField.text,
                            registerPasswordField.text,
                            repeatPasswordField.text
                        )
                    }
                }
            }
        }
    }


    Component {
        id: mainPage

        Rectangle {
            width: parent.width
            height: parent.height
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                spacing: 20

                Text {
                    id: settingsButton
                    text: "☰"
                    font.pointSize: 40
                    color: "grey"
                    Layout.alignment: Qt.AlignLeft
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent
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
                    checked: false  // Initial state
                    onCheckedChanged: {
                        // python.on_lock_unlock_button_click(doorSwitch.checked)
                    }
                    Layout.alignment: Qt.AlignHCenter
                }

                Text {
                    text: "The last active users:"
                    font.pointSize: 20
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }

                ListView {
                    id: activeUsersListView
                    width: parent.width
                    height: 200 // Adjust the height as needed
                    model: activeUsersModel

                    delegate: RowLayout {
                        spacing: 10

                        Image {
                            source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/user_icon.png"
                            width: 30
                            height: 30
                        }

                        Text {
                            text: model.name
                            font.pointSize: 18
                        }
                    }
                }

                // Bottom Navigation Bar
                RowLayout {
                    Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter


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
    }

    Dialog {
        id: settingsDialog
        width: 400
        height: parent.height
        modal: true
        visible: false


        Rectangle {
            color: "white" // Background color
            anchors.fill: parent

            ColumnLayout {
                anchors.fill: parent
                spacing: 15  // Space between elements
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
    }

    Dialog {
        id: changePasswordDialog
        width: 400
        height: 600
        modal: true
        visible: false
        anchors.centerIn: parent

        Rectangle {
            anchors.fill: parent

            ColumnLayout {
                anchors.fill: parent
                spacing: 10
                anchors.margins: 20  // Add some padding inside the dialog

                Text {
                    text: "Change Password"
                    font.pointSize: 24
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }

                Rectangle {
                    width: parent.width
                    height: 50
                    color: "white"
                    border.color: "gray"
                    border.width: 1

                    TextField {
                        id: currentPasswordField
                        placeholderText: "Current password"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 18
                        echoMode: TextInput.Password
                        verticalAlignment: TextInput.AlignVCenter
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 50
                    color: "white"
                    border.color: "gray"
                    border.width: 1

                    TextField {
                        id: newPasswordField
                        placeholderText: "New password"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 18
                        echoMode: TextInput.Password
                        verticalAlignment: TextInput.AlignVCenter
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 50
                    color: "white"
                    border.color: "gray"
                    border.width: 1

                    TextField {
                        id: repeatNewPasswordField
                        placeholderText: "Repeat new password"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 18
                        echoMode: TextInput.Password
                        verticalAlignment: TextInput.AlignVCenter
                    }
                }

                Button {
                    text: "Change Password"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        // python.on_change_password_button_click(
                        //     currentPasswordField.text,
                        //     newPasswordField.text,
                        //     repeatNewPasswordField.text
                        // )
                    }
                }

                Button {
                    text: "Cancel"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: changePasswordDialog.close()
                }
            }
        }
    }


    ListModel {
        id: activeUsersModel
    }

    Component {
        id: membersPage

        Rectangle {
            width: parent.width
            height: parent.height
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                spacing: 20  // Space between elements

                Text {
                    text: "All the members"
                    font.pointSize: 24
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    color: "black"
                    Layout.alignment: Qt.AlignHCenter
                }

                // List of Users
                ListView {
                    id: membersListView
                    width: parent.width
                    height: 400  // Adjust the height as needed
                    model: membersModel

                    delegate: RowLayout {
                        spacing: 10

                        // Profile Icon
                        Image {
                            source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/user.png"
                            width: 24
                            height: 24
                        }

                        Text {
                            text: model.name
                            font.pointSize: 18
                            color: "black"
                        }

                        Text {
                            text: model.status
                            font.pointSize: 18
                            color: model.status === "In" ? "green" : "red"
                        }

                        Button {
                            text: "Edit"
                            onClicked: {
                                console.log("Editing " + model.name)
                                editUserDialog.open()  // Open the edit user dialog
                            }
                        }
                    }
                }


                RowLayout {
                    Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
                    Text {
                        id: newMemberButton
                        text: "+"
                        font.pointSize: 40
                        color: "grey"
                        Layout.alignment: Qt.AlignLeft
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                stackView.push(newMemberPage)
                            }
                        }
                    }
                }

                // Bottom Navigation Bar
                RowLayout {
                    Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter

                    Button {
                        icon.source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/home.png"
                        icon.width: 35
                        icon.height: 35
                        icon.color: "grey"
                        onClicked: {
                            stackView.push(mainPage)
                        }
                        width: 250
                        height: 80
                        Layout.preferredWidth: 250
                        Layout.preferredHeight: 80
                    }

                    Button {
                        icon.source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/team.png"
                        icon.width: 35
                        height: 35
                        icon.color: "grey"
                        onClicked: stackView.push()
                        Layout.preferredWidth: 250
                        Layout.preferredHeight: 80
                    }
                }
            }
        }
    }

    ListModel {
        id: membersModel
    }

    Dialog {
        id: editUserDialog
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
            spacing: 10

            Text {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                id: editUserText
                font.pointSize: 20
                horizontalAlignment: Text.AlignHCenter
            }

            // Field for editing the member name
            Rectangle {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                width: 300
                height: 50
                color: "white"
                border.color: "gray"
                border.width: 1

                TextField {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    id: editUserField
                    placeholderText: "New Name"
                    anchors.fill: parent
                    padding: 10
                    font.pointSize: 18
                    verticalAlignment: TextInput.AlignVCenter
                }
            }

            // Dropdown or switch to change status (e.g., In/Out or Access/No Access)
            RowLayout {
                spacing: 10
                Text {
                    text: "Status:"
                    font.pointSize: 18
                    color: "black"
                }
                ComboBox {
                    id: statusComboBox
                    model: ["In", "Out"]  // You can use this to set the status
                    currentIndex: 0
                }
            }

            Button {
                text: "Save"
                width: 100
                height: 30
                Layout.preferredWidth: 100
                Layout.preferredHeight: 30
                background: Rectangle {
                    radius: 10
                    border.color: "gray"
                    border.width: 1
                }
                Layout.alignment: Qt.AlignHCenter

                onClicked: {
                    // var newName = editUserField.text
                    // var newStatus = statusComboBox.currentText
                    //
                    // python.change_member(editUserDialog.userName, newName)
                    // python.change_member_status(editUserDialog.userName, newStatus === "In")
                    //
                    // editUserDialog.close()
                }
            }

            Text {
                id: cancelButton
                text: "Cancel"
                font.pointSize: 12
                color: "black"
                Layout.alignment: Qt.AlignHCenter
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        editUserDialog.close()
                    }
                }
            }
        }

        onOpened: {
            editUserText.text = "Editing: " + editUserDialog.userName
            editUserField.text = editUserDialog.userName
        }
    }


    Component {
        id: newMemberPage

        Item {
            id: newMemberItem
            width: 500
            height: 650
            anchors.centerIn: parent

            Rectangle {
                id: overlay
                anchors.fill: parent
                color: "white"
                radius: 10
            }

            Button {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: "←"
                font.pointSize: 20
                anchors.left: parent.left
                anchors.top: parent.top
                background: Rectangle {
                    color: "white"
                }
                onClicked: {
                    stackView.pop()
                }
            }

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 20

                Text {
                    text: "Create a new member"
                    font.pointSize: 24
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }

                Rectangle {
                    width: 300
                    height: 50
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    color: "white"
                    border.color: "gray"
                    border.width: 1

                    TextField {
                        id: newMemberNameField
                        placeholderText: "Name"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 18
                        verticalAlignment: TextInput.AlignVCenter
                    }
                }

                Rectangle {
                    width: 300
                    height: 50
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    color: "white"
                    border.color: "gray"
                    border.width: 1

                    TextField {
                        id: newMemberSurnameField
                        placeholderText: "Surname"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 18
                        verticalAlignment: TextInput.AlignVCenter
                    }
                }

                Button {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    text: "Take Pictures"

                    onClicked: {
                        stackView.push(cameraPage)
                    }
                }

                Text {
                    text: "Select status"
                    font.pointSize: 18
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    color: "black"
                }

                ComboBox {
                    id: statusComboBox
                    width: 300
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    model: ["Always", "Temporary"]

                    onCurrentIndexChanged: {
                        if (currentIndex === 1) { // Temporary selected
                            dateTimeDialog.open();
                        }
                    }
                }
            }

            Button {
                text: "Save"
                font.pointSize: 18
                width: 150
                height: 50
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 20
                background: Rectangle {
                    color: "gray"
                    radius: 10
                }
                onClicked: {
                    // console.log("Save clicked with data:", newMemberNameField.text, newMemberSurnameField.text, statusComboBox.currentText);
                }
            }
        }
    }

    Dialog {
        id: dateTimeDialog
        title: "Select Date and Time"
        modal: true
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        width: 400
        height: 500
        anchors.centerIn: parent

        onAccepted: {
            console.log("Date and Time selected:", daySpinBox.value, monthSpinBox.value, yearSpinBox.value, hourSpinBox.value, minuteSpinBox.value);
        }
        onRejected: {
            console.log("Date and Time selection canceled");
        }

        ColumnLayout {
            spacing: 10
            anchors.centerIn: parent

            Text {
                text: "Choose Date"
                font.pointSize: 18
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                color: "black"
            }

            ColumnLayout {
                spacing: 5
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                RowLayout {
                    Text {
                        text: "Day"
                        font.pointSize: 16
                        verticalAlignment: Text.AlignVCenter
                    }

                    SpinBox {
                        id: daySpinBox
                        from: 1
                        to: 31
                        value: 1
                        width: 40
                    }
                }

                RowLayout {

                    Text {
                        text: "Month"
                        font.pointSize: 16
                        verticalAlignment: Text.AlignVCenter
                    }

                    SpinBox {
                        id: monthSpinBox
                        from: 1
                        to: 12
                        value: 1
                        width: 40
                    }
                }

                RowLayout {

                    Text {
                        text: "Year"
                        font.pointSize: 16
                        verticalAlignment: Text.AlignVCenter
                    }

                    SpinBox {
                        id: yearSpinBox
                        from: 2024
                        to: 2030
                        value: 2024
                        width: 60
                    }
                }


            }

            Text {
                text: "Choose Time"
                font.pointSize: 18
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                color: "black"
            }

            RowLayout {
                spacing: 10
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                SpinBox {
                    id: hourSpinBox
                    from: 0
                    to: 23
                    value: 12
                    width: 30
                }

                Text {
                    text: "Hour"
                    font.pointSize: 16
                    verticalAlignment: Text.AlignVCenter
                }

                SpinBox {
                    id: minuteSpinBox
                    from: 0
                    to: 59
                    value: 0
                    width: 30
                }

                Text {
                    text: "Minutes"
                    font.pointSize: 16
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
    }

    // Component {
    //     id: addPicturesPage
    //
    //     Rectangle {
    //         anchors.fill: parent
    //         color: "white"
    //
    //         ColumnLayout {
    //             anchors.centerIn: parent
    //             spacing: 20
    //
    //             Text {
    //                 text: "Please take 6 pictures using your device camera."
    //                 font.pointSize: 18
    //                 font.bold: true
    //                 color: "black"
    //                 horizontalAlignment: Text.AlignHCenter
    //             }
    //
    //             Button {
    //                 text: "Move Pictures"
    //                 onClicked: {
    //                 python.move_pictures_to_app_folder()
    //                 }
    //             }
    //
    //             Button {
    //                 text: "Open Camera"
    //                 onClicked: {
    //                     python.open_device_camera()
    //                 }
    //             }
    //
    //             Button {
    //                 text: "Finish"
    //                 onClicked: {
    //                     python.check_picture_completion()  // Verify picture completion in Python
    //                 }
    //             }
    //         }
    //     }
    // }

    Component {
        id: cameraPage

        Rectangle {
            anchors.fill: parent
            color: "white"

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 20

                Text {
                    text: "Take 6 Pictures"
                    font.pointSize: 18
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }

                Button {
                    text: "Take Picture"
                    onClicked: {
                        python.take_picture()  // Call the Python function to capture a picture
                    }
                }

                Button {
                    text: "Finish"
                    enabled: python.pictureCount === 6  // Enable only after 6 pictures
                    onClicked: {
                        stackView.pop()  // Return to the previous page
                    }
                }

                Text {
                    text: "Pictures Taken: " + python.pictureCount + "/6"
                    font.pointSize: 16
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }


}
