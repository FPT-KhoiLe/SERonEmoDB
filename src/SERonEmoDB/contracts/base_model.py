import lightning as L 
from abc import abstractmethod
from .types_ import Batch
from torch import Tensor 

class BaseLightningModel(L.LightningModule):
    """An abstract base class for Lightning models.
    
    This class serves as a template for creating Lightning models by enforcing
    the implementation of essential methods required by the Lightning framework.
    All methods are abstract and must be implemented by derived classes.

    Attributes
    ----------
    None
    
    Methods
    -------
    forward(x : Tensor) -> Tensor
        Abstract method for the forward pass of the model.
    
    training_step(batch : Batch, batch_idx) -> Tensor
        Abstract method defining a single training step.
    
    validation_step(batch : Batch, batch_idx) -> Tensor
        Abstract method defining a single validation step.
    
    configure_optimizers()
        Abstract method for configuring optimizers and learning rate schedulers.
    """
    
    @abstractmethod
    def __init__(self):
        """Initialize the Lightning module.
        
        Must be implemented by derived classes.
        """
        super().__init__()
        pass

    @abstractmethod
    def forward(self, x: Tensor) -> Tensor:
        """Perform the forward pass of the model.
        
        Parameters
        ----------
        x : Tensor
            Input tensor to be processed.
            
        Returns
        -------
        Tensor
            Output tensor from the model.
        """
        pass

    @abstractmethod
    def training_step(self, batch: Batch, batch_idx) -> Tensor:
        """Perform a single training step.
        
        Parameters
        ----------
        batch : Batch
            A batch of training data.
        batch_idx : int
            The index of the current batch.
            
        Returns
        -------
        Tensor
            The computed loss for the training step.
        """
        pass

    @abstractmethod
    def validation_step(self, batch: Batch, batch_idx) -> Tensor:
        """Perform a single validation step.
        
        Parameters
        ----------
        batch : Batch
            A batch of validation data.
        batch_idx : int
            The index of the current batch.
            
        Returns
        -------
        Tensor
            The computed loss for the validation step.
        """
        pass

    @abstractmethod
    def configure_optimizers(self):
        """Configure optimizers and LR schedulers.
        
        Returns
        -------
        Union[Optimizer, Tuple[List[Optimizer], List[_LRScheduler]]]
            A PyTorch optimizer or a tuple of lists containing optimizers
            and learning rate schedulers.
        """
        pass