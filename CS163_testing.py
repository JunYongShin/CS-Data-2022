import pandas as pd
import CS163_process_imdb
import CS163_filter_merged_data

'''
This file includes testing file.
'''


def test_filtered_year(df):
    '''
    This function tests whether filter is done
    properly
    '''
    is_year = df['startYear'] < 2000
    print('Empty DataFrame', df[is_year])


def test_columns(df):
    '''
    This function tests whether column filter
    is done properly
    '''
    print('Columns =', df.columns)


def test_functions():
    '''
    This function tests get_year function and
    change_gross function
    '''
    print('expected: 2018', CS163_process_imdb.get_year('2018'))
    print('expected: 0', CS163_process_imdb.get_year('10-20-2011'))
    print('expected: 200111000',
          CS163_filter_merged_data.change_gross('$200,111,000'))


def test_data_before(df):
    '''
    This function tests if there is any unwanted year
    value included.
    '''
    is_before = (df['startYear'] < 2000) | (df['startYear'] > 2019)
    print(df[is_before])


def test_data_after(df):
    '''
    This function tests if there is any unwanted year
    value included.
    '''
    is_after = (df['startYear'] > 2021) | (df['startYear'] < 2020)
    print(df[is_after])


def main():
    movie_merged = pd.read_pickle(r"./merged_data.pk1")
    final_data_merged = pd.read_pickle(r"./finaldf.pk1")
    data_before = pd.read_pickle(r"./data_before.pk1")
    data_after = pd.read_pickle(r"./data_after.pk1")
    test_filtered_year(movie_merged)
    test_filtered_year(final_data_merged)
    test_columns(movie_merged)
    test_columns(final_data_merged)
    test_functions()
    test_data_before(data_before)
    test_data_after(data_after)


if __name__ == '__main__':
    main()
