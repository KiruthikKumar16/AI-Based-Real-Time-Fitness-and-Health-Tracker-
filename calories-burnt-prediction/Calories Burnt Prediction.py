#!/usr/bin/env python
# coding: utf-8

# # Importing the Dependencies

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics


# #Data Collection & Preprocessing

# In[4]:


#laoding the data from csv file to a Pandas DataFrame
calories = pd.read_csv('calories.csv')

# Kaggle Dataset Integration and Processing Pipeline
# In[5]:


# print first five rows of the dataframe
calories.head()


# In[7]:


exercise_data = pd.read_csv('exercise.csv')


# In[8]:


exercise_data.head()


# #combining the two dataframes
# 

# In[9]:


calories_data = pd.concat([exercise_data , calories['Calories']],axis=1)


# In[10]:


calories_data.head()


# In[11]:


#checking the number of rows and column
calories_data.shape


# In[12]:


#getting some information about the data
calories_data.info()


# In[13]:


calories_data.isnull().sum()


# #Data Analysis

# In[14]:


#get some statistical about the data
calories_data.describe()


# #Data Visualization

# In[15]:


sns.set()


# In[18]:


#plotting the gender column in count plot
sns.countplot(calories_data['Gender'])


# In[19]:


#finding the distribution of "Age" column
sns.distplot(calories_data['Age'])


# In[20]:


#finding the distribution of "Height" Column
sns.distplot(calories_data['Height'])


# In[21]:


#finding the distribution of "Weight" Column
sns.distplot(calories_data['Weight'])


# #Finding the correlation in the dataset
# 
# Positive correlation
# Negative correlation

# In[32]:


correlation = calories_data.drop(columns=['Gender']).corr()


# In[53]:

# Interactive Fitness Analytics Dashboard
#constructing a heatmap to understand the correlation
# Advanced Machine Learning for Fitness Analytics
plt.figure(figsize=(10, 10))
sns.heatmap(correlation, cbar=True, square=True, fmt='.1f', annot=True, annot_kws={'size': 8}, cmap='Blues')


# #Converting the text data to numerical values

# In[35]:


calories_data.replace({"Gender":{'male':0,'female':1}},inplace=True)


# In[36]:


calories_data.head()


# #Separating features and Target

# In[39]:


X = calories_data.drop(columns=['User_ID','Calories'],axis=1)
Y = calories_data['Calories']


# In[40]:


print(X)


# #Splitting the data into training and Test data
# 

# In[41]:


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=2)


# In[42]:


print(X.shape,X_train.shape,X_test.shape)


# #Model Training

# In[43]:


#loading the model
model = XGBRegressor()


# In[44]:


#training the model with X_train
model.fit(X_train,Y_train)


# #Evaluation
# Real-Time Calorie Prediction System
# Prediction on Test Data

# In[45]:


test_data_prediction = model.predict(X_test)


# In[46]:


print(test_data_prediction)


# Mean Absolute Error

# In[50]:


mae = metrics.mean_absolute_error(Y_test,test_data_prediction)


# In[51]:


print("Mean Asolute Error = ",mae)


# #Predictive System

# In[ ]:




