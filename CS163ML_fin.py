import pandas as pd
import pickle
import math
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

'''
This file uses ML model and data merged from
previous files to plot and analyze data.
'''


def main():
    data_after = pd.read_pickle(r"./data_after.pk1")
    field_lst = ['averageRating', 'log_budget', 'War', 'Western', 'History',
                 'Fantasy', 'Crime', 'Action', 'Thriller', 'Sci-Fi',
                 'Biography', 'Drama', 'Adventure', 'Family', 'Sport',
                 'Romance', 'Mystery', 'Animation', 'Comedy', 'Horror',
                 'Music', 'Documentary', 'News']
    model = pickle.load(open('model.sav', 'rb'))
    error = pickle.load(open('error.sav', 'rb'))
    print(error)
    features_after = data_after.loc[:, field_lst]
    after_predict = model.predict(features_after)
    black_widow_tconst = 'tt3480822'
    is_black_widow = data_after['tconst'] == black_widow_tconst
    black_widow = data_after[is_black_widow]
    black_widow_features = black_widow.loc[:, field_lst]
    pred1 = model.predict(black_widow_features)[0]
    actual = black_widow['log_gross'].values
    names = ['Actual val', 'Predicted Val']
    vals = [math.exp(actual), math.exp(pred1)]
    print(actual, pred1)
    print(vals[1] - vals[0])
    print('Black Widow percent diff: ', (vals[1]-vals[0])/vals[0]*100)
    fig, ax = plt.subplots(1, figsize=(10, 7))
    ax.bar(names, vals)
    plt.ylabel('Gross ($)')
    plt.title('Black Widow Difference betwwen actual and '
              'expected ($50710807), MeanSquaredError:18')
    plt.savefig('./BlackWidow.jpg')
    after_predict = model.predict(features_after)
    after_predict = after_predict.sum()
    actual_gross = data_after['log_gross'].sum()
    name = ['actual', 'predict']
    vals = [actual_gross, after_predict]
    difference = after_predict - actual_gross
    print(difference)
    print(math.exp(difference))
    print('difference in percent: ',
          math.exp(difference)/math.exp(actual_gross)*100)
    fig, ax = plt.subplots(1, figsize=(10, 7))
    ax.bar(name, vals)
    plt.ylabel('Gross in log scale')
    plt.title('Difference between actual and '
              'expected in log scale($1.13e+66 difference),'
              ' MeanSquredError:18')
    plt.savefig('./actual_pred.jpg')


if __name__ == '__main__':
    main()
