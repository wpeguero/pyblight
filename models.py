"""Models Module
-----------------

This file will contain all of the actualized models
created from the abstract model class(es) made within
the base.py file."""
from tensorflow.keras.layers import Conv2D, Dense, Rescaling, Flatten, MaxPooling2D, Dropout, RandomZoom, Permute, Reshape, Input, Concatenate
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics import CategoricalAccuracy
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model, split_dataset
from tensorflow.keras.models import save_model
import tensorflow as tf
from pipeline import load_data, load_data2
import datetime

BATCH_SIZE = 8

def _main():
    inputs, output = tumor_classifier(1147, 957)
    model = Model(inputs=inputs, outputs=output)
    #model.build(input_shape=(800,800))
    plot_model(model, show_shapes=True, to_file='model6.png')
    
    model.compile(optimizer='RMSprop', loss=CategoricalCrossentropy(), metrics=[CategoricalAccuracy()])
    filename = "data/CMMD-set/clinical_data_with_unique_paths.csv"
    tfrecordname = 'data/CMMD-set/saved_data3'
    tfrecordname = None
    if tfrecordname is None:
        print("\nLoading data for training...\n")
        data = load_data2(filename)
        y = data['class']
        data.pop('class')
        dataset = tf.data.Dataset.from_tensor_slices((data, y)).batch(BATCH_SIZE)
    else:
        print("\nLoading TFRecord...\n")
        dataset = tf.data.Dataset.load('data/CMMD-set/saved_data3')
    dataset = dataset.shuffle(buffer_size=1_000).prefetch(tf.data.AUTOTUNE)
    tf.data.Dataset.save(dataset, 'data/CMMD-set/saved_data3')
    #trainds = dataset.random(seed=4).take(2808)
    #testds = dataset.random(seed=4).skip(2808)
    #trainds = trainds.shuffle(buffer_size=1_000).prefetch(tf.data.AUTOTUNE)
    #exit()
    #logs = './data/trainlogs/' + datetime.datetime.now().strftime("%Y%m%d - %H%M%S")
    #tb_callback1 = tf.keras.callbacks.TensorBoard(log_dir=logs, histogram_freq=1, profile_batch=20)
    #tb_callback2 = tf.keras.callbacks.TensorBoard(log_dir=logs, histogram_freq=1, profile_batch=40)
    model.fit(dataset, epochs=100)
    save_model(model,'./models/tclass_V10')


def base_image_classifier(img_height:float, img_width:float):
    """Basic Image Classifier for model comparison improvement.

    ...

    A class containing a simple classifier for any
    sort of image. The models stemming from this
    class will function to only classify the image
    in one manner alone (malignant or non-malignant).
    This model will not contain any rescaling or 
    data augmentation to show how significant the
    accuracy between a model with rescaling and
    data augmentation is against a model without
    any of these.

    Parameters
    -----------
    img_height : float
        The height, in pixels, of the input images.
        This can be the maximum height of all images
        within the dataset to fit a varied amount
        that is equal or less than the declared height.
    
    img_width : float
        The width, in pixels, of the input images.
        This can also be the maximum width of all
        images within the dataset to fit a varied
        amount that is equal or smaller in width
        to the declared dimension.
    
    batch_size : int
        One of the factors of the total sample size.
        This is done to better train the model without
        allowing the model to memorize the data.
    
    Returns
    -------
    inputs : {img_input, cat_input}
        Input layers set to receive both image and
        categorical data. The image input contains
        images in the form of a 2D numpy array. The
        categorical input is a 1D array containing
        patient information. This is mainly comprised
        of categorical data, but some nominal data.
    
    output : Dense Layer
        The last layer of the model developed. As
        the model is fed through as the input of
        the next layer, the last layer is required
        to create the model using TensorFlow's Model
        class.
    """
    img_input = Input(shape=(img_height,img_width,1), name="image")
    cat_input = Input(shape=(2), name="cat")
    inputs = [img_input, cat_input]
    # Set up the images
    x = Conv2D(16, 3, padding='same', activation='relu')(img_input)
    x = MaxPooling2D()(x)
    x = Flatten()(x)
    #x = Dense(128, activation='relu')(x)
    #Set up the categorical data
    y = Dense(2, activation='relu')(cat_input)
    y = Dense(1, activation='relu')(y)
    # Merge both layers
    together = Concatenate(axis=1)([x,y])
    output = Dense(2, activation='softmax', name="output")(together)
    return inputs, output

