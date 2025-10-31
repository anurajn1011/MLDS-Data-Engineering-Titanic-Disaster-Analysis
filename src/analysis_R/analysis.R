# Load libraries
library(dplyr)
library(caret)
library(broom)

cat("------ Loading Training Data ------\n")
train_df <- read.csv("data/titanic/train.csv")

# ---------- CLEANING ----------
cat("------ Cleaning the Training Data ------\n")
cat("Pre-cleaned columns in training data:\n")
print(colnames(train_df))

# Fill missing Age and Embarked values
cat("Filling in nulls in 'Age' and 'Embarked'.\n")
train_df$Age[is.na(train_df$Age)] <- median(train_df$Age, na.rm = TRUE)
train_df$Embarked[is.na(train_df$Embarked)] <- names(sort(table(train_df$Embarked), decreasing = TRUE))[1]

# Drop unused columns
cat("Dropping columns 'Name', 'Cabin', and 'Ticket'.\n")
train_df <- train_df %>% select(-Name, -Cabin, -Ticket)
print(colnames(train_df))

# Convert categorical variables
cat("Converting categorical columns to factors.\n")
train_df <- train_df %>%
  mutate(
    Survived = factor(Survived),
    Pclass = factor(Pclass),
    Sex = factor(Sex),
    Embarked = factor(Embarked)
  )

features <- c("Age", "SibSp", "Parch", "Fare", "Pclass", "Sex", "Embarked")

cat("Number of empty entries: ", sum(is.na(train_df)), "\n")
cat("Shape of the training data: ", paste(dim(train_df), collapse = " x "), "\n")

# ---------- MODEL ----------
cat("------ Developing a Logistic Model ------\n")

features <- c("Age", "SibSp", "Parch", "Fare", "Pclass", "Sex", "Embarked")

# Build formula dynamically
formula <- as.formula(paste("Survived ~", paste(features, collapse = " + ")))

# Train logistic regression model
cat("Fitting logistic regression model...\n")
model <- suppressWarnings(
  train(formula, data = train_df, method = "glm", family = "binomial")
)

cat("Model training complete.\n")

# Extract and print coefficients + intercept
cat("Intercept and Coefficients:\n")
coefs <- tidy(model$finalModel)
print(coefs)

# Predict on training set
cat("Testing our model on training set...\n")
pred_train <- predict(model, train_df)
acc_train <- mean(pred_train == train_df$Survived)
cat("Accuracy on training data: ", acc_train, "\n")

# ---------- TEST DATA ----------
cat("------ Predicting on Test Data ------\n")
test_df <- read.csv("data/titanic/test.csv")

cat("Columns in testing data prior to cleaning:\n")
print(colnames(test_df))

# Fill missing data
test_df$Age[is.na(test_df$Age)] <- median(test_df$Age, na.rm = TRUE)
test_df$Fare[is.na(test_df$Fare)] <- median(test_df$Fare, na.rm = TRUE)
test_df$Embarked[is.na(test_df$Embarked)] <- names(sort(table(test_df$Embarked), decreasing = TRUE))[1]

# Drop unused columns
test_df <- test_df %>% select(-Name, -Cabin, -Ticket)
cat("Dropped unused columns.\n")

cat("Columns in testing data following cleaning:\n")
print(colnames(test_df))
cat("Number of empty entries: ", sum(is.na(test_df)), "\n")
cat("Shape of the testing data: ", paste(dim(test_df), collapse = " x "), "\n")

# Convert to factors matching training
test_df <- test_df %>%
  mutate(
    Pclass = factor(Pclass, levels = levels(train_df$Pclass)),
    Sex = factor(Sex, levels = levels(train_df$Sex)),
    Embarked = factor(Embarked, levels = levels(train_df$Embarked))
  )

# Predict
cat("Predicting on test data...\n")
pred_test <- predict(model, test_df)
cat("Predicted!\n")

# Evaluate accuracy against gender_submission.csv
Y_test_true <- read.csv("data/titanic/gender_submission.csv")
Y_test_true$Survived <- factor(Y_test_true$Survived, levels = levels(train_df$Survived))

acc_test <- mean(pred_test == Y_test_true$Survived)
cat("Accuracy on predicting test data: ", acc_test, "\n")
