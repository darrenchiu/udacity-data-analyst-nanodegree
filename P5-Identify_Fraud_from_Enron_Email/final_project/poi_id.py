#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from outliers_detector import outliers
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'salary', 'bonus', 'deferred_income', 'long_term_incentive',
                        'restricted_stock']  # You will need to use more features
features_list_without_poi = ['salary', 'bonus', 'deferred_income', 'long_term_incentive',
                             'restricted_stock']  # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
# Remove the record of "TOTAL"
del data_dict['TOTAL']

# Remove top and bottom 2% or records
print "features"
print features_list_without_poi
outliers = outliers(data_dict, features_list_without_poi)

for person in outliers:
    del data_dict[person]

### Task 3: Create new feature(s)
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

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
gaussian_clf = GaussianNB()

from sklearn import tree
tree_clf = tree.DecisionTreeClassifier(min_samples_split=10)

from sklearn.svm import SVC
svm_clf =  SVC(kernel = 'rbf', C=10000)

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

gaussian_clf.fit(features_train, labels_train)
print gaussian_clf.score(features_test, labels_test)

tree_clf.fit(features_train, labels_train)
print tree_clf.score(features_test, labels_test)

svm_clf.fit(features_train, labels_train)
print svm_clf.score(features_test, labels_test)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(gaussian_clf, my_dataset, features_list)
