import tensorflow as tf

from tensorflow.keras.initializers import Identity as Identity2D


class Identity(Identity2D):

    def __call__(self, shape, dtype=None):
        # Equivalent to:
        #  *batch_shape, num_rows, num_columns = shape
        #  return self.gain * tf.eye(num_rows, num_columns, batch_shape, dtype=dtype)
        if len(shape) > 2:
            head, *tail = shape
            return tf.stack([self(tail, dtype) for _ in range(head)], axis=0)
        return super().__call__(shape, dtype)
