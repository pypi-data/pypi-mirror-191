import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer
import tensorflow_text as text
from tensorflow import shape


def positional_encoding(length, depth):
    depth = depth/2

    positions = np.arange(length)[:, np.newaxis]
    depths = np.arange(depth)[np.newaxis, :]/depth

    angle_rates = 1 / (10000**depths)
    angle_rads = positions * angle_rates

    pos_encoding = np.concatenate(
        [np.sin(angle_rads), np.cos(angle_rads)],
      axis=-1)

    return tf.cast(pos_encoding, dtype=tf.float32)


class PositionalEmbeddingLayer(Layer):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.d_model = d_model
        self.Embedding = tf.keras.layers.Embedding(vocab_size, d_model, mask_zero=True)
        self.PositionEnc = positional_encoding(vocab_size, d_model)

    def compute_mask(self, *args, **kargs):
        return self.Embedding.compute_mask(*args, **kargs)

    def call(self, x):
        length = shape(x)[1]
        x = self.Embedding(x)
        # scale
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x = x + self.PositionEnc[tf.newaxis, :length, :]
        return x


class BaseAttentionLayer(Layer):
    def __init__(self,**kargs):
        super().__init__()
        self.mha = tf.keras.layers.MultiHeadAttention(**kargs)
        self.norm = tf.keras.layers.LayerNormalization()
        self.add = tf.keras.layers.Add()

class CrossAttention(BaseAttentionLayer):
    def __call__(self,x,context):
        attn_out , attn_score = self.mha(
        query=x,
        key=context,
        value=context,
        return_attention_scores=True)
        self.last_attn_scr = attn_score
        x = self.add([x,attn_out])
        x = self.norm(x)
        return x

class GlobalSelfAttention(BaseAttentionLayer):
    def call(self,x):
        attn_out = self.mha(
        query=x,
        key=x,
        value=x)
        x = self.add([x,attn_out])
        x = self.norm(x)
        return x

class CasualSelfAttention(BaseAttentionLayer):
    def call(self,x):
        # using mask here cuz the model should not be exposed to words he hasnt seen before
        attn_out = self.mha(
        query=x,
        key=x,
        value=x,
        use_causal_mask = True)
        x = self.add([x,attn_out])
        x = self.norm(x)
        return x


class FeedForward(Layer):
    def __init__(self, d_model, forward_expansion, dropout):
        super().__init__()
        self.d_model = d_model
        self.seq = tf.keras.models.Sequential([
            tf.keras.layers.Dense(self.d_model * forward_expansion),
            tf.keras.layers.Dense(self.d_model),
            tf.keras.layers.Dropout(dropout)
        ])
        self.add = tf.keras.layers.Add()
        self.norm = tf.keras.layers.LayerNormalization()

    def call(self, x):
        x = self.add([x, self.seq(x)])
        x = self.norm(x)
        return x


class EncodeLayer(Layer):
    def __init__(self, *, d_model, num_heads, forward_expansion, dropout):
        super().__init__()
        self.gbl = GlobalSelfAttention(num_heads=num_heads, key_dim=d_model, dropout=dropout)
        self.ff = FeedForward(d_model=d_model, forward_expansion=forward_expansion, dropout=dropout)

    def call(self, x):
        x = self.gbl(x)
        x = self.ff(x)
        return x


class Encoder(Layer):
    def __init__(self, *, d_model,
                 vocab_size,
                 num_layers,
                 num_heads,
                 forward_expansion,
                 dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        self.positionenc = PositionalEmbeddingLayer(vocab_size=vocab_size, d_model=d_model)
        self.enclayers = [
            EncodeLayer(d_model=self.d_model, num_heads=num_heads, forward_expansion=forward_expansion, dropout=dropout)
            for _ in range(num_layers)
        ]
        self.dropout = tf.keras.layers.Dropout(dropout)

    def call(self, x):
        x = self.positionenc(x)
        for i in range(self.num_layers):
            x = self.enclayers[i](x)
        x = self.dropout(x)
        return x


class DecoderLayer(Layer):
    def __init__(self, *, d_model, num_heads, forward_expansion, dropout):
        super().__init__()
        self.casualatt = CasualSelfAttention(num_heads=num_heads, key_dim=d_model, dropout=dropout)
        self.crossatt = CrossAttention(num_heads=num_heads, key_dim=d_model, dropout=dropout)
        self.ff = FeedForward(d_model=d_model, forward_expansion=forward_expansion, dropout=dropout)

    def call(self, x, context):
        x = self.casualatt(x)
        x = self.crossatt(x=x, context=context)
        self.last_attn_scr = self.crossatt.last_attn_scr
        x = self.ff(x)
        return x


class Decoder(Layer):
    def __init__(self, *, d_model, num_layers, num_heads, forward_expansion, vocab_size, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        self.posenc = PositionalEmbeddingLayer(vocab_size=vocab_size, d_model=d_model)
        self.dropout = tf.keras.layers.Dropout(dropout)
        self.declayers = [
            DecoderLayer(d_model=d_model, num_heads=num_heads, forward_expansion=forward_expansion, dropout=dropout)
            for _ in range(num_layers)
        ]
        self.last_attn_scr = None

    def call(self, x, context):
        x = self.posenc(x)
        x = self.dropout(x)
        for i in range(self.num_layers):
            x = self.declayers[i](x=x, context=context)
        self.last_attn_scr = self.declayers[-1].last_attn_scr
        return x


class Transformer(Model):
    def __init__(self, *, num_layers, d_model, num_heads, forward_expansion, inpt_vocab_size, tar_vocab_size,
                 dropout=0.1):
        '''

        :param num_layers: Number Of Encoder / Decoder Layers to use.
        :param d_model: Dimensionality of the model.
        :param num_heads: Number of Heads for MultiHead Attention.
        :param forward_expansion: Expansion Factor For Feed Forward Dense Network.
        :param inpt_vocab_size: Input Vocab Size.
        :param tar_vocab_size: Target Vocab Size.
        :param dropout: Dropout factor for Dropout layer . (Default = 0.1)
        '''
        super().__init__()
        self.Encoder = Encoder(d_model=d_model,
                               vocab_size=inpt_vocab_size,
                               num_layers=num_layers,
                               num_heads=num_heads,
                               forward_expansion=forward_expansion,
                               dropout=dropout)
        self.Decoder = Decoder(d_model=d_model,
                               num_layers=num_layers,
                               num_heads=num_heads,
                               forward_expansion=forward_expansion,
                               vocab_size=tar_vocab_size,
                               dropout=dropout)
        self.final_layer = tf.keras.layers.Dense(tar_vocab_size)

    def call(self, inputs):
        context, x = inputs
        context = self.Encoder(context)
        x = self.Decoder(x, context)
        logits = self.final_layer(x)
        try:
            del logits._keras_mask
        except AttributeError:
            pass
        return logits