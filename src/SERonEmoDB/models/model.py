import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as pl
from torchmetrics import Accuracy
from SERonEmoDB.contracts.base_model import BaseLightningModel

class EmotionClassifier(BaseLightningModel):
    """
    A PyTorch Lightning module implementing a 1D-CNN for speech emotion recognition.
    
    This classifier processes audio inputs (raw waveform or MFCCs) through a series of 
    1D convolutional layers followed by a linear classifier to predict emotions.

    Architecture:
        - 2 convolutional layers with ReLU activation and pooling
        - Adaptive max pooling to collapse time dimension
        - Linear classifier for final prediction

    Args:
        n_classes (int, optional): Number of emotion classes to predict. Defaults to 7.
        lr (float, optional): Learning rate for the Adam optimizer. Defaults to 1e-3.
        input_channels (int, optional): Number of input channels (1 for raw waveform, n for MFCCs). 
            Defaults to 1.

    Attributes:
        accuracy: Multiclass accuracy metric using macro averaging
        conv: Sequential container of convolutional layers for feature extraction
        classifier: Linear layer for final classification
    """
    def __init__(self, n_classes: int = 7, lr: float = 1e-3, input_channels: int = 1):
        super().__init__()
        self.save_hyperparameters()
        self.accuracy = Accuracy(task="multiclass", num_classes=n_classes, average="macro")
        
        # Convolutional feature extractor
        self.conv = nn.Sequential(
            nn.Conv1d(self.hparams.input_channels, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
            nn.Conv1d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveMaxPool1d(1),  # Collapse time dim -> 1
        )

        self.classifier = nn.Linear(32, self.hparams.n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the model.

        Args:
            x (torch.Tensor): Input tensor of shape [batch_size, channels, time_steps]

        Returns:
            torch.Tensor: Logits tensor of shape [batch_size, n_classes]
        """
        h = self.conv(x)
        h = h.view(h.size(0), -1)
        return self.classifier(h)

    def training_step(self, batch, batch_idx):
        """
        Performs a single training step.

        Args:
            batch (tuple): Tuple containing input tensor and target labels
            batch_idx (int): Index of the current batch

        Returns:
            torch.Tensor: Computed loss value
        """
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        preds = logits.argmax(dim=-1)
        acc = self.accuracy(preds, y)
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        """
        Performs a single validation step.

        Args:
            batch (tuple): Tuple containing input tensor and target labels
            batch_idx (int): Index of the current batch
        """
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        preds = logits.argmax(dim=-1)
        acc = self.accuracy(preds, y)
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)

    def configure_optimizers(self):
        """
        Configures the optimizer for training.

        Returns:
            torch.optim.Optimizer: Adam optimizer with specified learning rate
        """
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)


