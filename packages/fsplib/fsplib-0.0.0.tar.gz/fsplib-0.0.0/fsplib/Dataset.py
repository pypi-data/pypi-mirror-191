from category_encoders import OrdinalEncoder
import pandas as pd
import numpy as np
import re
from category_encoders import OrdinalEncoder


def name_fix(input: str) -> str:
    return re.sub('[!,*/]', '', input).lower()


class Dataset():
    '''Dataset class to handle training/testing data
    '''

    TARGET = 'item_cnt_day'

    def __init__(self) -> None:
        self.encoder = OrdinalEncoder()
        self.num_cols = []
        self.cat_cols = []

    def read_file(self, datapath: str) -> None:
        '''Reads data from .csv file and performs ETL actions

        Parameters
        ----------
        datapath : str
            path to .csv file
        '''

        self.datapath = datapath

        df = pd.read_csv(self.datapath + 'sales_train.csv')
        test = pd.read_csv(self.datapath + 'test.csv').drop(columns='ID')
        test['date_block_num'] = 34
        self.df = pd.concat([df, test])

        self.shops = pd.read_csv(self.datapath + 'shops.csv')
        self.items = pd.read_csv(self.datapath + 'items.csv')
        self.item_categories = pd.read_csv(
            self.datapath + 'item_categories.csv')

        # 0. etl
        # sells
        self.df.drop_duplicates(inplace=True)
        self.df.loc[1163158, 'item_cnt_day'] = 522
        self.df.loc[1163158, 'item_price'] /= 522
        self.df.loc[1163158, 'item_id'] = 6065

        outliers = [484683, 2909818]
        self.df.drop(outliers, inplace=True)

        # categories
        drop_cats = [8, 80]
        to_drop = self.item_categories[self.item_categories['item_category_id'].isin(
            drop_cats)].index
        self.item_categories.drop(to_drop, inplace=True)

        self.item_categories['item_category_name'] = self.item_categories['item_category_name'].apply(
            lambda x: x.lower().split(' - ')
        )
        self.item_categories['item_cat'] = self.item_categories['item_category_name'].apply(
            lambda x: x[0]
        )
        self.item_categories['item_sub_cat'] = self.item_categories['item_category_name'].apply(
            lambda x: x[1] if len(x) > 1 else '')

        extra_cats = [26, 27, 28, 29, 30, 31]
        extra_cats = self.item_categories[self.item_categories['item_category_id'].isin(
            extra_cats)]
        self.item_categories.loc[extra_cats.index, 'item_cat'] = extra_cats['item_cat'].transform(
            lambda x: x.split()[0])
        self.item_categories.loc[extra_cats.index, 'item_sub_cat'] = extra_cats['item_cat'].transform(
            lambda x: x.split()[1]) + ' ' + extra_cats['item_sub_cat']

        # self.item_categories.drop_duplicates(subset='item_category_name',
        #                            inplace=True,
        #                            keep='last')
        # self.item_categories.drop(columns='item_category_name', inplace=True)

        # items
        self.items['item_name'] = self.items['item_name'].transform(name_fix)

        # shops
        self.shops['shop_name'] = self.shops['shop_name'].transform(name_fix)
        self.shops['shop_city'] = self.shops['shop_name'].apply(
            lambda x: x.split()[0])
        fix_shops = {
            0: 57,
            1: 58,
            11: 10,
            # 23: 24  # ???
        }
        for k, v in fix_shops.items():
            self.shops.loc[self.shops['shop_id'] == k, 'shop_id'] = v
            self.df.loc[self.df['shop_id'] == k, 'shop_id'] = v

        self.shops.drop_duplicates(
            subset='shop_id',
            inplace=True
        )

    def transform(self):
        self.df = self.df.groupby(
            by=[
                'date_block_num',
                'shop_id',
                'item_id'
            ]
        ).agg(
            {
                'item_cnt_day': 'sum'
            }
        ).reset_index()

        def add_lag(df, lag: int) -> None:
            shifted = df.loc[:, [
                'date_block_num',
                'shop_id',
                'item_id',
                'item_cnt_day']]
            shifted['date_block_num'] += lag
            df = df.merge(
                shifted,
                how='left',
                on=['date_block_num', 'shop_id', 'item_id'],
                suffixes=(None, '_lag' + str(lag))
            )
            return df.fillna(0)

        self.df = add_lag(self.df, 1)
        self.df = add_lag(self.df, 2)
        self.df = add_lag(self.df, 3)
        self.df = add_lag(self.df, 4)
        self.df = add_lag(self.df, 5)
        self.df = add_lag(self.df, 6)
        self.df = add_lag(self.df, 11)
        self.df = add_lag(self.df, 12)


        self.df = self.df.merge(
            self.shops,
            on='shop_id',
            how='left'
        ).merge(
            self.items,
            on='item_id',
            how='left'
        ).merge(
            self.item_categories,
            on='item_category_id',
            how='left'
        )

        self.cat_cols.extend([
            'shop_name',
            'shop_city',
            'item_cat',
            'item_sub_cat',
            'item_name'
        ])

        self.df = self.df.drop(
            columns=['shop_id',
                     'item_id',
                     'item_category_id',
                     'item_category_name']
        )

        df = self.df.copy()

        def add_group_feature(df: pd.DataFrame, group, new_suf: str):
            temp = self.df.groupby(by=group).sum(
                numeric_only=True).drop(columns='item_cnt_day')
            return df.merge(temp,
                            on=group,
                            suffixes=(None, '_'+new_suf)
                            )

        df = add_group_feature(df, ['date_block_num', 'shop_city'], 'city')
        df = add_group_feature(df, ['date_block_num', 'shop_name'], 'shop')
        df = add_group_feature(
            df, ['date_block_num', 'shop_city', 'item_cat'], 'city_cat')
        df = add_group_feature(
            df, ['date_block_num', 'shop_name', 'item_cat'], 'shop_cat')
        df = add_group_feature(df, ['date_block_num', 'item_cat'], 'cat')
        self.df = df

        self.df = self.df[self.df['date_block_num']>12]

        self.df = self.encoder.fit_transform(self.df)

    def getX(self):
        return self.df[self.df['date_block_num'] < 34].drop(
            columns=['item_cnt_day']
        )

    def getY(self):
        return self.df.loc[self.df['date_block_num'] < 34, 'item_cnt_day']

        # validation schema
    def split(self, cv):
        for train_index, test_index in cv.split(self.df['date_block_num'].unique()):
            train_set = self.df[self.df['date_block_num'].isin(train_index)]
            test_set = self.df[self.df['date_block_num'].isin(test_index)]

            X_train = train_set.drop(columns='item_cnt_day')
            y_train = train_set['item_cnt_day']

            X_test = test_set.drop(columns='item_cnt_day')
            y_test = test_set['item_cnt_day']

            yield X_train, y_train, X_test, y_test

    def create_test(self):
        '''Generates dataset with features to create submission
        '''

        return self.df[self.df['date_block_num'] == 34].drop(
            columns=['item_cnt_day']
        )


if  __name__ == '__main__':
    data = Dataset()
    data.read_file('./data/')
    data.transform()
    data.df.to_csv('data.csv', index=False)