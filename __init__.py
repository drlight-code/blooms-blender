import logging

if "bpy" not in locals():
    import bpy
    from bpy.props import (
        StringProperty,
        EnumProperty,
        BoolProperty,
        IntProperty,
        FloatProperty,
        PointerProperty
    )
    from bpy.types import (
        PropertyGroup
    )

    from . import (ui, blooms)
else:
    import importlib
    importlib.reload(blooms)
    importlib.reload(ui)


bl_info = {
    "name": "Blooms",
    "author": "Patric Schmitz",
    "version": (0, 0, 0),
    "blender": (2, 78, 0),
    "location": "3D View Tool Shelf (left)",
    "description": "Procedural modeling plugin to generate 3D printable zoetrope sculptures as invented by John Edmark.",
    "wiki_url": "TODO",
    "category": "Generative"
}

log = logging.getLogger('blooms')

class BloomsProperties(PropertyGroup):
    frame_count = IntProperty(
        name="frame-count",
        description='',
        default=144,
        min=0,
        update=blooms.update
    )

    live_update = BoolProperty(
        name="live-update",
        description='',
        default=False,
    )

    spin = BoolProperty(
        name="spin",
        description='',
        default=False,
    )

    spin_fps = FloatProperty(
        name="spin_fps",
        description='',
        default=10,
    )

def register():
    bpy.utils.register_class(BloomsProperties)

    blooms.register()
    ui.register()

    bpy.types.Scene.blooms = PointerProperty(type=BloomsProperties)

def unregister():
    bpy.utils.unregister_class(BloomsProperties)

    ui.unregister()
    blooms.unregister()

    del bpy.types.Scene.blooms
