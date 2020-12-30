import sys
import numpy as np
import paddle_fl as pfl
import paddle_fl.mpc.data_utils.alignment as alignment


def align_and_filter(input_file, data_shape, party_id, endpoints, is_receiver):
    """
    Align data between alice and bob. Then filter and save the data based
    on alignment result.

    Args:
        input_file: The file that save data to align.
        data_shape: The shape of saved data.
        party_id: The ID of this party.
        endpoints: The endpoints of all parties.
        is_receiver: Whether this party is receiver.

    Examples:
        For bob whose data file is bob.dat, data shape (i.e., feature shape)
        is 13, ID is 0, he use this method as follows:
        align_and_filter(input_file='bob.dat',
                        data_shape=13,
                        party_id=0,
                        endpoints='0:127.0.0.1:11111,1:127.0.0.1:22222',
                        is_receiver=True)

    """
    input_array = np.fromfile(input_file, sep=' ')
    input_array = input_array.reshape(input_array.shape[0] // (data_shape + 1),
                                      data_shape + 1)
    input_set = map(int, set(input_array[:, 0]))
    input_set = map(str, input_set)
    input_set = set(input_set)
    if is_receiver == 'True':
        is_receiver = True
    else:
        is_receiver = False
    # do alignment
    result = alignment.align(input_set=input_set,
                             party_id=party_id,
                             endpoints=endpoints,
                             is_receiver=is_receiver)
    # store filtered data
    filtered_data = []
    for r in result:
        idx = list(np.array(input_array[:, 0]).astype(np.int)).index(int(r))
        filtered_data.append(input_array[idx])
    filtered_data = np.array(filtered_data)
    if party_id == 0:
        filtered_file = 'alice_filtered.dat'
    else:
        filtered_file = 'bob_filtered.dat'
    filtered_data.tofile(filtered_file, sep=' ')


align_and_filter(input_file=sys.argv[1],
                 data_shape=int(sys.argv[2]),
                 party_id=int(sys.argv[3]),
                 endpoints=sys.argv[4],
                 is_receiver=sys.argv[5])