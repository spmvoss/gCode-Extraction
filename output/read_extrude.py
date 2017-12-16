from __future__ import print_function

from OCC.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.gp import gp_Circ
from OCC.GeomAPI import GeomAPI_PointsToBSpline
from OCC.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfLin2d
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Display.SimpleGui import init_display
from process_gcode import Processor

display, start_display, add_menu, add_function_to_menu = init_display()



def pipe():
    processor = Processor(filename="layer3.txt",sub_distance=0.05,max_dist=0.1, min_dist=0.01)
    processor.read()
    array2 = TColgp_Array1OfPnt(1, len(processor.layers["1_11"]))
    for ind, value in enumerate(processor.layers["1_11"]):
        if ind == 0:
            point = gp_Pnt(value[0], value[1], value[2])
        array2.SetValue(ind + 1, gp_Pnt(value[0], value[1], value[2]))
    # the bspline path, must be a wire
    bspline2 = GeomAPI_PointsToBSpline(array2,20,45).Curve()
    path_edge = BRepBuilderAPI_MakeEdge(bspline2).Edge()
    path_wire = BRepBuilderAPI_MakeWire(path_edge).Wire()

    # # the bspline profile. Profile mist be a wire
    # dir = gp_Dir(0, 1, 0)
    # circle = gp_Circ(gp_Ax2(point, dir), 0.2)
    # profile_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    #
    # # pipe
    # pipe = BRepOffsetAPI_MakePipe(path_wire, profile_edge).Shape()

    #display.DisplayShape(profile_edge, update=True)
    display.DisplayShape(path_wire, update=True)
    #display.DisplayShape(pipe, update=True)


if __name__ == '__main__':
    pipe()
    start_display()
