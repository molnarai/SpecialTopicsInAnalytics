import os
import json
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    
    # plt.show()


def load_and_scale(file_name: str, max_dim = 400):
    img = cv2.imread(file_name)
    # Calculate scaling factor
    h, w = img.shape[:2]
    scale = min(max_dim / h, max_dim / w)
    
    # Scale image if needed
    if scale < 1:
        new_h, new_w = int(h * scale), int(w * scale)
        scaled_image = cv2.resize(img, (new_w, new_h))
    else:
        scaled_image = img
        
    return scaled_image

#     _                      _        _   _                 
#    / \   _ __  _ __   ___ | |_ __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| '_ \ / _ \| __/ _` | __| |/ _ \| '_ \/ __|
#  / ___ \| | | | | | | (_) | || (_| | |_| | (_) | | | \__ \
# /_/   \_\_| |_|_| |_|\___/ \__\__,_|\__|_|\___/|_| |_|___/
                                                          

# ! ls -l {DATAPATH}/mtsd_v2_fully_annotated/annotations/
def load_annotations(file_path: str, save: bool = True) -> pd.DataFrame:
    """
    Use with: load_annotations(f"{DATAPATH}/mtsd_v2_fully_annotated")
    """
    csv_file = f"{os.path.basename(file_path)}.csv"
    if os.path.isfile(csv_file):
        annotations_df = pd.read_csv(csv_file)
        print(f"Loading from disk: {csv_file}")
        print(f"Number of records: {annotations_df.shape[0]:,}")
        return annotations_df
    
    # files = os.listdir(f"{file_path}/annotations/")
    files = glob.glob(f"{file_path}/annotations/*.json")
    
    annotations_list = []
    for json_file in files:
        # json_file = "{file_path}/annotations/{f}"
        try:
            annotation_data = json.load(open(json_file, "r", encoding='utf-8'))
            # annotation_data['objects']
            temp_df = pd.DataFrame.from_records(annotation_data['objects'])
            temp_df['file_name'] = json_file
            annotations_list.append(temp_df)
        except Exception as ex:
            print(f"Problem loading file '{json_file}': {ex}")
            
        
    
    annotations_df = pd.concat(annotations_list)
    annotations_df["slug"] = annotations_df["file_name"].map(lambda f: os.path.basename(f).split('.')[0])
    
    print(f"Number of records: {annotations_df.shape[0]:,}")
    if save:
        annotations_df.to_csv(csv_file, index=None)
    return annotations_df

