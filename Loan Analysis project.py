# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 20:54:57 2024

@author: eliza
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loan_data = pd.read_excel('loandataset.xlsx')
customer_data = pd.read_csv('customer_data.csv', sep=';')

#Display the first few rows of our dataset
print(loan_data.head())
print(customer_data.head())

#merging to dataframes on id
complete_data = pd.merge(loan_data, customer_data, left_on='customerid', right_on='id')

# Check for missing data
complete_data.isnull().sum()

#Remove the rows with missing data
complete_data = complete_data.dropna()
complete_data.isnull().sum()

#Check for duplicated data
complete_data.duplicated().sum()

#Dropping duplicates
complete_data = complete_data.drop_duplicates()

#Define a function to categorize purpose into broader categories

def categorize_purpose (purpose):
    if purpose in ['credit_card', 'debt_consolidation']:
        return 'Financial'
    elif purpose in ['educational', 'small_business']:
        return 'Educational?Business'
    else:
        return 'other'
categorize_purpose('credit_card')

complete_data['purpose_category']= complete_data['purpose'].apply(categorize_purpose)

# Create a new funtion based on criteria
# If the dti ratio is more than 20 and the delinq.2years is greater than 2 and the revol.uti>60 then the borrower

def assess_risk(row):
    if row ['dti']>20 and row['delinq.2yrs']>2 and row['revol.util']>60:
        return 'High Risk'
    else:
        return 'Low Risk'
    
    
complete_data['Risk'] = complete_data.apply(assess_risk, axis=1)

#Create a new function to categorize Fico score

def categorize_fico(fico_score):
    if fico_score>= 800 and fico_score<=850:
        return 'Excellent'
    elif fico_score>=740 and fico_score<800:
        return 'Very Good'
    elif fico_score>= 670 and fico_score<740:
        return 'Good'
    elif fico_score>= 580 and fico_score<670:
        return 'Fair'
    else:
        return 'Poor'

complete_data['fico_category'] = complete_data['fico'].apply(categorize_fico)

#Identify customers with more than average inquiries and derogatory records winth a funtion

def indetify_high_inq_derog(row):
    average_inq = complete_data['inq.last.6mths'].mean()
    average_derog = complete_data['pub.rec'].mean()
    
    if row['inq.last.6mths'] > average_inq and row['pub.rec']> average_derog:
        return True
    else:
        return False

complete_data['High_Inquries_and_Public_Records'] = complete_data.apply(indetify_high_inq_derog, axis=1)

#Data visualization
#Set the style of visualization (darkgrid, whitegrid, dark, white)
sns.set_style('darkgrid')

#Bar plot to show distibuition of loans by purpose
#seaborn palette = 'deep', 'pastel', 'dark', 'muted', 'bright', 'colorblind'

plt.figure(figsize=(10,6))
sns.countplot(x= 'purpose', data= complete_data, palette='dark')
plt.title('Loan Purpose Distribution')
plt.xlabel('Purpose of Loans')
plt.ylabel('Number of Loans')
plt.xticks(rotarion=45)
plt.show()

#Create a scatterplot for 'dit' vs 'Income'

plt.figure(figsize=(10,6))
sns.scatterplot(x = 'log.annual.inc', y = 'dti', data = complete_data)
plt.title('Debt-to-Income Ratio vs Annual Income')
plt.show()

#Distribuition of Fico scores
plt.figure(figsize=(10,6))
sns.histplot(complete_data['fico'], bins=30, kde=True)
plt.title('Distribuition of Fico Score')
plt.show()

#Box plot to determine risk vs interest rate
plt.figure(figsize=(10,6))
sns.boxplot(x  = 'Risk', y = 'int.rate', data = complete_data)
plt.title('Interest Rate vs Risk')
plt.show()

#Subplots

#Initialize the subplot figure
fig, axs = plt.subplots(2, 2, figsize=(20,20))

#1. Loan Purpose Distribuition
sns.countplot(x = 'purpose', data = complete_data, ax=axs[0,0])
axs[0,0].set_title('Loan Purpose Distribuition')
plt.setp(axs[0,0].xaxis.get_majorticklabels(), rotation=45)

#2. Debt_to-Income Ratio vs Fico Score
sns.scatterplot(x = 'fico', y = 'dti', data = complete_data, ax=axs[0,1])
axs[0,1].set_title('Debt-to-Income Ratio vs. Fico Score')

#3. Distribuition of Fico Scores
sns.histplot(complete_data['fico'],bins=30, kde=True, ax=axs[1,0])
axs[1,0].set_title('Distribuition of Fico Scores')

#4. Risk Category vs Interest Rate
sns.boxplot(x='Risk', y = 'int.rate', data = complete_data, ax=axs[1,1])
axs[1,1].set_title('Interest Rate vs. Risk Category')

#Adjust layout for readability
plt.tight_layout()
plt.show()
        




























