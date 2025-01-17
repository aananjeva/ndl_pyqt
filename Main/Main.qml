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
        onLoginSuccess: {
            stackView.push(mainPage)
            python.list_active_members_gui()
            python.lock_listener()
        }

        onRegisterSuccess: {
            stackView.push(mainPage)
            python.list_active_members_gui()
            python.lock_listener()
        }

        onDefaultLoginSuccess: {
            stackView.push(mainPage)
            python.list_active_members_gui()
            python.lock_listener()
        }

        onChangePasswordSignal: {
            changePasswordDialog.close()
            stackView.push(loginPage)
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
            pictureCountDisplay.text = "Has been taken " + backend.pictureCount + "/4 pictures";
            finishButton.enabled = backend.pictureCount === 4;
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

        onSaveDateSignal: {
            dateTimeDialog.close()
        }

    }

    // introPage layout PERFECT
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

    // loginPage layout PERFECT
    Component {
        id: loginPage

        Rectangle {
            anchors.fill: parent
            color: "white"

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 20

                // Title Text
                Text {
                    text: "Welcome to SmartLock"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    font.pointSize: 24
                    font.bold: true
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                }

                // Username Field
                Rectangle {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    width: 300
                    height: 35
                    color: "#f5f5f5" // Light grey background
                    radius: 8        // Rounded corners
                    border.color: "#dcdcdc"
                    border.width: 1

                    TextField {
                        id: usernameField
                        placeholderText: "username"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 16
                        verticalAlignment: TextInput.AlignVCenter
                        background: Rectangle {
                            color: "transparent" // Keeps parent background visible
                        }
                    }
                }


                Rectangle {
                    width: 300
                    height: 50
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: passwordField
                            placeholderText: "password"
                            Layout.fillWidth: true
                            font.pointSize: 16
                            echoMode: passwordVisibilityButton1.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton1
                            checkable: true
                            text: passwordVisibilityButton1.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton1.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }


                // Login Button
                ColumnLayout {
                    spacing: 10
                    Layout.alignment: Qt.AlignHCenter

                    Button {
                        text: "login"
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 50
                        font.pointSize: 16
                        background: Rectangle {
                            color: "#DAF1DE" // Light green
                            radius: 8
                        }
                        onClicked: {
                            python.login_button(
                                usernameField.text,
                                passwordField.text
                            )
                        }
                    }


                    // Default Login
                    Text {
                        id: forgotPasswordButton
                        text: "\n\n\n\n\n\n\nDefault Login"
                        font.pointSize: 12
                        color: "black"
                        Layout.alignment: Qt.AlignHCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                stackView.push(defaultPasswordPage)
                            }
                        }
                    }

                    // Register Page Link
                    Text {
                        id: registerButton
                        text: "I do not have an account"
                        font.pointSize: 12
                        color: "black"
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

    // defaultPasswordPage layout PERFECT
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
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    width: 300
                    height: 35
                    color: "#f5f5f5"
                    radius: 8
                    border.color: "#dcdcdc"
                    border.width: 1

                    TextField {
                        id: defaultUsernameField
                        placeholderText: "default username"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 16
                        verticalAlignment: TextInput.AlignVCenter
                        background: Rectangle {
                            color: "transparent" // Keeps parent background visible
                        }
                    }
                }

                Rectangle {
                    width: 300
                    height: 50
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: defaultPasswordField
                            placeholderText: "password"
                            Layout.fillWidth: true
                            font.pointSize: 16
                            echoMode: passwordVisibilityButton2.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton2
                            checkable: true
                            text: passwordVisibilityButton2.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton2.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }


                Button {
                    text: "enter"
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 50
                    font.pointSize: 16
                    background: Rectangle {
                        color: "#DAF1DE" // Light green
                        radius: 8
                    }
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

    // registerPage layout PERFECT
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
                spacing: 20
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
                    height: 35
                    color: "#f5f5f5"
                    radius: 8
                    border.color: "#dcdcdc"
                    border.width: 1

                    TextField {
                        id: registerUsernameField
                        placeholderText: "username"
                        anchors.fill: parent
                        padding: 10
                        font.pointSize: 16
                        verticalAlignment: TextInput.AlignVCenter
                        background: Rectangle {
                            color: "transparent" // Keeps parent background visible
                        }
                    }
                }

                Rectangle {
                    width: 300
                    height: 50
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: registerPasswordField
                            placeholderText: "password"
                            Layout.fillWidth: true
                            font.pointSize: 16
                            echoMode: passwordVisibilityButton3.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton3
                            checkable: true
                            text: passwordVisibilityButton3.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton3.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }


                Rectangle {
                    width: 300
                    height: 50
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: repeatPasswordField
                            placeholderText: "password"
                            Layout.fillWidth: true
                            font.pointSize: 16
                            echoMode: passwordVisibilityButton4.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton4
                            checkable: true
                            text: passwordVisibilityButton4.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton4.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }


                Button {
                    text: "Register"
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 50
                    font.pointSize: 16
                    background: Rectangle {
                        color: "#DAF1DE" // Light green
                        radius: 8
                    }
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

            Connections {
                target: python
                onMagneticLockSignal: function (magneticLockSignal) {
                    doorSwitch.checked = magneticLockSignal
                }
            }

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
                    text: "SmartLock System"
                    font.bold: true
                    font.pointSize: 24
                    horizontalAlignment: Text.AlignHCenter
                    color: "black"
                    Layout.alignment: Qt.AlignHCenter
                }

                Switch {
                    id: doorSwitch
                    scale: 1.5
                    checked: false
                    Layout.alignment: Qt.AlignHCenter

                    onCheckedChanged: {
                        python.on_lock_unlock()
                    }
                }

                Text {
                    text: doorSwitch.checked ? "open" : "close"
                    font.pointSize: 14
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }


                Text {
                    text: "The last active member:"
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
                            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter

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
                            // python.get_current_datetime()
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

    // settingsDialog layout PERFECT
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

    // changePasswordDialog layout PERFECT
    Dialog {
        id: changePasswordDialog
        width: 400
        height: 600
        modal: true
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        visible: false
        anchors.centerIn: parent

        function resetFields() {
            currentPasswordField.text = "";
            newPasswordField.text = "";
            repeatNewPasswordField.text = "";
        }

        onVisibleChanged: {
            if (visible) resetFields();
        }

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
                spacing: 20
                anchors.centerIn: parent

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
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: currentPasswordField
                            placeholderText: "password"
                            Layout.fillWidth: true
                            font.pointSize: 18
                            echoMode: passwordVisibilityButton5.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton5
                            checkable: true
                            text: passwordVisibilityButton5.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton5.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }


                Rectangle {
                    width: 300
                    height: 50
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: newPasswordField
                            placeholderText: "new password"
                            Layout.fillWidth: true
                            font.pointSize: 18
                            echoMode: passwordVisibilityButton6.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton6
                            checkable: true
                            text: passwordVisibilityButton6.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton6.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }


                Rectangle {
                    width: 300
                    height: 50
                    color: "transparent"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RowLayout {
                        anchors.fill: parent
                        spacing: 5

                        TextField {
                            id: repeatNewPasswordField
                            placeholderText: "repeat password"
                            Layout.fillWidth: true
                            font.pointSize: 18
                            echoMode: passwordVisibilityButton7.checked ? TextInput.Normal : TextInput.Password
                            verticalAlignment: TextInput.AlignVCenter
                            background: Rectangle {
                                color: "#f5f5f5"
                                radius: 8
                                border.color: "#dcdcdc"
                                border.width: 1
                            }
                        }

                        Button {
                            id: passwordVisibilityButton7
                            checkable: true
                            text: passwordVisibilityButton7.checked ? "🔓" : "🔒"
                            font.pixelSize: 16
                            background: Rectangle {
                                color: "transparent"
                            }
                            ToolTip.text: passwordVisibilityButton7.checked ? "Hide Password" : "Show Password"
                            ToolTip.visible: hovered
                        }
                    }
                }

            }
        }
    }

    // membersPage layout GOOD
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
                            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter

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
                                text: "  edit  "
                                font.pixelSize: 14
                                width: 100
                                height: 40
                                Layout.alignment: Qt.AlignHCenter
                                background: Rectangle {
                                    radius: 10
                                    color: "lightgray"
                                    border.color: "lightgray"
                                    border.width: 1
                                }
                                onClicked: {
                                    editMemberDialog.memberName = name
                                    editMemberDialog.memberStatus = status
                                    editMemberDialog.accessRemaining = access_remaining
                                    editMemberDialog.id = id;
                                    editMemberDialog.open()
                                    python.get_current_datetime()
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
                        color: "lightgray"
                        border.color: "lightgray"
                        border.width: 1
                    }
                    onClicked: {
                        stackView.push(newMemberPage)
                        python.clear_pictures_directory()
                        python.get_current_datetime()
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

    // editMemberDialog layout GOOD
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
                spacing: 5

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
                    Layout.alignment: Qt.AlignHCenter
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
                    Layout.alignment: Qt.AlignHCenter
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
                    Layout.alignment: Qt.AlignHCenter
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

    // confirmMemberDeleteDialog layout PERFECT
    Dialog {
        id: confirmDeleteMemberDialog
        width: 300
        height: 300
        anchors.centerIn: parent
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel


        // Action for OK Button
        onAccepted: {
            python.delete_member_button(editMemberDialog.id)
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
                    text: "Are you sure you want\nto delete a member?"
                    font.pixelSize: 15
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }

            }
        }
    }

    // newMemberPage layout GOOD
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

                Text {
                    text: "Please first take the pictures\nand then add a name"
                    font.pointSize: 15
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "black"
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
                        placeholderText: "name"
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

                Text {
                    text: "You will have to wait 45 seconds\nfor new member to be created"
                    font.pointSize: 15
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "black"
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

    // dateTimeDialog layout PERFECT
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
        }

        // Action for Cancel Button
        onRejected: {
            dateTimeDialog.close();  // Simply close the dialog
        }

        Rectangle {
            anchors.fill: parent
            color: "#F9FAFB"

            ColumnLayout {
                spacing: 15
                anchors.fill: parent
                anchors.margins: 20


                // Date Selection
                Text {
                    text: "Select Date & Time"
                    font.pointSize: 22
                    font.bold: true
                    color: "black"
                    Layout.alignment: Qt.AlignHCenter
                }

                ColumnLayout {
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

    // cameraPage layout PERFECT
    Component {
        id: cameraPage

        Rectangle {
            anchors.fill: parent
            color: "white"

            Column {
                anchors.centerIn: parent
                spacing: 15
                width: parent.width * 0.8

                // Title Text
                Text {
                    text: "📸 Take 4 Pictures"
                    font.pixelSize: 24
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#2c3e50"
                }

                // Instructions Text
                Text {
                    text: "• Press 'C' to take a picture\n• Press 'Q' to quit the camera"
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#7f8c8d"
                }

                // Take Picture Button
                Button {
                    text: "Take Picture"
                    width: parent.width * 0.6
                    height: 40
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pixelSize: 16
                    onClicked: {
                        python.take_picture()
                    }
                }

                // Picture Count Display
                Text {
                    id: pictureCountDisplay
                    text: "Pictures taken: " + python.pictureCount + "/4"
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#34495e"
                }

                // Finish and Cancel Buttons
                RowLayout {
                    spacing: 10
                    anchors.horizontalCenter: parent.horizontalCenter

                    Button {
                        id: finishButton
                        text: "Finish"
                        width: 120
                        enabled: backend.pictureCount === 4
                        font.pixelSize: 14
                        onClicked: {
                            console.log("Finish button clicked!");
                            stackView.push(newMemberPage)
                        }
                    }

                    Button {
                        id: cancelButton
                        text: "Cancel"
                        width: 120
                        font.pixelSize: 14
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
