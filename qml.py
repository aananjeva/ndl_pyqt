QML = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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
               onClicked: stackView.push(loginPage) // Fixed: Added the missing parenthesis here
           }
       }
   }


    Component {
    id: loginPage

    Rectangle {
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

            // Use a ColumnLayout to stack the buttons vertically
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
                        console.log("Logging in with username:", usernameField.text)
                        stackView.push(mainPage)  // Navigate to main page
                    }
                }

                Button {
                    Layout.alignment: Qt.AlignHCenter
                    text: "Register"
                    width: 300  
                    height: 50  
                    Layout.preferredWidth: 300  
                    Layout.preferredHeight: 50
                    onClicked: stackView.push(registerPage)  // Navigate to register page
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


       ColumnLayout {
           anchors.horizontalCenter: parent.horizontalCenter
           anchors.verticalCenter: parent.verticalCenter
           spacing: 20   // Space between elements


           Button {
               text: "←"  // You can replace this with an icon if you prefer
               font.pointSize: 20
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
                       console.log("Registering username:", registerUsernameField.text)
                       stackView.push(mainPage)
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
            anchors.margins: 20  // Margins around the ColumnLayout

            // Settings Button
            Button {
                text: "☰"
                width: 100
                height: 40
                onClicked: settingsDialog.open()  // Open the settings dialog
            }

            // Door Status Text
            Text {
                id: doorStatusText
                text: "The door is unlocked"
                font.bold: true
                font.pointSize: 24
                horizontalAlignment: Text.AlignHCenter
                color: "black" 
                Layout.alignment: Qt.AlignHCenter
            }

            // Switch for Door Status
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

            // List of Active Users
            ColumnLayout {
                spacing: 10  // Space between user entries
                Layout.alignment: Qt.AlignHCenter

                // Replace these with dynamic entries if needed
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

                // Add more users as needed
            }

            // Bottom Navigation Bar
            RowLayout {
                Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter 
                anchors.margins: 20  // Margins for the navigation bar

                Button {
                    text: "Home"
                    onClicked: stackView.push()  
                    width: 250  
                    height: 80  
                    Layout.preferredWidth: 250  
                    Layout.preferredHeight: 80
                }

                Button {
                    text: "Members"
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
        anchors.fill: parent
        color: "white" // Background color
        radius: 10 // Optional: rounded corners

        ColumnLayout {
            anchors.fill: parent
            spacing: 20
            anchors.margins: 20

            Text {
                text: "Settings"
                font.pointSize: 24
                font.bold: true
                color: "black"
                horizontalAlignment: Text.AlignHCenter
                Layout.alignment: Qt.AlignLeft
            }

            // Add your settings options here
            Text {
                text: "Option 1"
                font.pointSize: 18
                color: "black"
                Layout.alignment: Qt.AlignLeft
            }

            Text {
                text: "Option 2"
                font.pointSize: 18
                color: "black"
                Layout.alignment: Qt.AlignLeft
            }

        }
    }

   

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
                anchors.margins: 20  // Margins around the ColumnLayout

                // Title
                Text {
                    text: "All the members"
                    font.pointSize: 24
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    color: "black"
                    Layout.alignment: Qt.AlignHCenter
                }

                // List of Users
                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 10  // Space between user entries

                    // Example User Entries
                    Repeater {
                        model: 5  // Replace with the actual model of members

                        RowLayout {
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
                }

                // + Button to open the dialog
                RowLayout {
                    Layout.alignment: Qt.AlignLeft
                    Button {
                        text: "+"
                        font.pointSize: 30
                        width: 60
                        height: 60
                        onClicked: newUserDialog.open()  // Open the dialog
                    }
                }
                
                RowLayout {
                   Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
                   anchors.margins: 20  // Margins for the navigation bar


                Button {
                   text: "Home"
                   onClicked: stackView.push(mainPage)  
                   width: 250  
                   height: 80  
                   Layout.preferredWidth: 250  
                   Layout.preferredHeight: 80
                }


                Button {
                   text: "Members"
                   onClicked: stackView.push() 
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

            Button {
                text: "Cancel"
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
                onClicked: editUserDialog.close()
            }
        }

        onOpened: {
           editUserText.text = "Editing: " + editUserDialog.userName // Update dialog title
           editUserField.text = editUserDialog.userName // Pre-fill the field
        }
    }
    
    Dialog {
        id: newUserDialog
        width: 400
        height: 599
        modal: true  // Ensures it's modal (blocks interaction with the background)
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
                   }
               }
           } 
    } 
}
"""
