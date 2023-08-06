# Tensorflow Model Playground

- Different tensorflow Deep Learning model & Helper Function.
- Currently Included Generative Adversarial Networks , some helper function and Transformer.

## Usage Example
### Generative Adversarial Networks
* Simple CycleGAN

```python
from modelpg.GAN import build_generator , build_descriminator , composite_model,train_model
generator_1 = build_generator(image_shape=(256,256))
generator_2 = build_generator(image_shape=(256,256))

descriminator_1 = build_descriminator(image_shape=(256,256))
descriminator_2 = build_descriminator(image_shape=(256,256))

composite_1 = composite_model(generator_1,descriminator_1,generator_2,image_shape=(256,256))
composite_2 = composite_model(generator_2,descriminator_2,generator_1,image_shape=(256,256))

train_model(descriminator_1,descriminator_2,generator_1,generator_2,composite_1,composite_2,dataset,epochs=100)
```

- After training use each generator to generate images.


### Transformer
```python
from modelpg.Transformer import Transformer
num_layers = 4
d_model = 512
dff = 4
num_heads = 8
dropout_rate = 0.5
tf = Transformer(num_layers=num_layers,
                num_heads=num_heads,
                d_model = d_model,
                forward_expansion=dff,
                inpt_vocab_size=2000,
                tar_vocab_size=2000,
                dropout=dropout_rate)
```
Train this transformer using custom training loop or by `.fit()` method.
**Note : `.fit` would take ((query , key),value) as parameter here X = (query,key) & Y = (value).**