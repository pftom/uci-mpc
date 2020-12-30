import sys
import numpy as np
import time

import paddle
import paddle.fluid as fluid
import paddle_fl.mpc as pfl_mpc
import paddle_fl.mpc.data_utils.aby3 as aby3

role, server, port = sys.argv[1], sys.argv[2], sys.argv[3]
pfl_mpc.init("aby3", int(role), "localhost", server, int(port))
role = int(role)

# data preprocessing
BATCH_SIZE = 10

feature_reader = aby3.load_aby3_shares(
    "tmp/house_feature", id=role, shape=(13, ))
label_reader = aby3.load_aby3_shares("tmp/house_label", id=role, shape=(1, ))
batch_feature = aby3.batch(feature_reader, BATCH_SIZE, drop_last=True)
batch_label = aby3.batch(label_reader, BATCH_SIZE, drop_last=True)

x = pfl_mpc.data(name='x', shape=[BATCH_SIZE, 13], dtype='int64')
y = pfl_mpc.data(name='y', shape=[BATCH_SIZE, 1], dtype='int64')

# async data loader
loader = fluid.io.DataLoader.from_generator(
    feed_list=[x, y], capacity=BATCH_SIZE)
batch_sample = paddle.reader.compose(batch_feature, batch_label)
place = fluid.CPUPlace()
loader.set_batch_generator(batch_sample, places=place)

# network
y_pre = pfl_mpc.layers.fc(input=x, size=1)

infer_program = fluid.default_main_program().clone(for_test=False)

cost = pfl_mpc.layers.square_error_cost(input=y_pre, label=y)
avg_loss = pfl_mpc.layers.mean(cost)
optimizer = pfl_mpc.optimizer.SGD(learning_rate=0.001)
optimizer.minimize(avg_loss)

# loss file
loss_file = "tmp/uci_loss.part{}".format(role)

# train
exe = fluid.Executor(place)
exe.run(fluid.default_startup_program())
epoch_num = 20

start_time = time.time()
for epoch_id in range(epoch_num):
    step = 0

    # Method 1: feed data directly
    # for feature, label in zip(batch_feature(), batch_label()):
    #     mpc_loss = exe.run(feed={"x": feature, "y": label}, fetch_list=[avg_loss])

    # Method 2: feed data via loader
    for sample in loader():
        mpc_loss = exe.run(feed=sample, fetch_list=[avg_loss])

        if step % 50 == 0:
            print('Epoch={}, Step={}, Loss={}'.format(epoch_id, step,
                                                      mpc_loss))
            with open(loss_file, 'ab') as f:
                f.write(np.array(mpc_loss).tostring())
            step += 1

end_time = time.time()
print('Mpc Training of Epoch={} Batch_size={}, cost time in seconds:{}'
      .format(epoch_num, BATCH_SIZE, (end_time - start_time)))