import tensorflow as tf
from tensorflow.contrib.layers import fully_connected
from rnn_config import *


def _single_cell(num_units, cell_type, forget_bias=1.0, residual_connection=False):
    if cell_type == 'GRU':
        cell = tf.contrib.rnn.GRUCell(num_units)
    elif cell_type == 'LSTM':
        cell = tf.contrib.rnn.BasicLSTMCell(num_units=num_units,
                                            forget_bias=forget_bias)
    elif cell_type == 'RNN':
        cell = tf.contrib.rnn.BasicRNNCell(num_units=num_units)
    elif cell_type == 'GridLSTM':
        cell = tf.contrib.rnn.GridLSTMCell(num_units=num_units,
                                           num_frequency_blocks=[1, 2, 3])
    elif cell_type == 'LayerNormLSTM':
        cell = tf.contrib.rnn.LayerNormBasicLSTMCell(
            num_units,
            dropout_keep_prob=1.0,
            forget_bias=forget_bias,
            layer_norm=True)
    else:
        raise Exception
    if residual_connection:
        cell = tf.contrib.rnn.ResidualWrapper(cell)
    return cell


def _gradient_clip(gradients, max_gradient_norm):
    """Clipping gradients of a model."""
    clipped_gradients, gradient_norm = tf.clip_by_global_norm(
        gradients, max_gradient_norm)
    return clipped_gradients


def get_model(batch_data, batch_label, is_train=True):
    cell_list = []
    for i in range(NUM_LAYERS):
        residual_connection = i >= NUM_LAYERS - NUM_RESIDUAL_LAYERS
        cell = _single_cell(HIDDEN_UNITS,
                            CELL_TYPE,
                            residual_connection=residual_connection)
        # if i == 0:
        #     cell = tf.contrib.rnn.AttentionCellWrapper(cell,
        #                                                attn_length=ATTN_LENGTH,
        #                                                state_is_tuple=True)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell, output_keep_prob=DROPOUT_KEEP)
        cell_list.append(cell)
    multi_cell = tf.contrib.rnn.MultiRNNCell(cell_list)
    # batch_data = fully_connected(batch_data,
    #                              num_outputs=INPUT_FC_NUM_OUPUT,
    #                              activation_fn=None)
    output, state = tf.nn.dynamic_rnn(multi_cell,
                                      inputs=batch_data,
                                      dtype=tf.float32,
                                      time_major=False)
    output = output[:, -PREDICT_LEN:, :]
    print('lstm output shape: %s' % output.get_shape())
    output_reshape = tf.reshape(output, shape=(-1, HIDDEN_UNITS))
    # fc_output_0 = fully_connected(inputs=output_reshape,
    #                               num_outputs=FC_NUM_OUTPUT,
    #                               normalizer_fn=tf.contrib.layers.batch_norm)
    pred = fully_connected(output_reshape,
                           num_outputs=1,
                           activation_fn=None)
    # logits = tf.clip_by_value(logits, 1e-8, 0.95)
    reshaped_label = tf.reshape(batch_label, shape=(-1,))
    reg_loss = tf.reduce_mean(tf.squared_difference(pred, reshaped_label))
    trainable_vars = tf.trainable_variables()
    gradients = tf.gradients(reg_loss, trainable_vars)  # ,
    clipped_gradients = _gradient_clip(gradients, max_gradient_norm=1.0)
    global_step = tf.Variable(0, trainable=False)
    warm_up_factor = 0.9
    warm_up_steps = 200
    learning_rate_warmup_steps = 200
    inv_decay = warm_up_factor ** (tf.to_float(warm_up_steps - global_step))
    learning_rate = LR
    warm_up_learning_rate = tf.cond(global_step < learning_rate_warmup_steps,
                                    lambda: inv_decay * learning_rate,
                                    lambda: learning_rate)
    lr = tf.train.polynomial_decay(learning_rate=warm_up_learning_rate,
                                   global_step=global_step,
                                   end_learning_rate=END_LR,
                                   decay_steps=DECAY_STEP,
                                   power=0.6)
    opt = tf.train.MomentumOptimizer(lr, 0.9)
    # opt = tf.train.AdamOptimizer(lr)
    update = opt.apply_gradients(zip(clipped_gradients, trainable_vars), global_step=global_step)
    return update, reg_loss, lr


# import numpy as np
# (np.log1p(1.1) - np.log1p(1.0)) ** 2