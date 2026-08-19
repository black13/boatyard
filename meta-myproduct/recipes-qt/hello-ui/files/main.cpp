// the platform pattern in miniature:
//   ui_app    = QtQuick/QML window   (this)
//   server_app = QtCore headless     (hello daemon from §3)
// The UI is a QML scene; services are separate processes on DBus.

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

int main(int argc, char *argv[])
{
    // Qt 5.6-era style: set attributes before the app object.
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/Main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
