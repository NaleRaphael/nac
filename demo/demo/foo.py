from __future__ import absolute_import

__all__ = ['mul_data_mask', 'mul_mask_data']

# --- These 2 functions do the same thing, but take input parameters in different order. ---
def mul_data_mask(data, mask):
    return data*mask

def mul_mask_data(mask, data):
    return data*mask
