import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


'''
This file includes functions that plot data using
final merged data from previous files.
'''

final_data_merged = pd.read_pickle(r"./finaldf.pk1")


def convert_log(s):
    '''
    This function take int value
    and return log value.
    If input is 0, return 0.
    '''
    if s == 0:
        s = 0
    else:
        s = math.log(s)
    return s


def testing_set1():
    '''
    This function does one hot encoding
    '''
    testing_set = final_data_merged['genres'].str.join('|').str.get_dummies()
    return testing_set


def per_genre(df, col1):
    '''
    get buget per genre
    or boxoffice per genre
    depending col1 parameter.
    '''
    p_g = testing_set1().mul(df[col1], axis='index')
    return p_g


def plot_per_genre_before(boxoffice_per_unit_budget_before):
    '''
    This function plot box office per unit budget vs genre
    graph. It uses data before COVID.
    '''
    bpub = boxoffice_per_unit_budget_before
    bpub = bpub.sort_values()
    fig, ax = plt.subplots(1, figsize=(10, 7))
    bpub.plot.bar(ax=ax, x=bpub.index,
                  y=bpub.values)
    plt.xlabel('Genres')
    plt.ylabel('Performance Budget Ratio')
    plt.title('Preformance Budget Ratio for Each Genre Before Covid')
    plt.savefig('./plot_per_genre_before.jpg')


def plot_per_genre_after(boxoffice_per_unit_budget_after):
    '''
    This function plot box office per unit budget vs genre
    graph using data after COVID.
    '''
    bpua = boxoffice_per_unit_budget_after.sort_values()
    fig, ax = plt.subplots(1, figsize=(10, 7))
    bpua.plot.bar(ax=ax, x=bpua.index,
                  y=bpua.values)
    plt.xlabel('Genres')
    plt.ylabel('Performance Budget Ratio')
    plt.title('Preformance Budget Ratio for Each Genre After Covid')
    plt.savefig('./plot_per_genre_after.jpg')


def plot_budget_gross_line(df):
    '''
    Plot Budget gross graph.
    It draws line graph.
    '''
    sns.relplot(data=df, x='ProductionBudget', y='DomesticGross', kind='line')
    plt.title('Budget Gross Plot (Before Covid)')
    plt.savefig('./budget_gross_before_line.jpg')


def plot_budget_gross_point(df):
    '''
    Plot Budget gross graph.
    It draws point graph.
    '''
    sns.relplot(data=df, x='ProductionBudget', y='DomesticGross')
    plt.title('Budget Gross Plot (Before Covid)')
    plt.savefig('./budget_gross_before_dot.jpg')


def log_plot(df, x_name, y_name, title_name, file_name):
    '''
    Plot Budget gross graph using log value.
    '''
    sns.relplot(data=df, x=x_name, y=y_name)
    plt.title(title_name)
    plt.savefig('./' + file_name + '.jpg')


def main():
    final_data_merged = pd.read_pickle(r"./finaldf.pk1")
    lb = 'log_budget'
    pb = 'ProductionBudget'
    final_data_merged[lb] = final_data_merged[pb].apply(convert_log)
    lg = 'log_gross'
    dg = 'DomesticGross'
    final_data_merged[lg] = final_data_merged[dg].apply(convert_log)
    testing_set = testing_set1()
    final_data_merged = pd.merge(final_data_merged,
                                 testing_set, left_index=True,
                                 right_index=True)
    final_data_merged.to_pickle(r"./fin_finaldf.pk1")
    is_before = (final_data_merged['startYear'] >= 2000) & \
                (final_data_merged['startYear'] <= 2019)
    is_after = (final_data_merged['startYear'] > 2019) & \
               (final_data_merged['startYear'] <= 2021)
    data_before = final_data_merged[is_before]
    data_before.to_pickle(r"./data_before.pk1")
    data_after = final_data_merged[is_after]
    data_after.to_pickle(r"./data_after.pk1")
    budget_per_genre_before = per_genre(data_before, 'ProductionBudget')
    boxoffice_per_genre_before = per_genre(data_before, 'DomesticGross')
    budget_per_genre_after = per_genre(data_after, 'ProductionBudget')
    boxoffice_per_genre_after = per_genre(data_after, 'DomesticGross')
    budgetsum_before = budget_per_genre_before.sum()
    boxofficesum_before = boxoffice_per_genre_before.sum()
    budgetsum_after = budget_per_genre_after.sum()
    boxofficesum_after = boxoffice_per_genre_after.sum()
    boxoffice_per_unit_budget_before = budgetsum_before / boxofficesum_before
    boxoffice_per_unit_budget_after = budgetsum_after / boxofficesum_after

    plot_per_genre_before(boxoffice_per_unit_budget_before)
    plot_per_genre_after(boxoffice_per_unit_budget_after)
    plot_budget_gross_line(data_before)
    plot_budget_gross_point(data_before)
    log_plot(data_before, 'log_budget', 'log_gross',
             'Budget Gross (Log) Before Covid', 'budget_gross_log')

    log_plot(data_before, 'averageRating', 'log_gross',
             'Rating Gross (Log) Before Covid', 'rating_gross_log')


if __name__ == '__main__':
    main()
