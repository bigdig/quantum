<<<<<<< HEAD:photon/write_mx_rec.py
from photon.preprocess import Pipeline, LabelGenerator, PipelineNoNorm, PipelineWithZScore
from photon.get_data import get_ohlcvr_and_shuffle_idx, get_normed_ohlcvr_and_shuffled_idx
=======
from get_db_data.preprocess import Pipeline, LabelGenerator, PipelineNoNorm
from get_db_data.get_data import get_ohlcvr_and_shuffle_idx, get_normed_ohlcvr_and_shuffled_idx
>>>>>>> bac26ed5b8036a17ff8f7d8a7d36e0d7606ab4cf:get_db_data/write_mx_rec_from_db.py
import mxnet as mx
import logging
import numpy as np


def write_ohlcvr(use_days,
                 rec_name,
                 from_date='2008-01-01',
                 end_date='2017-08-01',
                 remove_head_num=10,
                 test_write=False):
    dataset, idxs = get_ohlcvr_and_shuffle_idx(use_days,
                                               from_date=from_date,
                                               end_date=end_date,
                                               remove_head_num=remove_head_num,
                                               test_write=test_write)
    record = mx.recordio.MXRecordIO(rec_name, 'w')
    count = 0
    label_gen = LabelGenerator(2)
    pipe = PipelineWithZScore()
    max_label = 0
    min_label = 1000
    for idx in idxs:
        ori_data = dataset[idx[0]][idx[1]: idx[2]]
        # TODO: filter chain, norm_data, generate label
        data = ori_data[:, :-1]
        label = ori_data[:, -1]
        new_data = pipe(data)
        if new_data is None:
            continue
        if new_data.dtype == np.float64:
            new_data = new_data.astype(np.float32)
        label = label_gen(label - 1.0)
        header = mx.recordio.IRHeader(0, label, count, 0)
        packed_s = mx.recordio.pack(header, new_data.tobytes())
        record.write(packed_s)
        count += 1
        if count % 1000 == 0:
            logging.info('write to records: %s', count)
        # if label > max_label:
        #     max_label = label
        # elif label < min_label:
        #     min_label = label
    logging.info('total write %s samples, max_label: %s, min_label: %s', count, max_label, min_label)
    record.close()


def write_ohlcvr_from_normed_data(use_days,
                                  rec_name,
                                  from_date='2008-01-01',
                                  end_date='2017-07-01',
                                  remove_head_num=10,
                                  class_num=20,
                                  test_write=False,
                                  regression=False):
    dataset, idxs = get_normed_ohlcvr_and_shuffled_idx(use_days,
                                                       from_date=from_date,
                                                       end_date=end_date,
                                                       remove_head_num=remove_head_num,
                                                       test_write=test_write)
    record = mx.recordio.MXRecordIO(rec_name, 'w')
    count = 0
    if regression:
        label_gen = lambda x: np.log1p(x)
    else:
        label_gen = LabelGenerator(class_num)
    pipe = PipelineNoNorm()
    max_label = 0
    min_label = 1000
    for idx in idxs:
        ori_data = dataset[idx[0]][idx[1]: idx[2]]
        # TODO: filter chain, norm_data, generate label
        data = ori_data[:, :-1]
        label = ori_data[:, -1]
        if np.any(label > 1.1) or np.any(label < 0.9) or not np.all(np.isfinite(label)):
            continue
        new_data = pipe(data)
        if new_data is None:
            continue
        if new_data.dtype == np.float64:
            new_data = new_data.astype(np.float32)
        label = label_gen(label - 1.0)
        header = mx.recordio.IRHeader(0, label, count, 0)
        packed_s = mx.recordio.pack(header, new_data.tobytes())
        record.write(packed_s)
        count += 1
        if count % 1000 == 0:
            logging.info('write to records: %s', count)
        # if label > max_label:
        #     max_label = label
        # elif label < min_label:
        #     min_label = label
    logging.info('total write %s samples, max_label: %s, min_label: %s', count, max_label, min_label)
    record.close()


def _unit_write(data_type):
    if data_type == 'standard_ohlcvr':
        write_ohlcvr(50,
                     rec_name='ohlcvr_ratio_norm.rec',
                     test_write=False)
    elif data_type == 'across_normed_ohlcvr':
        write_ohlcvr_from_normed_data(50,
                                      from_date='2017-05-01',
                                      end_date='2017-11-01',
                                      rec_name='norm_data_50_len_2_cls_valid.rec',
                                      class_num=2,
                                      test_write=False)
    elif data_type == 'across_normed_ohlcvr_regression':
        write_ohlcvr_from_normed_data(50,
                                      rec_name='ohlcvr_from_normed_data_for_reg_50_len.rec',
                                      test_write=False,
                                      regression=True)
    else:
        raise NotImplementedError


def _unit_read():
    recordio = mx.recordio.MXRecordIO('ohlcvr_ratio_norm.rec', 'r')
    for _ in range(10):
        item = recordio.read()
        header, data = mx.recordio.unpack(item)
        array = np.frombuffer(data, np.float32)
        print(header.label)
        print(array)


if __name__ == '__main__':
    _unit_write('standard_ohlcvr')
    # _unit_read()
