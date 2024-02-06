'''
Author: Qi7
Date: 2023-01-18 09:48:56
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-02-28 22:59:58
Description: slicing window for the array.
'''
import torch
import numpy as np

def sliding_windows(array, sub_window_size, step_size, start_index=0):
    """return the sliding window sized matrix. (preprocessing)
    input: array is a list with dimension of m x n. m is the timestamp and n is the features number.
    output: 1. the window data 2. window+1 data represent the predict target
    """
    array = np.array(array)
    start = start_index
    num_windows = len(array) - start - 1
    sub_windows = (
        start +
        np.expand_dims(np.arange(sub_window_size), axis=0) +
        np.expand_dims(np.arange(num_windows - sub_window_size + 1), 0).T
    )
    target_index = list(range(start + sub_window_size, len(array), step_size))
    
    return array[sub_windows[::step_size]], array[target_index]

def extract_windows(array, clearing_time_index, max_time, sub_window_size):
    """
    Rolling sub-window. For-loop is been used, which is bad in terms of the performance.
    """
    examples = []
    start = clearing_time_index + 1 - sub_window_size + 1
    
    for i in range(max_time+1):
        example = array[start+i:start+sub_window_size+i]
        examples.append(np.expand_dims(example, 0))
    
    return np.vstack(examples)


def extract_windows_vectorized(array, clearing_time_index, max_time, sub_window_size):
    start = clearing_time_index + 1 - sub_window_size + 1
    
    sub_windows = (
        start +
        # expand_dims are used to convert a 1D array to 2D array.
        np.expand_dims(np.arange(sub_window_size), 0) +
        np.expand_dims(np.arange(max_time + 1), 0).T
    )
    
    return array[sub_windows]

def vectorized_stride_v1(array, clearing_time_index, max_time, sub_window_size,
                         stride_size):
    start = clearing_time_index + 1 - sub_window_size + 1
    
    sub_windows = (
        start + 
        np.expand_dims(np.arange(sub_window_size), 0) +
        np.expand_dims(np.arange(max_time + 1), 0).T
    )
    
    # Fancy indexing to select every V rows.
    return array[sub_windows[::stride_size]]


def vectorized_stride_v2(array, clearing_time_index, max_time, sub_window_size,
                         stride_size):
    start = clearing_time_index + 1 - sub_window_size + 1
    
    sub_windows = (
        start + 
        np.expand_dims(np.arange(sub_window_size), 0) +
        # Create a rightmost vector as [0, V, 2V, ...].
        np.expand_dims(np.arange(max_time + 1, step=stride_size), 0).T
    )
    
    return array[sub_windows]



# testing
# x = [[1,11,111,1111],[5,6,7,8],[9,10,11,12],[2,3,4,5],[5,4,3,2],[2,3,4,1],[4,5,3,2],[2,3,1,4],[2,3,4,1],[2,3,4,1]]
# print(sliding_windows(x, sub_window_size=3, step_size=1))