# "Healthy"
 Predicting individual heart rate values per activity, personal physiology and measurements using 
 a mixed effect (fixed slope, varying intercept) multiple linear regression machine learning model.
 Built using Pandas on Python and R (some R libraries used are written in C and C++).
 Dataset is taken from the "Multilevel Monitoring of Activity and Sleep in Healthy People" 
 by Alessio Rossi et al. PhysioNet, June 19 2020.
 https://doi.org/10.13026/cerq-fc86
 
As of now the model is fully operational, with several validation methods included: regular split, stratified split and stratified k-fold cross validation.
Step-wise feature selection is used to find the best subset of variables for the model (one-hot encoded).
A final simple t-test implementation is used to distinguish irregular heart rate measurements per individual, potentially to alert the user or a practitioner, 
as part of a tele-medicine service or perhaps an application on a smart wearable device.
