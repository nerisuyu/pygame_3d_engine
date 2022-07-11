from engine.visualizeable.mesh2 import Mesh
import mimetypes

mimetypes.add_type("STL", ".stl")
mimetypes.add_type("OBJ", ".obj")
mimetypes.add_type("PNG", ".png")
mimetypes.add_type("JPEG", ".jpeg")

createVisualizeable = {
    'STL': lambda fn: Mesh().load_stl(fn),
    'PNG': print("png not implemented yet,dumbass"),
    'OBJ': print("obj is also not implemented, dumbbutt")
}


def load_visualizeable(filename=None):
    print("start loading")
    if filename:
        fileType = mimetypes.guess_type(filename)[0]
        if not fileType:
            print(f": No file type for '{filename}' found")
        else:
            print(f": fileType is {fileType}")

            __Visualizeable = createVisualizeable[fileType](filename)
            print("loaded",filename)
            return __Visualizeable
            # if fileType == "STL" or fileType == "OBJ":
            #     print(self.__name, ": create mesh")
            # else:
            #     if fileType == "PNG" or fileType == "JPEG":
            #         print(self.__name, ": create sprite")
            # todo call functions with different arguments based on fileType
            # todo find or write obj parser
            # todo find a way to color an stl model
            # todo figure out poses
# todo multiple visualzeables to an object
# todo new visualizeable - wireframe, second buffer for it or i dunno
