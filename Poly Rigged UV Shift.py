# 脚本功能：将UV从一个模型传递到另一个模型，并且尽量不影响目标模型上的现有历史。
# 使用后请请确认无误再手动执行"Non-Deformer History"
import pymel.core as pm

def transferUVsWithoutHistory(source, target):
    """
    Parameters:
    source (str): 源模型的名称，其UV是正确的
    target (str): 目标模型的名称，其UV需要被替换
    """
    # 确保源和目标对象存在
    if not pm.objExists(source):
        raise ValueError("源模型不存在: {}".format(source))
    if not pm.objExists(target):
        raise ValueError("目标模型不存在: {}".format(target))
        
    # 执行UV传递
    pm.polyTransfer(target, uv=True, ao=source)
    pm.select(target)  # 选择目标模型，以便检查结果

    print("已成功将UV从 {} 传递到 {}，请再次检查确认，无误后手动执行 Non-Deformer History。".format(source, target))

# 使用示例
# 请将"source" 修改为UV正确的模型
# 请将"target" 修改为被替换UV的模型
transferUVsWithoutHistory('source', 'target')
