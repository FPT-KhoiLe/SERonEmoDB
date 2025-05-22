import importlib
import inspect
import pytest
import torch
import pytorch_lightning as pl
from SERonEmoDB.contracts.base_model import BaseLightningModel

# Dynamically import the model module
module = importlib.import_module("SERonEmoDB.models.model")

# Collect all LightningModule subclasses defined in this module
model_classes = [
    obj for name, obj in inspect.getmembers(module, inspect.isclass)
    if issubclass(obj, BaseLightningModel) and obj.__module__ == module.__name__
]

@pytest.mark.parametrize('ModelClass', model_classes)
def test_model_forward_and_training(ModelClass):
    """
    For each LightningModule in the model module:
    - Instantiate with default args (n_classes=7, lr=1e-3 if accepted)
    - Test forward pass on raw waveform
    - Test training_step returns scalar
    - Ensure no NaN/Inf in logits
    """
    # Build kwargs for constructor
    sig = inspect.signature(ModelClass.__init__)
    kwargs = {}
    if 'n_classes' in sig.parameters:
        kwargs['n_classes'] = 7
    if 'lr' in sig.parameters:
        kwargs['lr'] = 1e-3
    if 'input_channels' in sig.parameters:
        kwargs['input_channels'] = 1

    # Instantiate
    model = ModelClass(**kwargs)

    # Raw waveform test: batch size = 2, 1 channel, 16000 samples
    x_raw = torch.randn(2, 1, 16000)
    logits = model(x_raw)

    # Check shape: [2, n_classes]
    n_classes = kwargs.get('n_classes', model.hparams.get('n_classes', logits.size(-1)))
    assert isinstance(logits, torch.Tensor)
    assert logits.shape == (2, n_classes)
    assert torch.isfinite(logits).all()

    # Training step test
    y = torch.zeros(2, dtype=torch.long)
    loss = model.training_step((x_raw, y), batch_idx=0)
    assert isinstance(loss, torch.Tensor)
    assert loss.dim() == 0
