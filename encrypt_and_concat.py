import numpy as np
import os
from paddle_fl.mpc.data_utils import aby3


def concat_encrypted_data(alice_file, alice_shape, bob_file, bob_shape, concat_file):
    """
    Concat vertical data owned by two parties after encryption.
    Note that we determine that the format of concatenated data
    is bob followed by alice.

    Args:
        alice_file: The file that save encrypted data of alice.
        alice_shape: The data shape of alice.
        bob_file: The file that save encrypted data of bob.
        bob_shape: The data shape of bob.
        concat_file: The file to save the concatenated data.
    """
    alice_shape = (2, ) + alice_shape
    alice_share_size = np.prod(alice_shape) * 8

    bob_shape = (2, ) + bob_shape
    bob_share_size = np.prod(bob_shape) * 8

    # store concatenated data
    concat_data = []

    with open(alice_file, 'rb') as alice, open(bob_file, 'rb') as bob:
        alice_share = alice.read(alice_share_size)
        bob_share = bob.read(bob_share_size)
        while alice_share and bob_share:
            alice_data = np.frombuffer(alice_share, dtype=np.int64).reshape(alice_shape)
            bob_data = np.frombuffer(bob_share, dtype=np.int64).reshape(bob_shape)
            data = np.concatenate((alice_data, bob_data), axis=1)
            concat_data.append(data)
            alice_share = alice.read(alice_share_size)
            bob_share = bob.read(bob_share_size)

    np.array(concat_data).tofile(concat_file, sep=' ')


def encrypt(file, data_len, encrypted_file):
    """
    Encrypt data for each party.

    Args:
        file: The file that saves data to encrypt.
        data_len: The length of plain data. E.g.,for uci housing
        feature data, the length is 13.
        encrypted_file: The file that saves encrypted data.
    """
    data = np.fromfile(file, sep=' ')
    data = data.reshape(data.shape[0] // (data_len + 1), data_len + 1)

    def sample_reader():
        """
        read concated data.
        """
        for d in data:
            yield d[1:]

    def encrypt_sample():
        """
        encrypt sample
        """
        for sample in sample_reader():
            yield aby3.make_shares(sample)

    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    aby3.save_aby3_shares(encrypt_sample, "./tmp/" + encrypted_file)

# Alice who has labels makes encryption.
encrypt(file='alice_filtered.dat',
        data_len=1,
        encrypted_file='house_label')
# Bob who has features makes encryption.
encrypt(file='bob_filtered.dat',
        data_len=13,
        encrypted_file='house_feature')

# Because alice has all labels and bob has all features,
# no need for concat between encrypted features and
# encrypted labels. Here is an example for concat between
# encrypted label and encrypted feature for computation party 0.
concat_encrypted_data(alice_file='./tmp/house_label.part0',
       alice_shape=(1,),
       bob_file='./tmp/house_feature.part0',
       bob_shape=(13,),
       concat_file='concat.part0')