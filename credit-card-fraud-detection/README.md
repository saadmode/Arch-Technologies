# Credit Card Fraud Detection Using Python

## Overview

I worked on this project as part of my cybersecurity internship at Arch Technologies to gain practical exposure to fraud detection and machine learning using Python.

The purpose of this project is to read credit card transaction records, build useful features from them, and predict which transactions are fraudulent. I compared one supervised model, which learns from labelled fraud examples, with three anomaly-detection methods that only look for unusual transactions.

Fraud is very rare in this dataset (about 0.4% to 0.6% of transactions), so accuracy is a misleading measure. Every model is judged using precision, recall, F1-score and PR-AUC for the fraud class.

## Project Setup

* Python 3.11
* pandas and numpy
* scikit-learn
* Windows 10
* Visual Studio Code with Jupyter notebooks

## Dataset

Kaggle: **Credit Card Fraud Detection** (kaushalnandania)

| File | Rows | Columns |
|------|------|---------|
| `train.csv` | 1,296,675 | 23 |
| `test.csv` | 555,719 | 23 |

The label column is `is_fraud`. The data is synthetic, so results should not be treated as real-world performance.

The CSV files are too large to upload to GitHub, so they are not included in this repository. Download them from Kaggle and place them in the project folder.

## Features

The notebook provides the following:

* Loads the training and test files and checks their shape, columns and data types
* Builds features: hour, day of week, customer age, amount, log of the amount, gender flag, city population and the distance in kilometres between the customer and the merchant
* One-hot encodes the merchant category
* Removes identifier columns (row index, card number, transaction number, names, street, city, zip, job, merchant and unix time) so models learn behaviour and not identities
* Trains a Gradient Boosting classifier with balanced class weights
* Trains three anomaly detectors: Isolation Forest, Local Outlier Factor and One-Class SVM
* Scales the features using statistics from the training data only
* Evaluates every model on the separate `test.csv` using fraud-class precision, recall, F1-score and PR-AUC

## Files in This Project

| File | Purpose |
|------|---------|
| `main.ipynb` | Loads the data, builds features, trains all four models and prints the results |

## Activity Performed

During this project, I worked with Python to:

* Download and inspect a credit card transaction dataset
* Turn raw columns into model features
* Train a supervised model and three anomaly detectors
* Evaluate all models on unseen test data
* Compare supervised learning with anomaly detection
* Fix problems found during development, such as missing libraries, a wrong dataset assumption, a coding error in the sampling step, misleading accuracy, missing feature scaling, identifier columns and training and testing on the same data

## How to Run

### 1. Prepare

Install Python 3 and the required libraries:

```bash
python -m pip install pandas numpy scikit-learn
```

Place `train.csv` and `test.csv` in the project folder and set the folder path in the first cell of `main.ipynb`:

```python
folder = r'E:\path\to\Credit Card Fraud Detection'
```

### 2. Run the Notebook

Open `main.ipynb` in Visual Studio Code, select the Python 3.11 kernel and choose **Run All**.

The One-Class SVM and Local Outlier Factor steps can take several minutes. If they are too slow, reduce the training subsample from 20,000 to 10,000 rows.

## Results

All models were trained on `train.csv` and scored on `test.csv`. The values below are for the fraud class.

| Model | Precision | Recall | F1-score | PR-AUC |
|-------|-----------|--------|----------|--------|
| Gradient Boosting (supervised) | 0.159 | 0.972 | 0.273 | 0.8609 |
| Isolation Forest | 0.154 | 0.281 | 0.199 | 0.534 |


Gradient Boosting was scored on all 555,719 test transactions. The anomaly detectors were scored on a random sample of 100,000 test transactions to save time.

### Observations

* The supervised Gradient Boosting model was clearly the best, with a PR-AUC of 0.8609 and a fraud recall of 97.2%.
* Its precision at the default threshold is only 15.9%, which means many false alarms. Tuning the threshold on a validation split would improve this.
* The anomaly detectors performed far worse. Fraud follows specific patterns, while anomaly detectors only look for unusual transactions.
* The fraud rate differs between the files (0.579% in train and 0.386% in test).

## What I Learned

This project helped me understand why accuracy is misleading on highly imbalanced data and how to evaluate models with precision, recall and PR-AUC instead.

I also gained exposure to feature engineering from dates, coordinates and categories, data leakage, and the difference between supervised learning and anomaly detection.

## Skills Practiced

* Python
* Machine Learning
* Fraud Detection Basics
* Feature Engineering
* Handling Imbalanced Data
* Model Evaluation
* Testing and Debugging

## Limitations

The dataset is synthetic, so real-world fraud will be messier and results may not carry over.

Only one train and test split was evaluated, and the decision threshold was left at its default value. The anomaly detectors were trained on a subsample, so their figures are less precise. No customer-history features, such as the number of transactions per card in the last hour, were built.

## Disclaimer

This project is for learning purposes and is not a production fraud-detection system. Use it only on data you own or have permission to analyse. Real transaction data contains private information and should be handled carefully.

## Project Evidence

Screenshots of the notebook output and a demonstration video can be added to document the models running and their results.
