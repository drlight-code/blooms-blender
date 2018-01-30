import bpy
from bpy.types import Panel

class BloomsToolBar(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_description= ""
    bl_category = "Blooms" # vertical tab label
    bl_label = "Blooms"    # section header label

    def draw(self, context):
        layout = self.layout
        layout.enabled = True

        blooms = context.scene.blooms

        col = layout.column()
        col.label("Generate:")

        row = col.row(align=True)
        row.prop(blooms, "frame_count", text="Frame Count")

        row = col.row(align=True)
        row.prop(blooms, "live_update", text="Realtime (live) Update")
        row.operator("bloom.generate", text="Generate")

#        row = col.row(align=True)

        col = layout.column()
        col.label("Visualize:")

        row = col.row(align=True)
        row.prop(blooms, "spin", text="Spin")
        row.prop(blooms, "spin_fps", text="FPS")

        #        row.operator("bloom.spin_toggle", text="Spin")

def register():
    print("registering blooms ui")
    bpy.utils.register_class(BloomsToolBar)

def unregister():
    print("unregistering blooms ui")
    bpy.utils.unregister_class(BloomsToolBar)
