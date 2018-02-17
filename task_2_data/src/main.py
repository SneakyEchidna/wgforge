#!/usr/bin/python3
import os
from pandas import read_csv, DataFrame, Series
from sklearn.preprocessing import LabelEncoder, Imputer
from sklearn.linear_model import LogisticRegression

movies = read_csv(os.path.join(os.path.abspath('.'), 'train.csv'))

test = read_csv(os.path.join(os.path.abspath('.'), 'test.csv'))
result = DataFrame(test.Id)
testresult = DataFrame(movies.Id, movies.Target)


""" Приводим к нужному виду обучающую выборку """

movies.Rating.fillna('Not Rated', inplace=True)
movies.Language.fillna('none', inplace=True)

"""Replacing string parameters with coresponding integer labels"""
label = LabelEncoder()
dicts = {}

label.fit(movies.Rating.drop_duplicates())
dicts["Rating"] = list(label.classes_)
movies.Rating = label.transform(movies.Rating)

label.fit(movies.Language.drop_duplicates())
dicts["Language"] = list(label.classes_)
movies.Language = label.transform(movies.Language)


label.fit(movies.Country.drop_duplicates())
dicts["Country"] = list(label.classes_)
movies.Country = label.transform(movies.Country)

"""Приводим к нужному виду финальную выборку"""
test.Rating.fillna('Not Rated', inplace=True)
test.Language.fillna('English', inplace=True)
test.Country.fillna('none', inplace=True)

label.fit(test.Rating.drop_duplicates())
dicts["Rating"] = list(label.classes_)
test.Rating = label.transform(test.Rating)

label.fit(test.Language.drop_duplicates())
dicts["Language"] = list(label.classes_)
test.Language = label.transform(test.Language)


label.fit(test.Country.drop_duplicates())
dicts["Country"] = list(label.classes_)
test.Country = label.transform(test.Country)

test = test.drop(['Poster', 'Id'], axis=1)

target = movies.Target
train = movies.drop(['Target', 'Poster', 'Id'], axis=1)

model_lr = LogisticRegression(penalty='l1', tol=0.01)


model_lr.fit(train, target)
result.insert(1, 'Probability', model_lr.predict_proba(test)[:, 1])
result.to_csv('prediction.csv', index=True, float_format='%.6f')
