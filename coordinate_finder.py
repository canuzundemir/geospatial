from qgis.core import QgsRectangle, QgsVectorLayer, QgsMapLayerProxyModel
from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem
from qgis.gui import QgsMapTool, QgsRubberBand
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class RectangleMapTool(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.startPoint = None
        self.endPoint = None

    def canvasPressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = self.toMapCoordinates(event.pos())
            self.endPoint = None
            event.accept()

    def canvasMoveEvent(self, event):
        if self.startPoint and not self.endPoint:
            self.endPoint = self.toMapCoordinates(event.pos())
            self.updateRubberBand()
            event.accept()

    def canvasReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.startPoint and self.endPoint:
            self.endPoint = self.toMapCoordinates(event.pos())
            self.updateRubberBand()
            self.processRectangle()
            self.startPoint = None
            self.endPoint = None
            event.accept()

    def showRubberBand(self):
        if self.rubberBand is None:
            self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
            self.rubberBand.setColor(QColor(255, 0, 0, 100))
            self.rubberBand.setWidth(1)
        self.updateRubberBand()
        self.rubberBand.show()

    def updateRubberBand(self):
        if self.rubberBand is not None and self.startPoint and self.endPoint:
            self.rubberBand.setToGeometry(QgsGeometry.fromRect(QgsRectangle(self.startPoint, self.endPoint)), None)

    def processRectangle(self):
        if self.startPoint and self.endPoint:
            extent = QgsRectangle(self.startPoint, self.endPoint)
            source_crs = self.canvas.mapSettings().destinationCrs()
            target_crs = QgsCoordinateReferenceSystem(4326)  # WGS84
            transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
            extent_transformed = transform.transformBoundingBox(extent)

            coordinates = f"[[[{extent_transformed.xMinimum()}, {extent_transformed.yMinimum()}],\n" \
                        f" [{extent_transformed.xMinimum()}, {extent_transformed.yMaximum()}],\n" \
                        f" [{extent_transformed.xMaximum()}, {extent_transformed.yMaximum()}],\n" \
                        f" [{extent_transformed.xMaximum()}, {extent_transformed.yMinimum()}]]]"

            print(f"Extent coordinates: {coordinates}")


    def activate(self):
        self.showRubberBand()

    def deactivate(self):
        if self.rubberBand is not None:
            self.rubberBand.hide()

canvas = iface.mapCanvas()
rectangle_tool = RectangleMapTool(canvas)
canvas.setMapTool(rectangle_tool)
canvas.refreshAllLayers()
