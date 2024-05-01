import maya.cmds as cmds

selected_models = {'character': '角色', 'wrapper': '包裹', 'target': '目标'}

def select_model(model_type, *args):
    # 选择物体并更新GUI上的标签以显示所选模型的名称
    selection = cmds.ls(selection=True)
    if selection:
        selected_models[model_type] = selection[0]
        cmds.text(model_type + "_label", edit=True, label=selected_models[model_type])
    else:
        cmds.warning("没有选中任何物体。")

def execute_process(*args):
    character_model = selected_models['character']
    wrapper_model = selected_models['wrapper']
    target_model = selected_models['target']

    # 确保所有必要的模型都已选择
    if not all(selected_models.values()):
        cmds.warning("请确保所有必要的模型都已选择。")
        return

    # 使用listHistory和ls查找BlendShape节点
    history = cmds.listHistory(character_model)
    blendShape_nodes = cmds.ls(history, type='blendShape')
    if not blendShape_nodes:
        cmds.error("角色模型上没有BlendShapes。")
        return
    
    bs_node = blendShape_nodes[0]
    targets = cmds.listAttr(bs_node + '.w', multi=True)
    
    if not cmds.objExists("Wrap"):
        cmds.group(em=True, name="Wrap")

    if not cmds.objExists(target_model + "_blendShape"):
        blendShape_node = cmds.blendShape(target_model, name=target_model + "_blendShape")[0]
    else:
        blendShape_node = target_model + "_blendShape"

    for target in targets:
        # 逐一激活每个BlendShape目标
        cmds.setAttr(f"{bs_node}.{target}", 1)
        # 复制包裹模型并重命名
        duplicated_wrapper = cmds.duplicate(wrapper_model, name=target)[0]
        # 将BlendShape目标重新设置为0
        cmds.setAttr(f"{bs_node}.{target}", 0)
        cmds.parent(duplicated_wrapper, "Wrap")

        # 查找新BlendShape目标的下一个索引
        existing_targets = cmds.aliasAttr(blendShape_node, query=True) or []
        weightIndex = len(existing_targets) // 2

        # 将复制的模型作为一个新的BlendShape目标添加
        cmds.blendShape(blendShape_node, edit=True, t=(target_model, weightIndex, duplicated_wrapper, 1.0), w=(weightIndex, 0))

    cmds.select(deselect=True)
    
def create_gui():
    window_name = "ModelProcessorGUI"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # 创建GUI窗口
    cmds.window(window_name, title="模型选择和处理工具", widthHeight=(300, 160))
    cmds.columnLayout(adjustableColumn=True)

    # 为选择模型创建行
    for model_type in ['character', 'wrapper', 'target']:
        cmds.rowLayout(numberOfColumns=3)
        cmds.text(label=f"{model_type.capitalize()} 模型：")
        cmds.button(label="选择", command=lambda x, mt=model_type: select_model(mt))
        model_label = model_type + "_label"
        cmds.text(model_label, label="未选择")
        cmds.setParent('..')
    
    cmds.button(label="执行", command=execute_process)
    cmds.showWindow(window_name)

create_gui()
