#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from outliers_detector import outliers
from tester import dump_classifier_and_data
from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import precision_score
from sklearn import model_selection

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'from_this_person_to_poi', 'from_poi_to_this_person',
                 'shared_receipt_with_poi']  # You will need to use more features
features_list_without_poi = ['from_this_person_to_poi', 'from_poi_to_this_person',
                             'shared_receipt_with_poi']  # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
# Remove the record of "TOTAL"
del data_dict['TOTAL']

# Remove top and bottom 2% or records
outliers = outliers(data_dict, features_list_without_poi)

for person in outliers:
    del data_dict[person]

### Task 3: Create new feature(s)
for person in data_dict.keys():
    data_dict[person]['number_of_missing_fields'] = sum(1 for x in data_dict[person].values() if x == 'NaN')

# adding the new feature to the list
features_list.append('number_of_missing_fields')
features_list_without_poi.append('number_of_missing_fields')

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

# Tune the SVM
parameters = {'kernel': ('linear', 'poly', 'rbf', 'sigmoid'), 'C': np.arange(1000, 100000, 1000)}
svr = SVC()
clf = model_selection.GridSearchCV(svr, parameters, scoring='precision', n_jobs=2, verbose=5)
clf.fit(features_train, labels_train)
print clf.best_params_
print clf.best_score_

# Build the clf
svm_clf = SVC(kernel='rbf', C=21000)
svm_clf.fit(features_train, labels_train)
print svm_clf.score(features_test, labels_test)
print precision_score(labels_test, svm_clf.predict(features_test), average='weighted')

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(svm_clf, my_dataset, features_list)
