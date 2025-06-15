# import resnet50
# import vgg16
# import efficientnetb0
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import EfficientNetB0

def get_model(name):
    if name == "ResNet50":
        return build_resnet()
    elif name == "VGG16":
        return build_vgg()
    elif name == "EfficientNetB0":
        return build_efficientnet()
    else:
        raise ValueError(f"Unknown model: {name}")

def build_resnet():
    base = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base.trainable = False
    x = GlobalAveragePooling2D()(base.output)
    out = Dense(1, activation="sigmoid")(x)
    model = Model(base.input, out)
    model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
    return model

def build_vgg():
    base = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base.trainable = False
    x = GlobalAveragePooling2D()(base.output)
    out = Dense(1, activation="sigmoid")(x)
    model = Model(base.input, out)
    model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
    return model

def build_efficientnet():
    base = EfficientNetB0(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base.trainable = False
    x = GlobalAveragePooling2D()(base.output)
    out = Dense(1, activation="sigmoid")(x)
    model = Model(base.input, out)
    model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
    return model
