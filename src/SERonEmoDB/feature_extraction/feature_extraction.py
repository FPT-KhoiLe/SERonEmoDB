import torchaudio
from SERonEmoDB.contracts.types_ import Transform
import torch.nn as nn

class MFCC40(Transform):
    """MFCC (Mel-frequency cepstral coefficients) feature extractor.
    
    This class implements MFCC transformation for audio signals using torchaudio,
    converting raw waveform into 40 MFCC features by default.
    
    Attributes:
        tf (torchaudio.transforms.MFCC): MFCC transformer from torchaudio
        _out (int): Number of MFCC coefficients (output channels)
    
    Args:
        sr (int, optional): Sampling rate of the input audio. Defaults to 16000.
        n_mfcc (int, optional): Number of MFCC coefficients to extract. Defaults to 40.
    """
    
    def __init__(self, sr=16000, n_mfcc=40):
        super().__init__()
        self.tf = torchaudio.transforms.MFCC(
            sample_rate=sr, 
            n_mfcc=n_mfcc,
            melkwargs={
                "n_fft": 400,     # Size of FFT window
                "hop_length": 160  # Number of samples between successive frames
            }
        )
        self._out = n_mfcc

    def __call__(self, wav):
        """Transform audio waveform to MFCC features.
        
        Args:
            wav (torch.Tensor): Input waveform tensor of shape [1, T] where T is the number of samples
        
        Returns:
            torch.Tensor: MFCC features of shape [40, Frames] where Frames is time dimension
        """
        m = self.tf(wav)          # Transform to shape [1, 40, Frames]
        return m.squeeze(0)       # Remove batch dimension to get [40, Frames]

    @property
    def output_channels(self):
        """Get the number of output channels (MFCC coefficients).
        
        Returns:
            int: Number of MFCC coefficients
        """
        return self._out

# Registry of available transforms
TRANSFORMS = {
    "raw": nn.Identity(),    # Returns raw waveform without transformation
    "mfcc": MFCC40(),       # Returns 40 MFCC coefficients
    # "spec": spectrogram(), # Placeholder for spectrogram transform
}