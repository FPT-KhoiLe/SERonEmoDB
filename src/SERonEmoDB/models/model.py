import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as pl
from torchmetrics import Accuracy

class EmotionClassifier(pl.LightningModule):
    """
    Simple 1D-CNN for speech emotion recognition.
    - Input: [B, C, T] (C=1 for raw waveform, or C=n for MFCCs)
    - Output: [B, n_classes]
    """
    def __init__(self, n_classes : int = 7, lr : float = 1e-3, input_channels : int = 1):
        super().__init__()
        self.save_hyperparameters()
        self.accuracy = Accuracy(task="multiclass", num_classes=n_classes, average="macro")
        # Convolutional feature extractor
        # If input C != 1, it still works by matching C to conv1 in_channels.
        self.conv = nn.Sequential(
            nn.Conv1d(self.hparams.input_channels, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
            nn.Conv1d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveMaxPool1d(1), # Collapse time dim -> 1
        )

        self.classifier = nn.Linear(32, self.hparams.n_classes)

    def forward(self, x : torch.Tensor) -> torch.Tensor:
        """
        x: [B, C, T]
        return: logits [B, n_classes]
        """
        h = self.conv(x)
        h = h.view(h.size(0), -1)
        return self.classifier(h)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        preds = logits.argmax(dim=-1)
        acc = self.accuracy(preds, y)
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        preds = logits.argmax(dim=-1)
        acc = self.accuracy(preds, y) # accuracy = % dự đoán đúng
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)

