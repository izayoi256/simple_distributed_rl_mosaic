from typing import Tuple

import numpy as np
import torch
import torch.nn as nn


class DQNImageBlock(nn.Module):
    def __init__(
        self,
        in_shape: Tuple[int, ...],
        filter: int = 32,
        activation="ReLU",
        enable_time_distributed_layer: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.enable_time_distributed_layer = enable_time_distributed_layer

        if isinstance(activation, str):
            activation = getattr(nn, activation)

        in_ch = in_shape[-3]

        # (batch, in_ch, 84, 84)
        # -> (batch, 32, 21, 21)
        # -> (batch, 64, 11, 11)
        # -> (batch, 64, 11, 11)
        self.image_layers = nn.ModuleList(
            [
                nn.Conv2d(
                    in_ch,
                    filter,
                    kernel_size=8,
                    stride=4,
                    padding=3,
                    padding_mode="replicate",
                ),
                activation(inplace=True),
                nn.Conv2d(
                    filter,
                    filter * 2,
                    kernel_size=4,
                    stride=2,
                    padding=2,
                    padding_mode="replicate",
                ),
                activation(inplace=True),
                nn.Conv2d(
                    filter * 2,
                    filter * 2,
                    kernel_size=3,
                    stride=1,
                    padding=1,
                    padding_mode="replicate",
                ),
                activation(inplace=True),
            ]
        )

        # --- out shape
        x = np.ones((1,) + in_shape, dtype=np.float32)
        y = self.forward(torch.tensor(x))
        self.out_shape = y.shape[-3:]

    def forward(self, x):
        if self.enable_time_distributed_layer:
            # (batch, seq, c, h, w) -> (batch*seq, c, h, w)
            batch_size, seq, channels, height, width = x.size()
            x = x.view(batch_size * seq, channels, height, width)

        for layer in self.image_layers:
            x = layer(x)

        if self.enable_time_distributed_layer:
            # (batch*seq, c, h, w) -> (batch, seq, c, h, w)
            _, channels, height, width = x.size()
            x = x.view(batch_size, seq, channels, height, width)

        return x


if __name__ == "__main__":
    m = DQNImageBlock((96, 72, 3))
    print(m)
