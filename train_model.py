import os
import json
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

TRAIN_PATH = "dataset/train"
VAL_PATH = "dataset/val"

IMG_SIZE = 160   # 🔥 reduced from 224
BATCH_SIZE = 16  # 🔥 smaller batch
EPOCHS = 5       # 🔥 reduced epochs

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    VAL_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# 🔥 Freeze everything (fast)
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(64, activation='relu')(x)   # smaller dense layer
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

os.makedirs("trained", exist_ok=True)

# Save
model_json = model.to_json()
with open("trained/food_model.json", "w") as json_file:
    json_file.write(model_json)

model.save_weights("trained/food_model_weights.h5")

class_indices = train_generator.class_indices
with open("trained/class_labels.json", "w") as f:
    json.dump(class_indices, f)

print("✅ Fast training completed")
