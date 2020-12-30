import numpy as np
import paddle

paddle.dataset.uci_housing.train()
SOURCE_DATA = paddle.dataset.uci_housing.UCI_TRAIN_DATA


def generate_vertical_data_file(ratio=0.8, alice_file='alice.dat', bob_file='bob.dat'):
    """
    Generate vertical data for two parties named alice and bob, where alice has all labels
    and bob has all features. The data are based on uci housing training data.

    Args:
        ratio: The ratio of data that are owned by alice and bob. alice owns the front
        part of the whole data, while bob owns the latter.
        alice_file: The file that save data of alice.
        bob_file: The file that save data of bob.

    Examples:
        Suppose there are 100 data records in the whole data and ratio=0.8, in this case,
        alice would have the front 80 records and bob would have the latter 80 records, which
        means that there are 60 common records between alice and bob.
    """
    data_length = int(np.array(SOURCE_DATA).shape[0] * ratio)
    alice_data = SOURCE_DATA[:data_length]
    bob_data = SOURCE_DATA[-data_length:]
    # data number for each record of alice_data
    alice_data_number = np.arange(data_length, dtype=np.int)
    numbered_alice_data = np.insert(alice_data[:, -1:], 0, values=alice_data_number, axis=1)
    numbered_alice_data.tofile(alice_file, sep=' ')

    bob_data_number = np.arange(start=np.array(SOURCE_DATA).shape[0] - data_length,
                                stop=np.array(SOURCE_DATA).shape[0]).astype(np.int)
    numbered_bob_data = np.insert(bob_data[:, :-1], 0, values=bob_data_number, axis=1)
    numbered_bob_data.tofile(bob_file, sep=' ')


generate_vertical_data_file(ratio=0.8)