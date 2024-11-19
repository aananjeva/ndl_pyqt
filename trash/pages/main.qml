import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 640
    height: 480

    Loader {
        id: pageLoader
        anchors.fill: parent
        source: "introPage.qml"
    }

    function navigateTo(page) {
        pageLoader.source = page; // Load the new page
    }

}
