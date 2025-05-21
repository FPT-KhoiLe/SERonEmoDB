"""
Type definitions and interfaces for the SERonEmoDB project.

This module defines common data structures and protocols used throughout the project 
to ensure type consistency and provide clear interfaces between components.

Classes:
    Batch: A dataclass representing a batch of audio data and corresponding emotion labels.
    Transform: A protocol defining the interface for audio transformation functions.
"""
from typing import Protocol, Tuple, Any
from torch import Tensor
from dataclasses import dataclass

@dataclass
class Batch:
    """
    Represents a batch of data for model training or inference.
    
    This dataclass encapsulates the input features and target labels for a batch
    of speech emotion recognition data.
    
    Attributes:
        x (Tensor): Input tensor with shape [B, C, T] where:
                    - B is the batch size
                    - C is the number of channels (1 for raw waveform, or n for MFCCs)
                    - T is the sequence length (time dimension)
        y (Tensor): Target labels tensor with shape [B] containing emotion class indices
    """
    x: Tensor          # [B, C, T]
    y: Tensor          # [B]

class Transform(Protocol):
    """
    Protocol defining the interface for audio transformation functions.
    
    This protocol specifies that any audio transformation must implement a __call__ 
    method that takes a waveform tensor and returns a transformed tensor. Implementations
    might include feature extractors like MFCC, spectrogram, or audio augmentations.
    
    Methods:
        __call__(wav: Tensor) -> Tensor: Transform a waveform into another representation
            Args:
                wav (Tensor): Audio waveform, typically with shape [1, T] where T is the time dimension
            Returns:
                Tensor: Transformed representation of the input waveform
    """
    def __call__(self, wav: Tensor) -> Tensor: ...
