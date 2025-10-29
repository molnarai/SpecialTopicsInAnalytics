import cv2
import numpy as np
import matplotlib.pyplot as plt

def imshow(img, max_dim=400, with_axis=False):
    """
    Display an OpenCV image or numpy array with scaling and proper color handling.
    
    Args:
        img: OpenCV image (BGR) or numpy array
        max_dim: Maximum dimension for scaling (default: 400)
        with_axis: Whether to show axes (default: False)
    """
    # Convert BGR to RGB if it's a color OpenCV image
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Calculate scaling factor
    h, w = img.shape[:2]
    scale = min(max_dim / h, max_dim / w)
    
    # Scale image if needed
    if scale < 1:
        new_h, new_w = int(h * scale), int(w * scale)
        scaled_image = cv2.resize(img, (new_w, new_h))
    else:
        scaled_image = img
    
    # Display based on image type
    if len(scaled_image.shape) == 2:  # Grayscale
        plt.imshow(scaled_image, cmap='gray')
    else:  # Color
        plt.imshow(scaled_image)
    
    if not with_axis:
        plt.axis('off')
    
    plt.show()


def load_and_scale(file_name: str, size = (400, 300)):
    img = cv2.imread(file_name)
    img = cv2.resize(img, size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
    

