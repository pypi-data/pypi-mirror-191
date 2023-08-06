#from kapre.composed import get_melspectrogram_layer
import tensorflow as tf

from kolibri.backend.tensorflow.layers.att_wgt_avg_layer import AttentionWeightedAverage, AttWgtAvgLayer
from kolibri.backend.tensorflow.layers.att_wgt_avg_layer import AttentionWeightedAverageLayer
from kolibri.backend.tensorflow.layers.folding_layer import FoldingLayer
from kolibri.backend.tensorflow.layers.kmax_pool_layer import KMaxPoolingLayer, KMaxPoolLayer, KMaxPooling
from kolibri.backend.tensorflow.layers.non_masking_layer import NonMaskingLayer
from kolibri.backend.tensorflow.layers.multi_head_attention import MultiHeadSelfAttention
from kolibri.backend.tensorflow.layers.crf import ConditionalRandomField
from kolibri.backend.tensorflow.layers.behdanau_attention import BahdanauAttention  # type: ignore
from typing import Dict, Any
from tensorflow import keras



L = keras.layers
L.BahdanauAttention = BahdanauAttention
L.KConditionalRandomField = ConditionalRandomField


def resigter_custom_layers(custom_objects: Dict[str, Any]) -> Dict[str, Any]:
    custom_objects['ConditionalRandomField'] = ConditionalRandomField
    custom_objects['BahdanauAttention'] = BahdanauAttention
    return custom_objects


if __name__ == "__main__":
    pass
