## tflite_model.py
import tensorflow as tf
from pathlib import Path
import numpy as np
import time
from loguru import logger
from pprint import pprint

# ENV + CONFIG
BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "models" / "1dcnn.tflite"
logger.debug(f"Given model path at : {model_path}")

CLASS_NAMES = ['N (0) - Normal','S (1) - SVEB','V (2) - VEB','F (3) - Fusion','Q (4) - Unknown']

class ECGTFLiteModel:

    def __init__(self, model_path: Path, class_names=CLASS_NAMES):
        self.class_names = class_names
        self.interpreter = tf.lite.Interpreter(model_path=str(model_path))
        self.interpreter.allocate_tensors()
       
        # Cache tensor details ONCE
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.input_index = self.input_details[0]["index"]
        self.output_index = self.output_details[0]["index"]

        self.current_batch_size = None
        logger.success("TFLite model loaded and ready")
        logger.info("Input Details:")
        pprint(self.input_details)
        logger.info("Output Details:")
        pprint(self.output_details)

    def predict(self, input_array: np.ndarray):
        """input_array shape: (batch, 187, 1)"""
        # Ensure float32
        input_array = input_array.astype(np.float32)
        batch_size = input_array.shape[0]

        # Resize ONLY if batch size changed
        if batch_size != self.current_batch_size:
            self.interpreter.resize_tensor_input(self.input_index, input_array.shape)
            self.interpreter.allocate_tensors()
            self.current_batch_size = batch_size

        # Run inference
        self.interpreter.set_tensor(self.input_index, input_array)
        self.interpreter.invoke()

        predictions = self.interpreter.get_tensor(self.output_index)

        predicted_indices = np.argmax(predictions, axis=1)
        predicted_classes = [self.class_names[i] for i in predicted_indices]
        confidences = np.max(predictions, axis=1)

        return predicted_classes, confidences

if __name__ == "__main__":

    model =  ECGTFLiteModel(model_path, CLASS_NAMES)
   
    batch_size:int = 4
    dummy_input = np.random.rand(batch_size, 187, 1)
    classes, confidences = model.predict(dummy_input)
    for predicted_class, confidence in zip(classes, confidences):
        logger.info("{} ({:.2f})", predicted_class, confidence)
