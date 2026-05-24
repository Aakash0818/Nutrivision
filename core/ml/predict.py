import os
import json
import numpy as np
import cv2
from django.conf import settings
from tensorflow.keras.models import model_from_json

TRAINED_PATH = os.path.join(settings.BASE_DIR, 'trained')

MODEL_JSON_PATH = os.path.join(TRAINED_PATH, 'food_model.json')
MODEL_WEIGHTS_PATH = os.path.join(TRAINED_PATH, 'food_model_weights.h5')
LABELS_PATH = os.path.join(TRAINED_PATH, 'class_labels.json')

IMG_SIZE = 160   # 🔥 MUST MATCH TRAINING SIZE

# Load model
with open(MODEL_JSON_PATH, 'r') as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)
model.load_weights(MODEL_WEIGHTS_PATH)

# Load labels
with open(LABELS_PATH, 'r') as f:
    class_indices = json.load(f)

class_labels = {v: k for k, v in class_indices.items()}


def predict_food(image_path):

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found or corrupted")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img, verbose=0)

    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions)) * 100

    predicted_label = class_labels[class_index]

    return predicted_label, round(confidence, 2)
