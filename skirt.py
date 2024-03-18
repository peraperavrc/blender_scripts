import bpy
import math

# シリンダーのメッシュを作成（スカートの基本形状）
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=1, depth=2, location=(0, 0, 0))
skirt_mesh = bpy.context.object
skirt_mesh.name = 'SkirtMesh'

# アーマチュアの作成
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
armature = bpy.context.object
armature.name = 'SkirtArmature'
bpy.ops.object.mode_set(mode='EDIT')

# ルートボーンの作成
root_bone = armature.data.edit_bones.new(name="Root")
root_bone.head = (0, 0, 0)
root_bone.tail = (0, 0, 1)

# ボーンを配置
for i in range(12):
    angle = 2 * math.pi * i / 12
    side = 'L' if math.sin(angle) > 0 else 'R'  # 左側か右側かを判断
    parent_bone = armature.data.edit_bones.new(name=f"{side}Bone.{i}")
    parent_bone.parent = root_bone  # ルートボーンを親とする
    parent_bone.head = (math.cos(angle), math.sin(angle), 1)
    parent_bone.tail = (math.cos(angle), math.sin(angle), 1.5)
    for j in range(1, 4):
        child_bone = armature.data.edit_bones.new(name=f"{side}Bone.{i}.{j}")
        child_bone.parent = parent_bone
        child_bone.use_connect = True
        child_bone.head = (parent_bone.tail[0], parent_bone.tail[1], parent_bone.tail[2])
        child_bone.tail = (parent_bone.tail[0], parent_bone.tail[1], parent_bone.tail[2] + 0.5)
        parent_bone = child_bone

bpy.ops.object.mode_set(mode='OBJECT')

# メッシュをアーマチュアの子として設定
skirt_mesh.modifiers.new(name="Armature", type='ARMATURE')
skirt_mesh.modifiers['Armature'].object = armature
skirt_mesh.parent = armature

# ウェイトペインティングの自動設定
bpy.ops.object.select_all(action='DESELECT')
armature.select_set(True)
skirt_mesh.select_set(True)
bpy.context.view_layer.objects.active = skirt_mesh
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
