This package is for computing feature importance in voting classifiers 

The steps of the algorithm to compute the feature importance of the Voting Classifier is:

Compute Feature Importance score of each of the base estimators
Multiply the weights of the base estimator to the importance score of each of the features.
Average out the features importance score (from step 2) for each feature.

The algorithm  takes the voting classifier and the weights as input and returns the feature importance as a pandas dataframe