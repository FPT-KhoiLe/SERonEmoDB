"""
EMO-DB Dataset Processing Module

This module provides classes and utilities for handling the Berlin Database of Emotional Speech (EMO-DB),
a dataset containing emotional speech recordings. The module implements PyTorch Dataset and
Lightning DataModule interfaces for seamless integration with deep learning workflows.

Key Components:
- EMOTION_MAP: Mapping between EMO-DB emotion codes and numerical labels
- EmoDBDataset: PyTorch Dataset implementation for EMO-DB
- EmoDataModule: Lightning DataModule for handling data splitting and loading
"""

import os
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from SERonEmoDB.contracts.base_data import BaseLightningDataModule, BaseLightningDataset
import kagglehub
import zipfile


EMOTION_MAP = {
    'W': 0,  # anger (Wut)
    'L': 1,  # boredom (Langeweile)
    'E': 2,  # disgust (Ekel)
    'A': 3,  # anxiety/fear (Angst)
    'F': 4,  # happiness (Freude)
    'T': 5,  # sadness (Trauer)
    'N': 6,  # neutral
}

# def download_data(dataset="piyushagni5/berlin-database-of-emotional-speech-emodb",
#                   root_dir="datas",
#                   force_download=False):
#     """
#     Tải và giải nén EMO-DB từ KaggleHub về `root_dir/<dataset_name>/wav/`.
#     Nếu đã tải sẵn (và `force_download=False`), hàm sẽ bỏ qua.
#     Trả về đường dẫn đến thư mục chứa .wav.
#     """
#     dataset_name = dataset.split("/")[-1]
#     target_dir = os.path.join(root_dir, dataset_name, "wav")
#     archive_path = os.path.join(root_dir, f"{dataset_name}.zip")
#
#     # Nếu đã có và không ép tải lại, exit sớm
#     if os.path.isdir(target_dir) and not force_download:
#         print(f"[download_data] Data đã tồn tại tại {target_dir}, bỏ qua download.")
#         return target_dir
#
#     os.makedirs(root_dir, exist_ok=True)
#     print(f"[download_data] Đang tải dataset `{dataset}` về {archive_path} ...")
#     archive_path = kagglehub.dataset_download(dataset, path=root_dir)
#     print(f"[download_data] Giải nén {archive_path} ...")
#
#     with zipfile.ZipFile(archive_path, "r") as z:
#         z.extractall(os.path.join(root_dir, dataset_name))
#     # Nếu file zip còn thừa, bạn có thể xóa:
#     # os.remove(archive_path)
#
#     # Giả sử thư mục giải nén có cấu trúc .../wav/*.wav
#     if not os.path.isdir(target_dir):
#         raise RuntimeError(f"Không tìm thấy thư mục WAV tại {target_dir} sau khi giải nén!")
#     print(f"[download_data] Hoàn thành. Dữ liệu nằm ở {target_dir}")
#     return target_dir

class EmoDBDataset(BaseLightningDataset):
    """
    Dataset class for loading and processing EMO-DB utterances.
    
    This class handles individual audio file loading and emotion label parsing from filenames.
    Each audio file is expected to have the emotion label as its 6th character in the filename.

    Args:
        data_dir (str): Directory containing the WAV files
        files_list (list, optional): Specific list of files to use. If None, uses all WAV files in data_dir
        transform (callable, optional): Transform to apply to the audio waveform
    
    Returns:
        tuple: (features, label) where features is a tensor of shape [1, T] or transformed shape,
               and label is an integer emotion class index
    """

    def __init__(self, data_dir, files_list=None, transform=None):
        super().__init__()
        self.data_dir = data_dir
        # Use provided file list or list all WAVs in directory
        self.files = files_list if files_list is not None else [f for f in os.listdir(data_dir) if f.endswith('.wav')]
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx) -> tuple[torch.Tensor, int]:
        """
        Load and process a single audio file and its emotion label.

        Args:
            idx (int): Index of the sample to load

        Returns:
            tuple: (features, label)
                - features: Tensor of shape [1, T] containing the audio waveform or transformed features
                - label: Integer emotion class index
        """
        fname = self.files[idx]
        path = os.path.join(self.data_dir, fname)
        waveform, sr = torchaudio.load(path)  # [1, T]
        # Resample to 16 kHz if needed
        if sr != 16000:
            waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)
        # Parse emotion label from filename (6th character)
        letter = fname[5]
        label = EMOTION_MAP.get(letter)
        # Apply transform (e.g., MFCC) if provided
        features = self.transform(waveform) if self.transform else waveform
        return features, label

class EmoDataModule(BaseLightningDataModule):
    """
    Lightning DataModule for EMO-DB dataset handling.

    This class manages dataset splitting, batch creation, and dataloader configuration.
    It provides train and validation dataloaders with automatic padding for variable-length sequences.

    Args:
        data_dir (str): Directory containing the WAV files
        batch_size (int, optional): Batch size for dataloaders. Defaults to 32
        transform (callable, optional): Transform to apply to the audio waveforms
        split_ratio (float, optional): Train/test split ratio. Defaults to 0.8
    """

    def __init__(self, data_dir, batch_size=32, transform=None, split_ratio=0.8):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.transform = transform
        self.split_ratio = split_ratio

    def setup(self, stage=None):
        """
        Prepare train and test datasets.
        
        Splits the available data into train and test sets based on split_ratio.
        Files are sorted for reproducibility before splitting.
        """
        # List and sort files for reproducibility
        all_files = sorted([f for f in os.listdir(self.data_dir) if f.endswith('.wav')])
        n = len(all_files)
        cutoff = int(n * self.split_ratio)
        train_files = all_files[:cutoff]
        test_files = all_files[cutoff:]

        # Create datasets with explicit file lists
        self.train_ds = EmoDBDataset(self.data_dir, files_list=train_files, transform=self.transform)
        self.test_ds = EmoDBDataset(self.data_dir, files_list=test_files, transform=self.transform)

    def pad_collate(self, batch):
        """
        Custom collate function for padding variable-length sequences in a batch.

        Args:
            batch: List of (features, label) tuples

        Returns:
            tuple: (padded_features, labels)
                - padded_features: Tensor with all sequences padded to the longest sequence length
                - labels: Tensor of corresponding emotion labels
        """
        feats, labels = zip(*batch)
        # Find max time-length in batch
        max_len = max(f.shape[-1] for f in feats)
        # Pad each feature to max_len
        padded = [F.pad(f, (0, max_len - f.shape[-1])) for f in feats]
        # Stack and return
        x = torch.stack(padded)
        y = torch.tensor(labels, dtype=torch.long)
        return x, y

    def train_dataloader(self):
        """Returns the training data loader."""
        return DataLoader(self.train_ds, batch_size=self.batch_size, shuffle=True, 
                         collate_fn=self.pad_collate, num_workers=19)

    def val_dataloader(self):
        """Returns the validation data loader."""
        return DataLoader(self.test_ds, batch_size=self.batch_size, shuffle=False, 
                         collate_fn=self.pad_collate, num_workers=19)

