import numpy as np
import pandas as pd
import tensorflow as tf

class WindowGenerator():
    def __init__(self, input_width, label_width, shift,
                 train_df, val_df, test_df,
                 label_columns=None):
        # Store the raw data
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        # Store the column names
        self.label_columns = label_columns

        # Work out the label column indices
        self.column_indices = {name: i for i, name in enumerate(train_df.columns)}

        # Work out the window parameters
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]


    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack([labels[:, :, self.column_indices[name]] for name in self.label_columns], axis=-1)

        # Set shape for Tensors
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels
    

def plot_window_data_distributions(window):
    fig, axes = plt.subplots(nrows=window.column_indices.size, figsize=(10, 7))
    for idx, ax in enumerate(axes):
        ax.hist(window.train.dataset[:, idx], bins=30, alpha=0.5, color='blue', label='Train')
        ax.hist(window.val.dataset[:, idx], bins=30, alpha=0.5, color='green', label='Val')
        ax.hist(window.test.dataset[:, idx], bins=30, alpha=0.5, color='orange', label='Test')
        ax.set_title(window.column_indices.keys()[idx].capitalize())
        ax.legend()

    plt.suptitle('Window Data Distributions')
    plt.show()


    def make_dataset(self, data):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=32,)
        ds = ds.map(self.split_window)
        return ds

    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df)