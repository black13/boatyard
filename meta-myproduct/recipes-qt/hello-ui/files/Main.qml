// The chartplotter UI in miniature: a QML scene with a "sonar-ish" canvas,
// driving a shader-style effect the way the real ui_app renders DSP textures.
// Run under Weston (qwayland-egl) or eglfs — both are in the image.

import QtQuick 2.6

Rectangle {
    width: 800
    height: 480
    color: "#0a0e14"

    // Top bar — the "kiosk chrome"
    Rectangle {
        id: topbar
        anchors { top: parent.top; left: parent.left; right: parent.right }
        height: 44
        color: "#151b26"
        Text {
            anchors.centerIn: parent
            text: "hello-ui — Qt 5 on embedded"
            color: "#7fd0ff"
            font.pixelSize: 18
        }
    }

    // A fake scrolling echo trace — where sonar would draw
    Canvas {
        id: trace
        anchors {
            top: topbar.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        property real t: 0
        onPaint: {
            var ctx = getContext("2d");
            ctx.fillStyle = "#0a0e14";
            ctx.fillRect(0, 0, width, height);
            ctx.strokeStyle = "#3adf8a";
            ctx.lineWidth = 2;
            ctx.beginPath();
            for (var x = 0; x < width; x += 4) {
                var y = height/2 + Math.sin((x + t) * 0.03) * height * 0.3;
                if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            }
            ctx.stroke();
        }
        NumberAnimation on t {
            from: 0; to: 600; duration: 6000; loops: Animation.Infinite
        }
        onTChanged: trace.requestPaint()
    }

    // Bottom status — the "shared variables" readout in miniature
    Rectangle {
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right }
        height: 28
        color: "#151b26"
        Text {
            anchors.centerIn: parent
            text: "slot boot · Qt " + Qt.runtimeVersion + " · " + Qt.platform.pluginName
            color: "#5a6a80"
            font.pixelSize: 12
        }
    }
}
