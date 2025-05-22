from abc import ABC, abstractmethod
from torch.utils.data import DataLoader
import lightning as L

class BaseLightningDataset(L.LightningDataModule, ABC):
    """Abstract base class for Lightning datasets.
    
    This class extends both Lightning's LightningDataModule and Python's ABC (Abstract Base Class)
    to define a template for dataset implementations. Any class inheriting from this must implement
    the abstract methods defined below.
    """
    
    @abstractmethod
    def __init__(self):
        """Initialize the dataset.
        
        Must be implemented by child classes.
        """
        super().__init__()
        pass

    @abstractmethod
    def __len__(self):
        """Return the total number of samples in the dataset.
        
        Must be implemented by child classes.
        
        Returns:
            int: Number of samples in the dataset
        """
        pass

    @abstractmethod
    def __getitem__(self, idx):
        """Get a sample from the dataset at the given index.
        
        Must be implemented by child classes.
        
        Args:
            idx (int): Index of the sample to retrieve
            
        Returns:
            Any: The sample at the given index
        """
        pass

class BaseLightningDataModule(L.LightningDataModule, ABC):
    """Abstract base class for Lightning data modules.
    
    This class provides a template for data module implementations in the Lightning framework.
    Child classes must implement the training and validation data loaders along with other
    required setup methods.
    """

    @abstractmethod
    def __init__(self):
        """Initialize the data module.
        
        Must be implemented by child classes.
        """
        pass

    @abstractmethod
    def setup(self, stage=None):
        """Perform setup operations for different stages of training.
        
        Must be implemented by child classes. This method is called by Lightning to perform
        setup operations before training, validation, or testing begins.
        
        Args:
            stage (str, optional): Stage of training ('fit', 'validate', 'test', or 'predict')
        """
        pass

    @abstractmethod
    def pad_collate(self, batch):
        """Collate and pad a batch of samples.
        
        Must be implemented by child classes. This method should handle any necessary padding
        or processing when combining multiple samples into a batch.
        
        Args:
            batch (list): A list of samples to be collated
            
        Returns:
            Any: The processed batch
        """
        pass

    @abstractmethod
    def train_dataloader(self) -> DataLoader:
        """Create and return the training data loader.
        
        Must be implemented by child classes.
        
        Returns:
            DataLoader: PyTorch DataLoader for the training dataset
        """
        pass

    @abstractmethod
    def val_dataloader(self) -> DataLoader:
        """Create and return the validation data loader.
        
        Must be implemented by child classes.
        
        Returns:
            DataLoader: PyTorch DataLoader for the validation dataset
        """
        pass