import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

train_df = pd.read_csv("data/titanic/train.csv")

""" CLEANING """

# age, cabin, and embarked have empty entries
print("------ Cleaning the Training Data ------")
print("Pre-cleaned columns in training data")
print(train_df.columns.to_list())
# for age, we will fill it in with the median
print("Filling in nulls in 'Age' and 'Embarked.")
train_df["Age"] = train_df["Age"].fillna(train_df["Age"].median())

# fill in Embarked with the mode
train_df["Embarked"] = train_df["Embarked"].fillna(train_df["Embarked"].mode()[0])

# drop the name, ticker, and cabin column since that won't have any relation to predicting survivability
train_df = train_df.drop(columns=["Name", "Cabin", "Ticket"])
print("Dropped columns 'Name', 'Cabin' and 'Ticket':")
print(train_df.columns.to_list())
# convert categorical variables like Survived, Pclass, Sex, and Embarked as Dummy Variables
train_df = pd.get_dummies(train_df, columns=["Survived", "Pclass", "Sex", "Embarked"])
print("Converted categorical columns in training set to factors.")
print(train_df.columns.to_list())

# checking nulls and shape
print(f"Number of empty entries in the dataframe: {train_df.isnull().any().sum()}")
print("The shape of the training data: ", train_df.shape)

""" EXPLORATION """
print("------ Exploring the Training Data ------")
print("We have checked the numeric values for correlations previously.")
# check the correlation matrix
# print(train_df.corr(numeric_only=True))
# we do not notice any high correlations between the variables

""" MODEL """
print("------ Developing a Logistic Model ------")

print("Extracted the features.")
features = ["Age", "SibSp", "Parch", "Fare", 'Pclass_1', 'Pclass_2', 'Pclass_3',
                    'Sex_female', 'Sex_male', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
model = LogisticRegression()
print("Scaling the predictors for the training model.")
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(train_df[features]), columns=features)
print("First three rows of scaled predictors: \n", X_scaled.head(3))
print("Fitting the model: ")
model.fit(X_scaled, train_df['Survived_1'])
print("Intercept: ", model.intercept_)
print("Coefficients: ", model.coef_)

# predict on the train test
Y_pred_train = model.predict(train_df[features])
score = model.score(X_scaled, train_df["Survived_1"])
print("Tested our model on our training set.")
print(f"Score recevied after testing: {score}")

# --- predict on the test set --- #

print("------ Predicting on Test Data ------")
test_df = pd.read_csv("data/titanic/test.csv")

print("The columns in the testing data prior to cleaning for prediction: ", test_df.columns.to_list())

# Fill missing values instead of dropping
test_df["Age"] = test_df["Age"].fillna(test_df["Age"].median())
test_df["Fare"] = test_df["Fare"].fillna(test_df["Fare"].median())
test_df["Embarked"] = test_df["Embarked"].fillna(test_df["Embarked"].mode()[0])
test_df = test_df.drop(columns=["Name", "Cabin", "Ticket"])

print(f"Number of empty entries in the dataframe: {test_df.isnull().any().sum()}")
print("The shape of the testing data: ", test_df.shape)
print("The columns in the testing data prior to cleaning for prediction: ", test_df.columns.to_list())

# converting test_df categorical cols to factors and verifying
test_df = pd.get_dummies(test_df, columns=["Pclass", "Sex", "Embarked"])
print("Converting test category columns to factors.")

# capturing predictions
print("Predicting on the test set... ")
Y_pred_test = model.predict(test_df[features])
print("Predicted!")

# scaling the inputs for the test
print("Scaling the predictors in the test data.")
scaler_test = StandardScaler()
X_scaled_test = pd.DataFrame(scaler.fit_transform(test_df[features]), columns=features)
print("First three rows of scaled predictors: \n", X_scaled_test.head(3))

# checking our model
Y_test_true = pd.read_csv("data/titanic/gender_submission.csv") 
Y_test_true = pd.get_dummies(Y_test_true, columns=["Survived"])
score = model.score(X_scaled_test, Y_test_true["Survived_1"])
print("Testing our model on our testing set.")
print(f"Score recevied after testing on training set: {score}")