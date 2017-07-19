import numpy as np
import pandas as pd


def outliers(data_dict, features):
    # convert into pandas dataframe
    df = pd.DataFrame(data_dict.values())
    df.drop('email_address', axis=1, inplace=True)
    for col in features:
        df[col] = df[col].astype('float64')

    # search for outliers
    person_with_extreme_value = set([])
    print(features)
    for feature in features:
        upper = np.percentile(df[feature].dropna(), 98)
        lower = np.percentile(df[feature].dropna(), 2)

        for person in data_dict.keys():
            if data_dict[person][feature] != 'NaN':
                if data_dict[person][feature] >= upper or data_dict[person][feature] <= lower:
                    person_with_extreme_value.add(person)

    return person_with_extreme_value
    # print person_with_extreme_value
    # print len(person_with_extreme_value)
