QML = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia


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
               anchors.horizontalCenter: parent.horizontalCenter
               anchors.verticalCenter: parent.verticalCenter
               spacing: 20  
    
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
                               python.on_forgot_password_button_click()
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
                   text: "Please press the button on the lock manually."
                   modal: true
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
                text: "Take Pictures"
                
                onClicked: {
                    python.open_camera_and_take_pictures()
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
  }

  Component {
    id: addPicturesPage

    Rectangle {
        anchors.fill: parent
        color: "white"
        
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

        ColumnLayout {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            spacing: 20 

            Text {
                text: "Please make 6 pictures from different angles"
                font.pointSize: 20
                font.bold: true
                color: "black"
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: picturePreview
                width: 300
                height: 300
                color: "#f0f0f0"
                border.color: "gray"
                border.width: 1

                Text {
                    text: "Picture Preview"
                    anchors.centerIn: parent
                    color: "gray"
                }
            }

            Button {
                text: "Take Pictures"
                Layout.alignment: Qt.AlignHCenter
                onClicked: {
                    // Call the Python function to open the camera and take pictures
                    python.open_camera_and_take_pictures()
                }
            }

            Button {
                text: "Done"
                Layout.alignment: Qt.AlignHCenter
                onClicked: {
                    stackView.pop() 
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
           anchors.margins: 20  

           Text {
               id: settingsButton
               text: "☰"
               font.pointSize: 40
               color: "grey"
               Layout.alignment: Qt.AlignLeft
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
                  python.on_lock_unlock_button_click(doorSwitch.checked)
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
        height: 350
        modal: true
        visible: false
    
        Rectangle {
            anchors.fill: parent
            color: "white"
            radius: 10  // Optional: rounded corners
    
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 10
    
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
                        python.on_change_password_button_click(
                            currentPasswordField.text, 
                            newPasswordField.text, 
                            repeatNewPasswordField.text
                        )
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
            anchors.margins: 20  // Margins around the ColumnLayout

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
                Layout.alignment: Qt.AlignLeft
                Text {
                    id: settingsButton
                    text: "+"
                    font.pointSize: 40
                    color: "grey"
                    Layout.alignment: Qt.AlignLeft
                    MouseArea {
                        anchors.fill: parent  
                        onClicked: newUserDialog.open()
                    }
                }
            }

            // Bottom Navigation Bar
            RowLayout {
                Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
                anchors.margins: 20

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
                    height: 35
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
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10
    
            Text {
                id: editUserText
                font.pointSize: 20
                horizontalAlignment: Text.AlignHCenter
            }
    
            // Field for editing the member name
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
    
                // Save logic
                onClicked: {
                    // Get the new name and status
                    var newName = editUserField.text
                    var newStatus = statusComboBox.currentText
    
                    // Call Python functions to update member name and status
                    python.change_member(editUserDialog.userName, newName)
                    python.change_member_status(editUserDialog.userName, newStatus === "In")
                    
                    // Close the dialog
                    editUserDialog.close()
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
          spacing: 20

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
                text: "Take Pictures"
                
                onClicked: {
                    python.open_camera_and_take_pictures()
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
   }
   
}
"""
