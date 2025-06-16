from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224, 224)
BATCH_SIZE = 32


def get_data_generators(dataset_path, split_ratio=0.8):
    datagen = ImageDataGenerator(
        rescale=1. / 255,
        validation_split=1 - split_ratio,
        rotation_range=10,
        zoom_range=0.1,
        horizontal_flip=True
    )

    train_gen = datagen.flow_from_directory(
        dataset_path,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training',
        shuffle=True
    )

    val_gen = datagen.flow_from_directory(
        dataset_path,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation',
        shuffle=False
    )

    return train_gen, val_gen
