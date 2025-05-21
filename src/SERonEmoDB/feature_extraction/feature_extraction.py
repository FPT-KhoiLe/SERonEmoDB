# src/seronemodb/feature_extraction/feature_extraction.py
import torchaudio
from SERonEmoDB.contracts.types_ import Transform
import torch.nn as nn

class MFCC40(Transform):
    def __init__(self, sr=16000, n_mfcc=40):
        super().__init__()
        self.tf = torchaudio.transforms.MFCC(
            sample_rate=sr, n_mfcc=n_mfcc,
            melkwargs={"n_fft":400, "hop_length":160}
        )
        self._out = n_mfcc                # =40

    def __call__(self, wav):              # wav [1,T]
        m = self.tf(wav)                  # [1, 40, Frames]
        return m.squeeze(0)               # [40, Frames]  ← chuẩn 2-D

    @property
    def output_channels(self):            # cho Model & Trainer biết C
        return self._out

# Registry để Ingest tra cứu
TRANSFORMS = {
    "raw":  nn.Identity(),   # trả waveform
    "mfcc": MFCC40(),          # mặc định 40 coeff
    # "spec": spectrogram(),
}

