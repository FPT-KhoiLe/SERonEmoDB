import torch
import torchaudio
import pytest

from SERonEmoDB.data_ingest.data_ingest import EmoDBDataset, EmoDataModule, EMOTION_MAP
from SERonEmoDB.feature_extraction.feature_extraction import TRANSFORMS

def create_dummy_wav(path):
    """Helper to create a 1-second random WAV at 16 kHz."""
    waveform = torch.randn(1, 16000)
    torchaudio.save(str(path), waveform, 16000, format="wav")


@pytest.fixture
def tmp_emodb(tmp_path):
    """Creates a temporary EMODB-like directory with a few WAV files."""
    emotions = ['W', 'L', 'N']  # anger, boredom, neutral
    for emo in emotions:
        fname = f"01a01{emo}a.wav"
        create_dummy_wav(tmp_path / fname)
    return tmp_path


def test_dataset_basic(tmp_emodb):
    ds = EmoDBDataset(str(tmp_emodb))
    # Should have 3 samples
    assert len(ds) == 3
    for features, label in ds:
        # Features must be a Tensor of shape [1, T]
        assert isinstance(features, torch.Tensor)
        assert features.ndim == 2 and features.size(0) == 1
        # Label must be a valid emotion index
        assert label in EMOTION_MAP.values()


@pytest.mark.parametrize("tx_name,tx", TRANSFORMS.items())
def test_datamodule_split_and_loaders(tmp_emodb, tx_name, tx):
    """
    For every transform in TRANSFORMS:
    • 50 % / 50 % split  ⇒ 1 train, 2 test  (tmp fixture has 3 wavs)
    • DataLoader must yield 3-D batch  [B, C, T]  where C == tx.output_channels
    """
    dm = EmoDataModule(
        str(tmp_emodb),
        batch_size=1,
        transform=tx,
        split_ratio=0.5,
    )
    dm.setup()

    # --- dataset lengths ---
    assert len(dm.train_ds) == 1, f"{tx_name}: wrong train len"
    assert len(dm.test_ds) == 2,  f"{tx_name}: wrong test  len"

    # --- dataloader shapes ---
    x, y = next(iter(dm.train_dataloader()))
    assert x.ndim == 3 and y.ndim == 1, f"{tx_name}: Ta cần Input Tensor có shape [B, C, T] và Input Labels có shape [B]"
    assert torch.isfinite(x).all(),              f"{tx_name}: NaN/Inf in batch"
