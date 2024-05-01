import maya.cmds as cmds

selected_models = {'character': '', 'wrapper': '', 'target': ''}

def select_model(model_type, *args):
    selection = cmds.ls(selection=True)
    if selection:
        selected_models[model_type] = selection[0]
        # Updating the GUI label to show the selected model name
        cmds.text(model_type + "_label", edit=True, label=selected_models[model_type])
    else:
        cmds.warning("No objects selected.")

def execute_process(*args):
    character_model = selected_models['character']
    wrapper_model = selected_models['wrapper']
    target_model = selected_models['target']

    # Make sure all models are selected
    if not all(selected_models.values()):
        cmds.warning("Please ensure all models are selected.")
        return

    # Using listHistory and ls to find BlendShape nodes
    history = cmds.listHistory(character_model)
    blendShape_nodes = cmds.ls(history, type='blendShape')
    if not blendShape_nodes:
        cmds.error("The character model does not have BlendShapes.")
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
        # Activating each blendshape target
        cmds.setAttr(f"{bs_node}.{target}", 1)
        # Duplicating the wrapper model and renaming it
        duplicated_wrapper = cmds.duplicate(wrapper_model, name=target)[0]
        # Deactivating the blendshape target back
        cmds.setAttr(f"{bs_node}.{target}", 0)
        cmds.parent(duplicated_wrapper, "Wrap")

        # Finding the next index for the new blendshape target
        existing_targets = cmds.aliasAttr(blendShape_node, query=True) or []
        weightIndex = len(existing_targets) // 2

        # Adding the duplicated model as a new blendshape target
        cmds.blendShape(blendShape_node, edit=True, target=(target_model, weightIndex, duplicated_wrapper, 1.0), weight=(weightIndex, 0))

    cmds.select(deselect=True)
    
def create_gui():
    window_name = "ModelProcessorGUI"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Creating the GUI window
    cmds.window(window_name, title="Model Selection and Processing Tool", widthHeight=(300, 160))
    cmds.columnLayout(adjustableColumn=True)

    # Creating rows for selecting models
    for model_type in ['character', 'wrapper', 'target']:
        cmds.rowLayout(numberOfColumns=3)
        cmds.text(label=f"{model_type.capitalize()} Model:")
        cmds.button(label="Select", command=lambda x, mt=model_type: select_model(mt))
        model_label = model_type + "_label"
        cmds.text(model_label, label="None selected")
        cmds.setParent('..')
    
    cmds.button(label="Execute", command=execute_process)
    cmds.showWindow(window_name)

create_gui()
