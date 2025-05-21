# src/seronemodb/data_ingest.py
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

def download_data(dataset="piyushagni5/berlin-database-of-emotional-speech-emodb",
                  root_dir="datas",
                  force_download=False):
    """
    Tải và giải nén EMO-DB từ KaggleHub về `root_dir/<dataset_name>/wav/`.
    Nếu đã tải sẵn (và `force_download=False`), hàm sẽ bỏ qua.
    Trả về đường dẫn đến thư mục chứa .wav.
    """
    dataset_name = dataset.split("/")[-1]
    target_dir = os.path.join(root_dir, dataset_name, "wav")
    archive_path = os.path.join(root_dir, f"{dataset_name}.zip")

    # Nếu đã có và không ép tải lại, exit sớm
    if os.path.isdir(target_dir) and not force_download:
        print(f"[download_data] Data đã tồn tại tại {target_dir}, bỏ qua download.")
        return target_dir

    os.makedirs(root_dir, exist_ok=True)
    print(f"[download_data] Đang tải dataset `{dataset}` về {archive_path} ...")
    archive_path = kagglehub.dataset_download(dataset, path=root_dir)
    print(f"[download_data] Giải nén {archive_path} ...")

    with zipfile.ZipFile(archive_path, "r") as z:
        z.extractall(os.path.join(root_dir, dataset_name))
    # Nếu file zip còn thừa, bạn có thể xóa:
    # os.remove(archive_path)

    # Giả sử thư mục giải nén có cấu trúc .../wav/*.wav
    if not os.path.isdir(target_dir):
        raise RuntimeError(f"Không tìm thấy thư mục WAV tại {target_dir} sau khi giải nén!")
    print(f"[download_data] Hoàn thành. Dữ liệu nằm ở {target_dir}")
    return target_dir

class EmoDBDataset(BaseLightningDataset):
    """
    Dataset for EMO-DB utterances. Labels are parsed from filename (position 6).
    """
    def __init__(self, data_dir, files_list=None, transform=None):
        super().__init__()
        self.data_dir = data_dir
        # Use provided file list or list all WAVs in directory
        self.files = files_list if files_list is not None else [f for f in os.listdir(data_dir) if f.endswith('.wav')]
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx) -> tuple[torch.Tensor, int]:  # Features: [1, T], label
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
    LightningDataModule for EMO-DB: splits data into train/test and provides loaders.
    """
    def __init__(self, data_dir, batch_size=32, transform=None, split_ratio=0.8):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.transform = transform
        self.split_ratio = split_ratio

    def setup(self, stage=None):
        download_data()
        # List and sort files for reproducibility
        all_files = sorted([f for f in os.listdir(self.data_dir) if f.endswith('.wav')])
        n = len(all_files)
        cutoff = int(n * self.split_ratio)
        train_files = all_files[:cutoff]
        test_files  = all_files[cutoff:]

        # Create datasets with explicit file lists
        self.train_ds = EmoDBDataset(self.data_dir, files_list=train_files, transform=self.transform)
        self.test_ds  = EmoDBDataset(self.data_dir, files_list=test_files,  transform=self.transform)

    def pad_collate(self,batch):
        # batch: list of (features, label), features: Tensor [C, T_i]
        feats, labels = zip(*batch)
        # Tìm max time-length
        max_len = max(f.shape[-1] for f in feats)
        # Pad mỗi feature về chiều dài max_len
        padded = [F.pad(f, (0, max_len - f.shape[-1])) for f in feats]
        # Stack và return
        x = torch.stack(padded)
        y = torch.tensor(labels, dtype=torch.long)
        return x, y

    def train_dataloader(self):
        return DataLoader(self.train_ds, batch_size=self.batch_size, shuffle=True, collate_fn=self.pad_collate, num_workers=19)

    def val_dataloader(self):
        return DataLoader(self.test_ds,  batch_size=self.batch_size, shuffle=False, collate_fn=self.pad_collate, num_workers=19)

