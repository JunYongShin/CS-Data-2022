import pandas as pd
'''
This file processes IMBD file into dataframe.
I splitted this as a single file since it takes
quite of time to process this file.
'''


def get_year(s):
    '''
    This function takes string value year
    and return to an integer value.
    If the year is not in 4 digit format,
    it returns 0
    '''
    if type(s) != int:
        if len(s) == 4:
            s = int(s)
        else:
            s = 0
    return s


def process_imdb():
    '''
    This function takes IMDB file and convert it into a pandas
    dataframe. It also filters and leave only required columns.
    Return filtered dataframe.
    '''
    imdb_data = pd.read_csv('./data_title.tsv', sep='\t')
    imdb_data['startYear'] = imdb_data['startYear'].apply(get_year)
    filtered_imdb = imdb_data[(imdb_data['titleType'] == 'movie') &
                              ((imdb_data['startYear']) >= 2000)]
    filtered_imdb = filtered_imdb.loc[:, ['tconst', 'primaryTitle',
                                          'originalTitle', 'startYear',
                                          'genres']]
    filtered_imdb = filtered_imdb[filtered_imdb['genres'] != r'\N']
    return filtered_imdb


def process_rating():
    '''
    This function process imdb rating file
    and return filtered dataframe.
    '''
    rating_data = pd.read_csv(r'./data.csv')
    rating_filtered = rating_data.loc[:, ['tconst', 'averageRating']]
    return rating_filtered


def main():
    process_imdb()
    process_rating()
    movie_merged = process_imdb().merge(process_rating(),
                                        left_on='tconst', right_on='tconst')
    movie_merged.to_pickle(r"./merged_data.pk1")


if __name__ == '__main__':
    main()
