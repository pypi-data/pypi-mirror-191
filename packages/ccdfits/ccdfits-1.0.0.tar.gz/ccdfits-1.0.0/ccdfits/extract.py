import numpy as np
from skimage.measure import label, regionprops_table
from skimage.filters import apply_hysteresis_threshold
from skimage.segmentation import clear_border
import pandas as pd

def extract_events(image: np.ndarray, low: float, high: float, border=False, 
                   properties=None, rename=True):
    
    
    # first create a binary mask of pixels with events
    mask = apply_hysteresis_threshold(image, low, high)
    
    # exclude events in the border
    if not border:
        mask = clear_border(mask)

    # now label the connected regions of the mask
    labels = label(mask, connectivity=2)

    # create a table with the relevant properties of each event
    if properties is None:
        properties=('area', 'intensity_image', 'label', 
                            'weighted_centroid', 'weighted_moments_central', 
                            'bbox')
    props = regionprops_table(labels, intensity_image=image, 
                              properties=properties)
    
    # create a pandas dataframe with the info
    df = pd.DataFrame(props)

    # but rename stuff for clarity
    if rename:
        if 'weighted_centroid' in properties:
            df.rename(columns={'weighted_centroid-0': 'bar_y',
                            'weighted_centroid-1': 'bar_x'}, 
                    inplace=True)
        
        if 'bbox' in properties:
            df.rename(columns={'bbox-0': 'y_min',
                            'bbox-1': 'x_min',
                            'bbox-2': 'y_max',
                            'bbox-3': 'x_max'}, 
                    inplace=True)

        if 'weighted_moments_central' in properties:
            df.rename(columns={'weighted_moments_central-0-0': 'charge',
                            'weighted_moments_central-0-2': 'var_x',
                            'weighted_moments_central-2-0': 'var_y'}, 
                    inplace=True)

    return df