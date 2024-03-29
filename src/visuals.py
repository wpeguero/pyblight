"""Set of functions and algorithms to observe model training."""
import pandas as pd
import plotly.express as px
from pydicom import dcmread
from PIL import Image
import numpy as np

def _main():
    sample_image = "data/Dataset_BUSI_with_GT/benign/benign (1).png"
    sample_mask = "data/Dataset_BUSI_with_GT/benign/benign (1)_mask.png"
    img = Image.open(sample_image)
    msk = Image.open(sample_mask)
    mask = np.asarray(msk).astype('float32')
    image = np.asarray(img)
    print(mask)
    #print(image)
    #fn__image = "data/CBIS-DDSM/CBIS-DDSM/Calc-Test_P_00038_LEFT_CC/08-29-2017-DDSM-NA-96009/1.000000-full mammogram images-63992/1-1.dcm"
    #fn__image_full = "data/CBIS-DDSM/CBIS-DDSM/Calc-Test_P_00038_LEFT_CC_1/08-29-2017-DDSM-NA-94942/1.000000-ROI mask images-18515/1-1.dcm"
    #fn__image_mask = "data/CBIS-DDSM/CBIS-DDSM/Calc-Test_P_00038_LEFT_CC_1/08-29-2017-DDSM-NA-94942/1.000000-ROI mask images-18515/1-2.dcm"
    #ds = dcmread(fn__image)
    #fig = px.imshow(ds.pixel_array)
    #fig.show()
    #ds_full = dcmread(fn__image_full)
    #fig_full = px.imshow(ds_full.pixel_array)
    #fig_full.show()
    #print(ds.pixel_array.shape)
    #ds_mask = dcmread(fn__image_mask)
    #fig_mask = px.imshow(ds_mask.pixel_array)
    #fig_mask.show()


if __name__ == "__main__":
    _main()
