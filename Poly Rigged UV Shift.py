# Script Function: Transfer UVs from one model to another while minimizing the impact on the existing history of the target model.
# Please double-check the results before manually executing "Non-Deformer History"
import pymel.core as pm

def transferUVsWithoutHistory(source, target):
    """
    Parameters:
    source (str): The name of the source model, which has the correct UVs
    target (str): The name of the target model, whose UVs need to be replaced
    """
    # Ensure both source and target objects exist
    if not pm.objExists(source):
        raise ValueError("Source model does not exist: {}".format(source))
    if not pm.objExists(target):
        raise ValueError("Target model does not exist: {}".format(target))
        
    # Execute UV transfer
    pm.polyTransfer(target, uv=True, ao=source)
    pm.select(target)  # Select the target model to facilitate result checking

    print("Successfully transferred UVs from {} to {}. Please double-check and then manually execute Non-Deformer History.".format(source, target))

# Usage example
# Please change "source" to the model with correct UVs
# Please change "target" to the model whose UVs are to be replaced
transferUVsWithoutHistory('source', 'target')
