import klayout.db as db
import klayout.lib
import numpy as np
import os
import importlib.resources
from . import alignment

lib_basic = db.Library.library_by_name("Basic")
ly = db.Layout()
# sets unit to micrometer
LY_DBU = ly.dbu


def export_layer_gds(filename):
    for layer_index, layer_info in zip(ly.layer_indexes(), ly.layer_infos()):
        parameters_saving = db.SaveLayoutOptions()
        parameters_saving.add_layer(layer_index, layer_info)
        ly.write(filename+'_layer'+str(layer_index)+'.gds', parameters_saving)


def export_design_gds(filename):
    ly.write(filename+'.gds')

# sets path of alignment mark files
with importlib.resources.path(alignment, "alignment_square.GDS") as p:
    ALIGN_SQUARE_PATH = str(p)


class AbstractPolygon:
    def __init__(self, name: str, polygonDB, centered=True):
        """
        AbstractPolygon is the parent class of different types of polygons (rectangle, circles).
        It is an abstract class and never directly instantiated.

        :param name: Name of the AbstractPolygon
        :type name: str
        :param polygon: created polygon object
        :type polygon: db.Polygon
        :param centered: specifies if the object is drawn from its geometrical center (True) or from the bottom left corner (False)
        :type centered: bool
        """
        self.name = name
        self.centered = centered
        self.polygonDB = polygonDB

    def transformation(self, dx, dy, rotation=0, magnitude=1, mirrorx=False):
        """
        Transformation allows to move, rotate, magnify and mirror a polygon or text

        :param dx: Movement in x direction in um
        :type dx: int
        :param dy: Movement in y direction in um
        :type dy: int
        :param rotation: Rotation in degree
        :type rotation: int
        :param magnitude: Magnifying factor
        :type magnitude: int
        :param mirrorx: Mirror in x direction
        :type mirrorx: bool
        """
        complex_transformation = db.ICplxTrans(magnitude, rotation, mirrorx, int(dx/LY_DBU), int(dy/LY_DBU))
        if hasattr(self, 'polygonDB'):
            self.polygonDB.transform(complex_transformation)
        else:
            self.regionDB.transform(complex_transformation)


class Rectangle(AbstractPolygon):
    def __init__(self, name: str, x: float, y: float, centered=True):
        """
        Rectangle class inherits from AbstractPolygon class and allows to create a rectangular polygon.

        :param name: name of the rectangular polygon object
        :type name: str
        :param x: width of the rectangle
        :type x: float
        :param y: height of the rectangle
        :type y: float
        :param centered: specifies if the object is drawn from its geometrical center (True) or from the bottom left corner (False)
        :type centered: bool
        """
        self.x = x
        self.y = y
        self.centered = centered

        x_um = self.x/LY_DBU
        y_um = self.y/LY_DBU
        if self.centered:
            point_rectangle = [db.DPoint(-x_um/2, -y_um/2), db.DPoint(x_um/2, -y_um/2),
                               db.DPoint(x_um/2, y_um/2), db.DPoint(-x_um/2, y_um/2)]
        else:
            point_rectangle = [db.DPoint(0, 0), db.DPoint(x_um, 0), db.DPoint(x_um, y_um), db.DPoint(0, y_um)]

        self.polygonDB = db.Polygon(point_rectangle)
        super().__init__(name, self.polygonDB, centered)


class Circle(AbstractPolygon):

    def __init__(self, name: str, radius: float, centered=True, nr_points=64):
        """
        Circle class allows to create a circular polygon object and inherits from AbstractPolygon class.

        :param name: name of the circular polygon object
        :type name: str
        :param radius: radius of circle
        :type radius: float
        :param centered: specifies if the object is drawn from its geometrical center (True), always True for circle
        :type centered: bool
        :param nr_points: number of points used to draw the circular polygon
        :type nr_points: int
        """
        self.radius = radius
        self.nr_points = nr_points

        radius = self.radius/LY_DBU
        angles = np.linspace(0, 2*np.pi, self.nr_points + 1)[0:-1]
        points = []  # array of points
        for angle in angles:
            points.append(db.Point(radius*np.cos(angle), radius*np.sin(angle)))
        self.polygonDB = db.Polygon(points)
        super().__init__(name, self.polygonDB, centered)


