# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: experimental.py
# time: 2019-05-22 19:35

from typing import Dict, Any

from tensorflow import keras
from keras_self_attention import SeqSelfAttention

import kolibri.backend
from kolibri.backend.tensorflow.tasks.text.labeling import BaseLabelingModel
from kolibri.backend.tensorflow.layers import L


class BLSTMAttentionModel(BaseLabelingModel):
    """Bidirectional LSTM Self Attention Sequence Labeling Model"""

    @classmethod
    def get_default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get hyper parameters of model
        Returns:
            hyper parameters dict
        """
        return {
            'layer_blstm': {
                'units': 64,
                'return_sequences': True
            },
            'layer_self_attention': {
                'attention_activation': 'sigmoid'
            },
            'layer_dropout': {
                'rate': 0.5
            },
            'layer_time_distributed': {},
            'layer_activation': {
                'activation': 'softmax'
            }
        }

    def build_model_arc(self):
        """
        build model architectural
        """
        output_dim = len(self.label_indexer.token2idx)
        config = self.hyper_parameters
        embed_model = self.embedding.embed_model

        layer_blstm = L.Bidirectional(L.LSTM(**config['layer_blstm']),
                                      name='layer_blstm')
        layer_self_attention = SeqSelfAttention(**config['layer_self_attention'],
                                                name='layer_self_attention')
        layer_dropout = L.Dropout(**config['layer_dropout'],
                                  name='layer_dropout')

        layer_time_distributed = L.TimeDistributed(L.Dense(output_dim,
                                                           **config['layer_time_distributed']),
                                                   name='layer_time_distributed')
        layer_activation = L.Activation(**config['layer_activation'])

        tensor = layer_blstm(embed_model.output)
        tensor = layer_self_attention(tensor)
        tensor = layer_dropout(tensor)
        tensor = layer_time_distributed(tensor)
        output_tensor = layer_activation(tensor)

        self.tf_model = keras.Model(embed_model.inputs, output_tensor)


# Register custom layer
kolibri.backend.tensorflow.custom_objects['SeqSelfAttention'] = SeqSelfAttention

if __name__ == "__main__":

    from kolibri.datasets.reader.snips import SnipsIntentCorpus

    train_corpus = SnipsIntentCorpus()
    train_corpus.read(task_name='ner')


    train_x, train_y = train_corpus.get_instances(sub_set='train')
    valid_x, valid_y = train_corpus.get_instances(sub_set='test')
    model = BLSTMAttentionModel()
    model.fit(train_x, train_y, valid_x, valid_y, batch_size=64, epochs=2)
    model.evaluate(valid_x, valid_y)
    model.save("/Users/mohamedmentis/Documents/Mentis/Development/Python/Deep_kolibri/demos/classifier_dnn")