"""Build train/validation/test splits."""

from random import shuffle


def build_splits(data, train_frac=0.8, val_frac=0.1):
    shuffle(data)
    n = len(data)
    n_train = int(n * train_frac)
    n_val = int(n * val_frac)
    return data[:n_train], data[n_train:n_train+n_val], data[n_train+n_val:]