class Region:
    def __init__(self, polygon_object_list):
        """
        Region class allows to create regions from a list of polygons (such as rectangle or circle).
        Regions can be used for boolean operations.

        :param polygon_object_list: List of Polygon
        :type polygon_object_list:
        """
        self.polygonDB_list = [polygon_object.polygonDB for polygon_object in polygon_object_list]
        self.regionDB = db.Region(self.polygonDB_list)

    def subtract(self, region_to_subtract):
        """
        Subtract a region from another one. The boolean result is stored in the original region.

        :param region_to_subtract: Region to subtract from the original region.
        :type region_to_subtract: Region
        """
        self.regionDB = self.regionDB - region_to_subtract.regionDB

    def add(self, region_to_add):
        """
        Add a region from another one. The boolean result is stored in the original region.

        :param region_to_add: Region to add from the original region.
        :type region_to_add: Region
        """
        self.regionDB = self.regionDB + region_to_add.regionDB


class Cell:
    # doc string
    def __init__(self, name: str, gds_path=''):
        """
        A cell is one of the building blocks of the layout. It can contain any type of object (polygon, region, text, etc...).

        :param name: Name of the cell
        :type name: str
        :param gds_path: GDS path when importing external .gds file, such as alignment mark.
        :type gds_path: full_path
        """
        if gds_path:
            # https://www.klayout.org/klayout-pypi/examples/layout_merge/
            ly_import = db.Layout()
            ly_import.read(gds_path)
            imported_top_cell = ly_import.top_cell()

            self.name = name
            gds_cell = ly.create_cell(self.name)
            gds_cell.copy_tree(imported_top_cell)

            # frees the resources of the imported layout
            ly_import._destroy()

            self.layers = {}  # dict with layers as keys
            self.cell = gds_cell
        else:
            self.name = name
            self.layers = {}  # dict with layers as keys
            self.cell = ly.create_cell(self.name)

    def draw_polygon(self, polygon_object, target_layer):
        """
        Draw a polygon on the cell in the specified layer.

        :param polygon_object: Polygon object (rectangle, circle) to draw
        :type polygon_object: Polygon
        :param target_layer: Layer to draw the object in
        :type target_layer: int
        """
        self.cell.shapes(target_layer).insert(polygon_object.polygonDB)
        # it would be nice if we could add multiple polygons at the same time/to multiple layers at the same time

    def draw_path(self, path_object, target_layer):
        """
        Draw a path on the cell in the specified layer.

        :param path_object: Path object to draw
        :type path_object: Path
        :param target_layer: Layer to draw the object in
        :type target_layer: int
        """
        self.cell.shapes(target_layer).insert(path_object.path)

    def draw_region(self, region, target_layer):
        """
        Draw a region on the cell in the specified layer.

        :param region: Region to draw
        :type region: db.Region
        :param target_layer: Layer to draw the object in
        :type target_layer: int
        """
        self.cell.shapes(target_layer).insert(region.regionDB)

    def draw_text(self, text_region, target_layer):
        """
        Draw a text on the cell in the specified layer.

        :param text_region: Text to draw
        :type text_region: db.Region
        :param target_layer: Layer to draw the object in
        :type target_layer: layer object
        """
        self.cell.shapes(target_layer).insert(text_region.regionDB)

    def insert_cell(self, cell_to_insert, origin_x=0, origin_y=0, magnitude=1, rotation=0, mirrorx=False):
        """
        Insert a cell in the current cell. The inserted cell can be placed, rotated, magnified and mirrored.

        :param cell_to_insert: Cell to insert in the current cell
        :type cell_to_insert: Cell
        :param origin_x: x coordinate in the current cell of the center of the inserted cell in um
        :type origin_x: int
        :param origin_y: y coordinate in the current cell of the center of the inserted cell in um
        :type origin_y: int
        :param magnitude: Magnification of the cell
        :type magnitude: int
        :param rotation: Rotation in degree
        :type rotation: int
        :param mirrorx: Mirror in x direction
        :type mirrorx: bool
        """
        complex_transformation = db.ICplxTrans(magnitude, rotation, mirrorx, int(origin_x/LY_DBU),
                                               int(origin_y/LY_DBU))
        cell_instance = db.CellInstArray(cell_to_insert.cell.cell_index(), complex_transformation)
        self.cell.insert(cell_instance)

    def insert_cell_array(self, cell_to_insert, x_row, y_row, x_column, y_column, n_row: int, n_column: int,
                          origin_x=0, origin_y=0, magnitude=1, rotation=0, mirrorx=False):
        """
        Insert an array of cell in the current cell. The inserted cell can be placed, rotated, magnified and mirrored.

        :param cell_to_insert: Cell to insert in the current cell
        :type cell_to_insert: Cell
        :param x_row: x coordinate of row vector in um
        :type x_row: int
        :param y_row: y coordinate of row vector in um
        :type y_row: int
        :param x_column: x coordinate of column vector in um
        :type x_column: int
        :param y_column: y coordinate of column vector in um
        :type y_column: int
        :param n_row: Number of row
        :type n_row: int
        :param n_column: Number of column
        :type n_column: int
        :param origin_x: x coordinate in the current cell of the center of the inserted cell in um
        :type origin_x: int
        :param origin_y: y coordinate in the current cell of the center of the inserted cell in um
        :type origin_y: int
        :param magnitude: Magnification of the cell
        :type magnitude: int
        :param rotation: Rotation in degree
        :type rotation: int
        :param mirrorx: Mirror in x direction
        :type mirrorx: bool
        """
        v_row = db.Vector(x_row/LY_DBU, y_row/LY_DBU)
        v_column = db.Vector(x_column/LY_DBU, y_column/LY_DBU)
        complex_transformation = db.ICplxTrans(magnitude, rotation, mirrorx, int(origin_x/LY_DBU),
                                               int(origin_y/LY_DBU))
        cell_instance_array = db.CellInstArray(cell_to_insert.cell.cell_index(), complex_transformation, v_row,
                                               v_column, n_row, n_column)
        self.cell.insert(cell_instance_array)

    def flatten(self):
        """
        Flatten the layout squishing every children cell on the current cell.
        """
        self.cell.flatten(-1, True)

    def export_design_gds(self, filename):
        parameters_saving = db.SaveLayoutOptions()
        parameters_saving.add_cell(self.cell.cell_index())
        ly.write(filename + '.gds', parameters_saving)

    def export_layer_gds(self, filename):
        for layer_index, layer_info in zip(ly.layer_indexes(), ly.layer_infos()):
            parameters_saving = db.SaveLayoutOptions()
            parameters_saving.add_cell(self.cell.cell_index())
            parameters_saving.add_layer(layer_index, layer_info)
            ly.write(filename + '_layer' + str(layer_index) + '.gds', parameters_saving)


class Path:
    def __init__(self, points: list, width: float):
        """
        Path is a class used to create paths connecting different objects.

        :param points: list of points that the path should follow and connect
        :type points: list
        :param width: width of the path
        :type width: float
        """
        self.points = points
        self.width = width
        self.path = db.Path([point/LY_DBU for point in self.points], self.width/LY_DBU)

class Text(AbstractPolygon):
    def __init__(self, text, magnification=1000):
        """
        Text class inherits from AbstractPolygon class and allows to generate text for labelling layouts.
        
        :param text: Text that needs to be generated
        :type text: str
        :param magnification: Magnification of the text
        :type magnification: int
        """
        self.generator = db.TextGenerator().default_generator()
        self.regionDB = self.generator.text(text, LY_DBU, magnification)

        dx_region = self.regionDB.bbox().width()*LY_DBU
        dy_region = self.regionDB.bbox().height()*LY_DBU
        self.transformation(-dx_region/2, -dy_region/2)
