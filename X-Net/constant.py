import tensorflow as tf
from absl import app

FLAGS = tf.compat.v1.flags.FLAGS  #tf.app.flags.FLAGS 

tf.compat.v1.flags.DEFINE_integer('input_image_height', 256,
                            """Input image height.""")
tf.compat.v1.flags.DEFINE_integer('input_image_width', 256,
                            """Input image width.""")
tf.compat.v1.flags.DEFINE_integer('batch_size', 1,
                            """Number of images to process in a batch.""")