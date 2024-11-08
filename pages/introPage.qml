// introPage.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtMultimedia

Rectangle{
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
          mainWindow.navigateTo("loginPage.qml")
      }
}