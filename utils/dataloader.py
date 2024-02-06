'''
Author: Qi7
Date: 2023-03-01 08:04:54
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-03-01 08:05:05
Description: 
'''
import torch

class MyLoader(torch.utils.data.Dataset):
    """
    customized data loader for loading the data from dataset
    """
    def __init__(self, data_root, data_label):
        self.data = data_root
        self.label = data_label
        self.length = self.data.shape[0]
    
    def __getitem__(self,index):
        data = self.data[index]
        labels = self.label[index]
        return data, labels
    
    def __len__(self):
        return len(self.data)