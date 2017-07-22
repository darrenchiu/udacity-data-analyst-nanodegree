#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.svm import SVC
from sklearn import tree
import numpy as np
from sklearn.metrics import precision_score, recall_score
from sklearn import model_selection
from sklearn.naive_bayes import GaussianNB


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
sorted_features = [
    'total_stock_value',
    'exercised_stock_options',
    'deferred_income',
    'from_this_person_to_poi',
    'restricted_stock',
    'other',
    'long_term_incentive',
    'total_payments',
    'number_of_missing_fields',
    'salary',
    'bonus',
    'shared_receipt_with_poi',
    'expenses',
    'from_messages',
    'from_poi_to_this_person',
    'to_messages',
    'deferral_payments',
    'restricted_stock_deferred',
    'director_fees',
    'loan_advances'
]
features_list = ['poi'] + sorted_features[0:3]
features_list_without_poi = sorted_features[0:3]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
# Remove the record of "TOTAL"
del data_dict['TOTAL']
del data_dict['LOCKHART EUGENE E']
del data_dict['THE TRAVEL AGENCY IN THE PARK']
del data_dict['SKILLING JEFFREY K']
del data_dict['LAY KENNETH L']

### Task 3: Create new feature(s)
for person in data_dict.keys():
    data_dict[person]['number_of_missing_fields'] = sum(1 for x in data_dict[person].values() if x == 'NaN')

# convert the fields we want into numbers
for person in data_dict:
    for feature in features_list_without_poi:
        if data_dict[person][feature] == "NaN":
            data_dict[person][feature] = 0
        else:
            data_dict[person][feature] = float(data_dict[person][feature])

# feature scaling
for feature in features_list_without_poi:
    feature_max = max(x[feature] for x in data_dict.values())
    feature_min = min(x[feature] for x in data_dict.values())
    for person in data_dict:
        data_dict[person][feature] = (data_dict[person][feature] - feature_min) / (feature_max - feature_min)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# Build the clf
gaussian_clf = GaussianNB()
gaussian_clf.fit(features_train, labels_train)
print gaussian_clf.score(features_test, labels_test)
print precision_score(labels_test, gaussian_clf.predict(features_test), average='weighted')

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(gaussian_clf, my_dataset, features_list)
