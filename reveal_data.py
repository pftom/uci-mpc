import numpy as np
import paddle
import six
from paddle_fl.mpc.data_utils import aby3
def load_decrypt_data(filepath, shape):
    """
    load the encrypted data and reconstruct
    """
    part_readers = []
    for id in six.moves.range(3):
        part_readers.append(
            aby3.load_aby3_shares(
                filepath, id=id, shape=shape))
    aby3_share_reader = paddle.reader.compose(part_readers[0], part_readers[1],
                                              part_readers[2])
    epoch_id = 0
    for instance in aby3_share_reader():
        p = aby3.reconstruct(np.array(instance))
        print("Epoch %d, Step 0, Loss: %f " % (epoch_id,p[0]))
        epoch_id += 1


load_decrypt_data("tmp/uci_loss", (1, ))