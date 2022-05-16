import pandas as pd
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import seaborn as sns
sns.set()

'''
This file was only to save models so that model does not changes everytime.
Once the model and error file is saved, do not run this file again.
'''


def main():
    data_before = pd.read_pickle(r"./data_before.pk1")
    field_lst = ['averageRating', 'log_budget', 'War', 'Western', 'History',
                 'Fantasy', 'Crime', 'Action', 'Thriller', 'Sci-Fi',
                 'Biography', 'Drama', 'Adventure', 'Family', 'Sport',
                 'Romance', 'Mystery', 'Animation', 'Comedy', 'Horror',
                 'Music', 'Documentary', 'News']
    features = data_before.loc[:, field_lst]
    labels = data_before['log_gross']
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.2)
    model = DecisionTreeRegressor()
    model.fit(features_train, labels_train)
    train_predictions = model.predict(features_train)
    test_predictions = model.predict(features_test)
    train_error = mean_squared_error(labels_train, train_predictions)
    test_error = mean_squared_error(labels_test, test_predictions)
    train_predictions = model.predict(features_train)
    test_predictions = model.predict(features_test)
    train_error = mean_squared_error(labels_train, train_predictions)
    test_error = mean_squared_error(labels_test, test_predictions)
    error_lst = [train_error, test_error]
    pickle.dump(model, open('model.sav', 'wb'))
    pickle.dump(error_lst, open('error.sav', 'wb'))


if __name__ == '__main__':
    main()
