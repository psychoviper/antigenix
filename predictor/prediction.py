import tensorflow as tf
import numpy as np
import os
from django.apps import apps

def predict(sequences):
    # Load the model
    # Get the app's directory path
    app_dir = apps.get_app_config('predictor').path

    # Join the app directory with the model file name
    model_path = os.path.join(app_dir, 'antigenicity_model.h5')

    # Load the model
    model = tf.keras.models.load_model(model_path)
    ans=[]
    for seq in sequences:
        print(len(seq))
        predictions = model.predict(seq)
        ans.append(predictions)
    print(ans[0])
    return ans[0]

# if __name__=="__main__":
#     # Example new sequences (assuming numerical data for simplicity)
#     sequence = 'MAATQETAIDKYKKVKRIKWIVRLLGGSTGVVIAAAITLLLIVSMAIFGGQSSTGTPNGGISGTATVKNLPPEVMRWQAMVEQECAAQGVPELVPYVLAIIMVESNGISEKLPDIMQSSESQGWAMNTISNPKDSIYYGVMHLKGAFDDAKMLGINDLLAIVQTYNFGRNYVHWLAANNKTHSIQTADYYSLTVVAPAGGNRNGTTIGYSQPVAVAYNGGYRYINGGNFFYAEMVKQYLSFDGAGGTSGQIPGGSETFKVMMDEVLKYNGNPYVWGGKSSSQGFDCSGLTYWAYKTAGITIPISAATQYDFTVEVDPKDAQPGDLVFFRGTYGGPNHVSHVGIYIDANTMYDSNGSGVGYHQFTSSYWQQHYAGIRRVPR'
#     val = get_acc(sequence)
#     val = val.reshape(1, -1)
#     sequences=[]
#     sequences.append(val)
#     # print(val)
#     predict(sequences)