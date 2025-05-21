from abc import ABC, abstractmethod
from torch.utils.data import DataLoader
import lightning as L

class BaseLightningDataset(L.LightningDataModule, ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        pass
    @abstractmethod
    def __len__(self):
        pass
    @abstractmethod
    def __getitem__(self, idx):
        pass

class BaseLightningDataModule(L.LightningDataModule, ABC):
    """Bắt buộc lớp con hiện thực train_dataloader / val_dataloader"""
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def setup(self, stage=None):
        pass
    @abstractmethod
    def pad_collate(self, batch):
        pass
    @abstractmethod
    def train_dataloader(self) -> DataLoader:
        pass
    @abstractmethod
    def val_dataloader(self) -> DataLoader:
        pass