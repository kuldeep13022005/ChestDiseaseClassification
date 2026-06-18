import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input


class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename
    
    def predict(self):
        ## load model
        
        model = load_model(os.path.join("Artifacts","Model_Training", "Trained_Model.h5"))

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        test_image = preprocess_input(test_image)
        result = np.argmax(model.predict(test_image), axis=1)
        print(result)

        class_mapping = {
            0: 'Adenocarcinoma Cancer',
            1: 'Large Cell Carcinoma',
            2: 'Normal',
            3: 'Squamous Cell Carcinoma'
        }
        prediction = class_mapping.get(result[0], 'Unknown')
        return [{ "image" : prediction}]