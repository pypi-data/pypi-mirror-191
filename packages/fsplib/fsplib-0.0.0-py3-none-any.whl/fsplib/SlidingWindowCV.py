import numpy as np
from pandas import DataFrame
# test comm


class SlidingWindowCV():
    '''_summary_
    '''

    def __init__(self, train_size: int, test_size: int) -> None:
        '''_summary_

        Parameters
        ----------
        train_size : int
            Size of training set
        size : int
            Size of validation set
        '''
        self.train_size = train_size
        self.test_size = test_size

    def split(self, X, y=None, groups=None):
        '''_summary_
        '''
        for i in range(34 - self.train_size - self.test_size - 1):
            # train = X['date_block_num].isin(np.arange(i, i + self.train_size))
            train = X[X['date_block_num'].isin(np.arange(i, i + self.train_size))].index
            test = X[X['date_block_num'].isin(np.arange(i + self.train_size + 1, i + self.train_size + self.test_size + 1))].index
            yield train, test



