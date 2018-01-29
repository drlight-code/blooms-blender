import sys
import math
import logging

import bpy
from mathutils import Matrix, Vector

rootName = "bloom"
frameCount = 144
sphereRadius = 1
lateralRotationMax = 80
tangentialOrientation = True
scaleMin = 0.04
scaleMax = 0.12
goldenAngle = 137.5077640

log = logging.getLogger('blooms')

class SpinStart(bpy.types.Operator):
    bl_idname = "bloom.generate"
    bl_label = "Generate Bloom"
    bl_options = {'REGISTER'}

    def execute(self, context):
        log.debug("generating..")
        generate();
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SpinStart)

def unregister():
    bpy.utils.unregister_class(SpinStart)

if __name__ == "__main__":
    register()

def getHierarchyNames(name):
    names = []
    names.append(name)

    obj = bpy.data.objects[name]
    for child in obj.children:
        names += getHierarchyNames(child.name)

    return names

def deleteHierarchy(name):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get all names in the hierarchy
    names = getHierarchyNames(name)
#    log.debug('deleting objects: ' + str(names))

    # Remove the animation data from all objects and select them.
    for objName in names:
        obj = bpy.data.objects[objName]
        obj.select = True


    for obj in bpy.context.selected_objects:
        obj.animation_data_clear()
        material = bpy.data.materials.get(obj.name)
        if material:
            bpy.data.materials.remove(material, do_unlink=True)
        mesh = bpy.data.meshes.get(obj.name)
        if mesh:
            bpy.data.meshes.remove(mesh, do_unlink=True)

    # Delete the selected objects
    bpy.ops.object.delete()

class BloomTransformStrategy:
    longitudeIncrement = math.radians(goldenAngle)
    rotationLongitude = Matrix.Rotation(longitudeIncrement, 4, Vector((0, 0, 1)))

    frame = 0
    transformGlobal = Matrix.Translation(Vector((sphereRadius, 0, 0)))
    transformLocal = Matrix()

    def getTransform(self):
        return self.transformGlobal

    def step(self):
        self.frame = self.frame + 1

        self.transformGlobal = self.rotationLongitude * self.transformGlobal

        lateralRotationAxis = (self.transformGlobal * Vector((0, -1, 0, 0))).xyz
        rotationLatitude = Matrix.Rotation(1.0 / frameCount * math.radians(lateralRotationMax), 4, lateralRotationAxis)
        self.transformGlobal = rotationLatitude * self.transformGlobal


# def bloom():
#     cleanup()
#     generate()
#     unify()
#     bisect()

def cleanup():
    if bpy.data.objects.get(rootName):
        deleteHierarchy(rootName)

def getColorForFrame(frame):
    p = frame / (frameCount-1)
    return (0, p, 1-p)

def getScaleForFrame(frame):
    p = frame / (frameCount-1)
    scale = scaleMax - (scaleMax - scaleMin) * p
    return Matrix.Scale(scale, 4)

def getRotationForFrame(frame):
    p = frame / (frameCount-1)

    rotAngle = math.pi * 4 * p
    return Matrix.Rotation(rotAngle, 4, Vector((0, 1, 0)))

def getNameForFrame(frame):
    return "frame" + str(frame)

def update(self, context):
    if context.scene.blooms.live_update:
        generate()

def generate():
    cleanup()

    bpy.ops.object.empty_add()
    root = bpy.data.objects["Empty"]
    root.name = rootName

    bpy.ops.mesh.primitive_uv_sphere_add()
    base = bpy.data.objects["Sphere"]
    base.name = "base"
    base.parent = root
    base.matrix_local = Matrix.Scale(sphereRadius, 4)

    base.select = True
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.bisect(plane_no=(0, 0, 1), clear_inner=True)
    bpy.ops.mesh.fill()
    bpy.ops.object.editmode_toggle()

    createPetals()

def createPetals():
    root = bpy.data.objects[rootName]
    strategy = BloomTransformStrategy()

    for frame in range(0, frameCount):
        name = getNameForFrame(frame)
        bpy.ops.mesh.primitive_cube_add()

        obj = bpy.data.objects["Cube"]
        obj.name = name
        obj.data.name = name + "-mesh"
        obj.parent = root

        material = bpy.data.materials.new(name=name)
        material.diffuse_color = getColorForFrame(frame)
        obj.active_material = material

        # test
        scale = getScaleForFrame(frame)
        rotation = getRotationForFrame(frame)
        transform = strategy.getTransform() * scale * rotation
        obj.matrix_local = transform

        strategy.step()

def unify():
    log.debug("unifying..")

def bisect():
    log.debug("bisecting..")
