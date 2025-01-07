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

    Notification {
        id: notification
    }

    ListModel {
        id: membersModel
    }

    ListModel {
        id: activeMembersModel
    }

    Connections {
        target: python
        onOnLoginSuccess: {
            stackView.push(mainPage)
            python.list_active_members_gui()
            python.lock_listener()
        }

        onOnRegisterSuccess: {
            stackView.push(mainPage)
            python.list_active_members_gui()
            python.lock_listener()
        }

        onDefaultLoginSuccess: {
            stackView.push(mainPage)
            python.list_active_members_gui()
            python.lock_listener()
        }

        onMembersUpdated: function (members) {
            membersModel.clear();
            for (let i = 0; i < members.length; i++) {
                membersModel.append({
                    name: members[i].name,
                    status: members[i].authorization,
                    access_remaining: members[i].access_remaining,
                    id: members[i].id
                });
            }
        }

        onNotificationSignal: function (message) {
            notification.show(message);
        }

        onActiveMembersUpdated: function (members) {
            activeMembersModel.clear();
            for (let i = 0; i < members.length; i++) {
                activeMembersModel.append({
                    name: members[i].name,
                    status: members[i].authorization
                });
            }
        }
        onPictureCountChanged: {
            pictureCountDisplay.text = "Has been taken " + backend.pictureCount + "/6 pictures";
            finishButton.enabled = backend.pictureCount === 6;
        }

        onMagneticLockSignal: {
            doorSwitch.checked = magneticLockSignal;
        }

        onNewMemberSignal: {
            stackView.push(membersPage)
            python.list_all_members_gui()
        }

        onEditMemberSignal: {
            stackView.push(membersPage)
            python.list_all_members_gui()
        }

        onDeleteMemberSignal: {
            editMemberDialog.close()
            python.list_all_members_gui()
        }

    }

    // introPage layout
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

    // loginPage layout
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
                            python.login_button(
                                usernameField.text,
                                passwordField.text
                            )
                        }
                    }

                    Text {
                        id: forgotPasswordButton
                        text: "Default Login"
                        font.pointSize: 12
                        color: "black"  // Change text color to indicate it's clickable
                        Layout.alignment: Qt.AlignHCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                stackView.push(defaultPasswordPage)
                                // python.forgot_password_button()
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
            }
        }
    }

    // defaultPasswordPage layout
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
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
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
                    width: 300
                    height: 50
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 50
                    onClicked: {
                        python.default_login_button(
                            defaultUsernameField.text,
                            defaultPasswordField.text
                        )
                    }
                }
            }
        }
    }

    // registerPage layout
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
                    width: 300
                    height: 50
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 50
                    onClicked: {
                        python.register_button(
                            registerUsernameField.text,
                            registerPasswordField.text,
                            repeatPasswordField.text
                        )
                    }
                }
            }
        }
    }

    // mainPage layout
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

                    // palette {
                    //     highlighted: doorSwitch.checked ? "green" : "lightgrey"
                    //     base: "white"
                    // }

                    onCheckedChanged: {
                        python.on_lock_unlock()
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

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "transparent"
                    anchors.margins: 20


                    ListView {
                        id: activeMembersListView
                        anchors.fill: parent
                        anchors.margins: 20
                        model: activeMembersModel

                        // Add Header Row
                        header: RowLayout {
                            spacing: 10
                            width: parent.width

                            Text {
                                text: "Name"
                                font.bold: true
                                font.pixelSize: 18
                                Layout.alignment: Qt.AlignLeft
                            }

                            Text {
                                text: "Status"
                                font.bold: true
                                font.pixelSize: 18
                                Layout.alignment: Qt.AlignLeft
                            }
                        }

                        delegate: RowLayout {
                            spacing: 10
                            width: parent.width
                            height: 50

                            // Name Column
                            Text {
                                text: name
                                font.pixelSize: 16
                                Layout.alignment: Qt.AlignLeft
                            }

                            // Status Column
                            Rectangle {
                                color: status === "authorized" ? "lightgreen" :
                                        status === "temporary" ? "orange" : "lightcoral"
                                radius: 5
                                height: 20
                                width: 100
                                Layout.alignment: Qt.AlignLeft

                                Text {
                                    anchors.centerIn: parent
                                    text: status === "authorized" ? "has access" :
                                            status === "temporary" ? "temporary" : "no access"
                                    font.pixelSize: 14
                                    color: "white"
                                }
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
                            python.list_active_members_gui()
                        }
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
                        onClicked: {
                            stackView.push(membersPage)
                            python.list_all_members_gui()
                        }
                        width: 250
                        height: 80
                        Layout.preferredWidth: 250
                        Layout.preferredHeight: 80
                    }
                }

            }
        }
    }

    // settingsDialog layout
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
                spacing: 15
                anchors.margins: 20

                // Spacer to push content to the bottom
                Item {
                    Layout.fillHeight: true
                }

                // Change Password Text
                RowLayout {
                    Layout.alignment: Qt.AlignLeft
                    spacing: 10

                    Text {
                        text: "Change the password"
                        font.pointSize: 18
                        color: "black"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                changePasswordDialog.open()
                            }
                        }
                    }
                }

                // Logout Text
                RowLayout {
                    Layout.alignment: Qt.AlignLeft
                    spacing: 10

                    Text {
                        id: logoutButton
                        text: "Logout"
                        font.pointSize: 18
                        color: "black"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                stackView.push(loginPage)
                                settingsDialog.close()
                            }
                        }
                    }
                }
            }
        }
    }

    // changePasswordDialog layout
    Dialog {
        id: changePasswordDialog
        width: 400
        height: 600
        modal: true
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        visible: false
        anchors.centerIn: parent

        onAccepted: {
            python.change_password_button(
                currentPasswordField.text,
                newPasswordField.text,
                repeatNewPasswordField.text
            )
        }

        onRejected: {
            changePasswordDialog.close()
        }

        Rectangle {
            anchors.fill: parent
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                spacing: 10
                anchors.margins: 20  // Add padding inside the dialog

                Text {
                    text: "Change Password"
                    font.pointSize: 24
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }

                TextField {
                    id: currentPasswordField
                    placeholderText: "Current password"
                    Layout.fillWidth: true
                    font.pointSize: 18
                    echoMode: TextInput.Password
                    verticalAlignment: TextInput.AlignVCenter
                }

                TextField {
                    id: newPasswordField
                    placeholderText: "New password"
                    Layout.fillWidth: true
                    font.pointSize: 18
                    echoMode: TextInput.Password
                    verticalAlignment: TextInput.AlignVCenter
                }

                TextField {
                    id: repeatNewPasswordField
                    placeholderText: "Repeat new password"
                    Layout.fillWidth: true
                    font.pointSize: 18
                    echoMode: TextInput.Password
                    verticalAlignment: TextInput.AlignVCenter
                }
            }
        }
    }

    // membersPage layout
    Component {
        id: membersPage

        Rectangle {
            anchors.fill: parent
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                spacing: 20

                // Title
                Text {
                    text: "All the members"
                    font.pointSize: 24
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }

                // Wrapper for ListView
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "transparent"
                    anchors.margins: 20


                    ListView {
                        id: membersListView
                        anchors.fill: parent
                        anchors.margins: 20
                        model: membersModel

                        // Add Header Row
                        header: RowLayout {
                            spacing: 10
                            width: parent.width

                            Text {
                                text: "Name"
                                font.bold: true
                                font.pixelSize: 18
                                Layout.alignment: Qt.AlignLeft
                            }

                            Text {
                                text: "Status"
                                font.bold: true
                                font.pixelSize: 18
                                Layout.alignment: Qt.AlignLeft
                            }

                            Text {
                                text: "Edit"
                                font.bold: true
                                font.pixelSize: 18
                                Layout.alignment: Qt.AlignLeft
                            }
                        }

                        delegate: RowLayout {
                            spacing: 10
                            width: parent.width
                            height: 50

                            // Name Column
                            Text {
                                text: name
                                font.pixelSize: 16
                                Layout.alignment: Qt.AlignLeft
                            }

                            // Status Column
                            Rectangle {
                                color: status === "authorized" ? "lightgreen" :
                                        status === "temporary" ? "orange" : "lightcoral"
                                radius: 5
                                height: 20
                                width: 100
                                Layout.alignment: Qt.AlignLeft

                                Text {
                                    anchors.centerIn: parent
                                    text: status === "authorized" ? "has access" :
                                            status === "temporary" ? "temporary" : "no access"
                                    font.pixelSize: 14
                                    color: "white"
                                }
                            }

                            Button {
                                text: "Edit"
                                onClicked: {
                                    editMemberDialog.memberName = name
                                    editMemberDialog.memberStatus = status
                                    editMemberDialog.accessRemaining = access_remaining
                                    editMemberDialog.id = id;
                                    editMemberDialog.open()
                                }
                            }
                        }
                    }
                }

                Button {
                    text: "     +     "
                    font.pixelSize: 20
                    width: 100
                    height: 40
                    Layout.alignment: Qt.AlignHCenter
                    background: Rectangle {
                        radius: 10
                        border.color: "gray"
                        border.width: 1
                    }
                    onClicked: {
                        stackView.push(newMemberPage)
                        python.clear_pictures_directory()
                    }
                }

                // Navigation Buttons
                RowLayout {
                    Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
                    spacing: 20

                    Button {
                        icon.source: "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/.venv/images/home.png"
                        icon.width: 35
                        icon.height: 35
                        icon.color: "grey"
                        onClicked: {
                            stackView.push(mainPage)
                            python.list_active_members_gui()
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
                        onClicked: {
                            stackView.push(membersPage)
                            python.list_all_members_gui()
                        }
                        Layout.preferredWidth: 250
                        Layout.preferredHeight: 80
                    }
                }
            }
        }
    }

    // editMemberDialog layout
    Dialog {
        id: editMemberDialog
        width: 400
        height: 500
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        visible: false
        anchors.centerIn: parent

        // Action for OK Button
        onAccepted: {
            python.edit_member_button(
                editMemberDialog.id,
                statusComboBox.currentText
            )
        }

        // Action for Cancel Button
        onRejected: {
            editMemberDialog.close();  // Simply close the dialog
        }

        property string memberName: ""
        property string memberStatus: ""
        property string accessRemaining: ""
        property string id: ""

        Rectangle {
            color: "white"
            anchors.fill: parent
            anchors.centerIn: parent  // Center the rectangle within the dialog
            radius: 10  // Optional: Add rounded corners for a nice effect

            ColumnLayout {
                anchors.fill: parent
                anchors.centerIn: parent

                // Header
                Text {
                    text: "Edit Member"
                    font.bold: true
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }

                // Name Field
                RowLayout {
                    spacing: 10
                    Text {
                        text: "Name:"
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }
                    Text {
                        text: editMemberDialog.memberName
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }
                }

                // Status Field
                RowLayout {
                    spacing: 10
                    Text {
                        text: "Status:"
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }
                    Text {
                        text: editMemberDialog.memberStatus
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }
                }

                // Access Remaining Field
                RowLayout {
                    spacing: 10
                    Text {
                        text: "Access Remaining:"
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }
                    Text {
                        text: editMemberDialog.accessRemaining
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }
                }

                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    Text {
                        text: "Change status"
                        font.pointSize: 16
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        color: "black"
                    }

                    ComboBox {
                        id: statusComboBox
                        width: 300
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        model: ["always", "temporary", "no access"]

                        onCurrentIndexChanged: {
                            if (currentIndex === 1) { // Temporary selected
                                dateTimeDialog.open();
                            }
                        }
                    }
                }


                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 10

                    Button {
                        id: deleteMemberButton
                        text: "Delete"
                        font.pixelSize: 16
                        width: 120
                        height: 40
                        background: Rectangle {
                            color: "red"
                            radius: 8
                        }
                        contentItem: Text {
                            text: deleteMemberButton.text
                            color: "white"
                            font.pixelSize: 16
                            anchors.centerIn: parent
                        }
                        onClicked: {
                            // python.delete_member_button(editMemberDialog.id)
                            confirmDeleteMemberDialog.open()
                        }
                    }
                }
            }
        }
    }

    Dialog{
        id: confirmDeleteMemberDialog
        width: 300
        height: 300
        anchors.centerIn: parent
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel

        property string id: ""

        // Action for OK Button
        onAccepted: {
            python.delete_member_button(confirmDeleteMemberDialog.id)
        }

        // Action for Cancel Button
        onRejected: {
            confirmDeleteMemberDialog.close();  // Simply close the dialog
        }

        Rectangle {
            color: "white"
            anchors.fill: parent
            anchors.centerIn: parent  // Center the rectangle within the dialog
            radius: 10  // Optional: Add rounded corners for a nice effect

            ColumnLayout {
                anchors.fill: parent
                anchors.centerIn: parent

                // Header
                Text {
                    text: "Are you sure you want to delete a member?"
                    font.bold: true
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }

            }
        }
    }

    // newMemberPage layout
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
                    stackView.push(membersPage)
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


                Button {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    text: "Take Pictures 📷"

                    onClicked: {
                        stackView.push(cameraPage)
                    }
                }

                RowLayout {

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
                        model: ["always", "temporary"]

                        onCurrentIndexChanged: {
                            if (currentIndex === 1) { // Temporary selected
                                dateTimeDialog.open();
                            }
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
                    color: "lightgray"
                    radius: 10
                }
                onClicked: {
                    python.new_member_button(
                        newMemberNameField.text,
                        statusComboBox.currentText
                    )
                }
            }
        }
    }

    // dateTimeDialog layout
    Dialog {
        id: dateTimeDialog
        modal: true
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        width: 500
        height: 600
        anchors.centerIn: parent

        // Action for OK Button
        onAccepted: {
            python.get_date_button(
                yearComboBox.model.get(yearComboBox.currentIndex).text,
                monthComboBox.currentIndex + 1,  // Months are 0-based
                dayComboBox.model.get(dayComboBox.currentIndex).text,
                hourSpinBox.value,
                minuteSpinBox.value
            )
            dateTimeDialog.close();
        }

        // Action for Cancel Button
        onRejected: {
            dateTimeDialog.close();  // Simply close the dialog
        }

        Rectangle {
            anchors.fill: parent
            color: "white"

            ColumnLayout {
                spacing: 15
                anchors.fill: parent
                anchors.margins: 20

                // Back Button
                Button {
                    text: "←"
                    font.pointSize: 20
                    background: Rectangle {
                        color: "transparent"
                    }
                    onClicked: {
                        dateTimeDialog.visible = false
                    }
                }

                // Date Selection
                Text {
                    text: "Select Date"
                    font.pointSize: 18
                    color: "black"
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    spacing: 10
                    Layout.alignment: Qt.AlignHCenter

                    ComboBox {
                        id: dayComboBox
                        model: ListModel {
                            Component.onCompleted: {
                                for (let i = 1; i <= 31; i++) {
                                    append({"text": i})
                                }
                            }
                        }
                        currentIndex: 0
                        displayText: model.get(currentIndex).text
                        width: 30
                    }

                    ComboBox {
                        id: monthComboBox
                        model: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                        currentIndex: 0
                        displayText: model[currentIndex]
                        width: 120
                    }

                    ComboBox {
                        id: yearComboBox
                        model: ListModel {
                            Component.onCompleted: {
                                for (let i = 2025; i <= 2030; i++) {
                                    append({"text": i})
                                }
                            }
                        }
                        currentIndex: 0
                        displayText: model.get(currentIndex).text
                        width: 60
                    }
                }

                // Time Selection
                Text {
                    text: "Select Time"
                    font.pointSize: 18
                    color: "black"
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    spacing: 10
                    Layout.alignment: Qt.AlignHCenter

                    SpinBox {
                        id: hourSpinBox
                        from: 0
                        to: 23
                        value: 12
                        width: 60
                    }

                    Text {
                        text: ":"
                        font.pointSize: 18
                    }

                    SpinBox {
                        id: minuteSpinBox
                        from: 0
                        to: 59
                        value: 0
                        width: 60
                    }
                }
            }
        }
    }

    // cameraPage layout
    Component {
        id: cameraPage

        Rectangle {
            anchors.fill: parent
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 10

                // Title Text
                Text {
                    text: "Take 6 Pictures"
                    font.pixelSize: 24
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    text: "To take a picture please press c"
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Text {
                    text: "To quite the camera press q"
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                // Take Picture Button
                Button {
                    text: "Take Picture"
                    anchors.centerIn: parent
                    onClicked: {
                        python.take_picture()  // Call the Python function to capture and save a picture
                    }
                }

                // Picture Count Text
                Text {
                    id: pictureCountDisplay
                    text: "Has been taken " + python.pictureCount + "/6 pictures"
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                // Finish and Cancel Buttons Row
                RowLayout {
                    spacing: 20
                    anchors.horizontalCenter: parent.horizontalCenter

                    Button {
                        id: finishButton
                        text: "Finish"
                        enabled: backend.pictureCount === 6  // Enable only when 6 pictures are present
                        onClicked: {
                            console.log("Finish button clicked!");
                            stackView.push(newMemberPage)
                        }
                    }

                    Button {
                        id: cancelButton
                        text: "Cancel"
                        onClicked: {
                            python.clear_pictures_directory()
                            stackView.push(newMemberPage)
                        }
                    }
                }
            }
        }
    }


}