def base_image_classifier2(img_height:float, img_width:float):
    """Basic Image Classifier with rescaling and data augmentation.

    ...

    A class containing a simple classifier for any
    sort of image. The models stemming from this class
    will include rescaling and data augmentation
    for the sake and purpose of normalizing the data.
    
    Parameters
    -----------
    img_height : float
        The height, in pixels, of the input images.
        This can be the maximum height of all images
        within the dataset to fit a varied amount
        that is equal or less than the declared height.
    
    img_width : float
        The width, in pixels, of the input images.
        This can also be the maximum width of all
        images within the dataset to fit a varied
        amount that is equal or smaller in width
        to the declared dimension.
    
    batch_size : int
        One of the factors of the total sample size.
        This is done to better train the model without
        allowing the model to memorize the data.
    
    Returns
    -------
    inputs : {img_input, cat_input}
        Input layers set to receive both image and
        categorical data. The image input contains
        images in the form of a 2D numpy array. The
        categorical input is a 1D array containing
        patient information. This is mainly comprised
        of categorical data, but some nominal data.
    
    output : Dense Layer
        The last layer of the model developed. As
        the model is fed through as the input of
        the next layer, the last layer is required
        to create the model using TensorFlow's Model
        class.
    """
    img_input = Input(shape=(img_height,img_width,3), name="Image Input")
    cat_input = Input(shape=(5), name="Categorical Input")
    inputs = [img_input, cat_input]
    # Set up the images
    x = Rescaling(1./255, input_shape= (img_height, img_width,3))(img_input)
    x = RandomZoom(0.1)(x)
    x = Conv2D(16, 3, padding='same', activation='relu')(x)
    x = MaxPooling2D()(x)
    #x = Dense(128, activation='relu')(x)
    #Set up the categorical data
    y = Dense(2, activation='relu')(cat_input)
    y = Dense(1, activation='relu')(y)
    # Merge both layers
    together = Concatenate(axis=1)([x,y])
    output = Dense(2, activation='softmax')(together)
    return inputs, output

def base_tumor_classifier(img_height:float, img_width:float):
    """Base Tumor Classification Algorithm.

    ...

    A class containing a simple classifier for side-view
    image. The models stemming from this class
    will include rescaling and data augmentation
    for the sake and purpose of normalizing the data.

    Parameters
    -----------
    img_height : float
        The height, in pixels, of the input images.
        This can be the maximum height of all images
        within the dataset to fit a varied amount
        that is equal or less than the declared height.
    
    img_width : float
        The width, in pixels, of the input images.
        This can also be the maximum width of all
        images within the dataset to fit a varied
        amount that is equal or smaller in width
        to the declared dimension.
    
    Returns
    -------
    inputs : {img_input, cat_input}
        Input layers set to receive both image and
        categorical data. The image input contains
        images in the form of a 2D numpy array. The
        categorical input is a 1D array containing
        patient information. This is mainly comprised
        of categorical data, but some nominal data.
    
    output : Dense Layer
        The last layer of the model developed. As
        the model is fed through as the input of
        the next layer, the last layer is required
        to create the model using TensorFlow's Model
        class.
    """
    img_input = Input(shape=(img_height, img_width, 1), name='image')
    cat_input = Input(shape=(2), name='cat')
    inputs = [img_input, cat_input]
    # Set up the images
    x = Rescaling(1./255, input_shape=(img_height, img_width,1))(img_input)
    # Finish building the model

def tumor_classifier(img_height:float, img_width:float):
    """Complete Tumor Classification Algorithm.

    ...

    A class containing a simple classifier for any
    sort of image. The models stemming from this class
    will include rescaling and data augmentation
    for the sake and purpose of normalizing the data.

    Parameters
    -----------
    img_height : float
        The height, in pixels, of the input images.
        This can be the maximum height of all images
        within the dataset to fit a varied amount
        that is equal or less than the declared height.
    
    img_width : float
        The width, in pixels, of the input images.
        This can also be the maximum width of all
        images within the dataset to fit a varied
        amount that is equal or smaller in width
        to the declared dimension.
    
    batch_size : int *
        One of the factors of the total sample size.
        This is done to better train the model without
        allowing the model to memorize the data.
    
    Returns
    -------
    inputs : {img_input, cat_input}
        Input layers set to receive both image and
        categorical data. The image input contains
        images in the form of a 2D numpy array. The
        categorical input is a 1D array containing
        patient information. This is mainly comprised
        of categorical data, but some nominal data.
    
    output : Dense Layer
        The last layer of the model developed. As
        the model is fed through as the input of
        the next layer, the last layer is required
        to create the model using TensorFlow's Model
        class.
    
    ---
    
    *Deprecated
    """
    img_input = Input(shape=(img_height, img_width, 1), name='image')
    cat_input = Input(shape=(2), name='cat')
    inputs = [img_input, cat_input]
    # Set up the images
    x = Rescaling(1./255, input_shape=(img_height, img_width,1))(img_input)
    x = Conv2D(96, 11, strides=(4,4), activation='sigmoid')(x)
    x = MaxPooling2D(pool_size=(3,3))(x)
    x = Conv2D(256, 5, padding='same', activation='sigmoid')(x)
    x = MaxPooling2D(pool_size=(3,3), strides=2)(x)
    x = Conv2D(384, 3, padding='same', activation='sigmoid')(x)
    #x = Dropout(0.3)(x)
    x = Conv2D(384, 3, padding='same', activation='sigmoid')(x)
    x = Conv2D(256, 3, padding='same', activation='sigmoid')(x)
    x = MaxPooling2D(pool_size=(3,3), strides=2)(x)
    x = Flatten()(x)
    x = Dense(4096, activation='gelu')(x)
    #x = Dropout(0.3)(x)
    x = Dense(4096, activation='gelu')(x)
    x = Dense(1000, activation='gelu')(x)
    x = Dense(500, activation='gelu')(x)
    x = Dense(250, activation='gelu')(x)
    x = Dense(100, activation='gelu')(x)
    x = Dense(50, activation='gelu')(x)
    x = Dense(25, activation='gelu')(x)
    #Set up the categorical data
    y = Dense(2, activation='gelu')(cat_input)
    y = Dense(1, activation='gelu')(y)
    # Merge both layers

    together = Concatenate(axis=1)([x,y])
    output = Dense(2, activation='sigmoid', name='class')(together)
    return inputs, output


if __name__ == "__main__":
    _main()