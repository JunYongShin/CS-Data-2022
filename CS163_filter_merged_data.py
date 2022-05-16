import pandas as pd
import requests


'''
This file includes functions to get data from
webpage and conver them info dataframe. Also,
functions in this file will merge both webpage dataframe
and dataframe from CS163_process_imdb file.
'''


movie_merged = pd.read_pickle(r"./merged_data.pk1")


def list_genres(s):
    '''
    This funciton takes strings and
    return a list of genres by splitting ','
    '''
    s = s.split(',')
    return s


movie_merged['genres'] = movie_merged['genres'].apply(list_genres)


def change_gross(s):
    '''
    This function takes string value and
    return interger value.
    '''
    s = s.strip()
    s = s.strip('$').split(',')
    s = ''.join(s)
    return int(s)


def get_year1(s):
    '''
    This function takes string value
    of date and return to integer value
    of year.
    '''
    if s == 'Unknown':
        s = 0
    elif len(s) > 4:
        s = s.split(',')
        s = s[1].strip()
        s = int(s)
    else:
        s = int(s)
    return s


def get_data_from_page(url_address):
    '''
    This function get data from url and
    return to pandas dataframe.
    '''
    url = url_address
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    dfs = pd.read_html(r.text)
    return dfs[0]


def get_budget_df_list():
    '''
    This function loops through links and
    return lists of pandas dataframe.
    '''
    budget_df = []
    for i in range(0, 63):
        if i == 0:
            budget_link = r'https://www.the-numbers.com/movie/budgets/all'
        else:
            budget_link = r'https://www.the-numbers.com/movie/budgets/all/' \
                          + str(100*i+1)
        df = get_data_from_page(budget_link)
        budget_df.append(df)
    return budget_df


def combined_budget():
    '''
    This function combine dataframes and
    return filtered dataframe.
    '''
    budget_df = get_budget_df_list()
    budget_combined = pd.concat(budget_df)
    pb = 'ProductionBudget'
    budget_combined[pb] = budget_combined[pb].apply(change_gross)
    dg = 'DomesticGross'
    budget_combined[dg] = budget_combined[dg].apply(change_gross)
    rd = 'ReleaseDate'
    budget_combined[rd] = budget_combined[rd].apply(get_year1)
    budget_combined = budget_combined[[rd, 'Movie', pb, dg]]
    budget_combined = budget_combined[(budget_combined[rd] >= 2000)]
    return budget_combined


def main():
    budget_combined = combined_budget()
    ot = 'originalTitle'
    m = 'Movie'
    final_merged = movie_merged.merge(budget_combined, left_on=ot, right_on=m)
    year_match = final_merged['startYear'] == final_merged['ReleaseDate']
    final_merged = final_merged[year_match]
    final_merged.to_pickle(r"./finaldf.pk1")


if __name__ == '__main__':
    main()
