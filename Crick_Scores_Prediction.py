import pandas as pd 
import numpy as np
import pickle
# loading the dataset

df = pd.read_csv("ipl.csv")

## Data Cleaning
## Removing unwanted columns

columns_to_remove = ['mid', 'venue', 'batsman', 'bowler', 'striker', 'non-striker']
df.drop(labels=columns_to_remove,axis=1,inplace=True)

# Removing unwanted teams

df['bat_team'].unique()
teams_we_want = ['Kolkata Knight Riders', 'Chennai Super Kings', 
                'Rajasthan Royals','Mumbai Indians','Kings XI Punjab',
                'Royal Challengers Bangalore', 'Delhi Daredevils','Sunrisers Hyderabad']

df = df[(df['bat_team'].isin(teams_we_want)) & (df['bowl_team'].isin(teams_we_want))]


df['bat_team'].unique()
# Removing first 5 overs data in the matches


df = df[df['overs']>=5.0]




# Converting the column 'date' from string into datetime object
from datetime import datetime
df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y'))




## Data Preprocessing
encoded_df = pd.get_dummies(data=df,columns=['bat_team','bowl_team'])
encoded_df.columns
encoded_df.head()
# Rearranging the columns

encoded_df = encoded_df[['date', 'bat_team_Chennai Super Kings', 'bat_team_Delhi Daredevils', 'bat_team_Kings XI Punjab',
              'bat_team_Kolkata Knight Riders', 'bat_team_Mumbai Indians', 'bat_team_Rajasthan Royals',
              'bat_team_Royal Challengers Bangalore', 'bat_team_Sunrisers Hyderabad',
              'bowl_team_Chennai Super Kings', 'bowl_team_Delhi Daredevils', 'bowl_team_Kings XI Punjab',
              'bowl_team_Kolkata Knight Riders', 'bowl_team_Mumbai Indians', 'bowl_team_Rajasthan Royals',
              'bowl_team_Royal Challengers Bangalore', 'bowl_team_Sunrisers Hyderabad',
              'overs', 'runs', 'wickets', 'runs_last_5', 'wickets_last_5', 'total']]
# Train-Test Splitting

X_train =  encoded_df.drop(labels='total',axis=1)[encoded_df['date'].dt.year <=2016]
X_test =  encoded_df.drop(labels='total',axis=1)[encoded_df['date'].dt.year >=2017]

y_train = encoded_df[encoded_df['date'].dt.year <= 2016]['total'].values
y_test = encoded_df[encoded_df['date'].dt.year >= 2017]['total'].values

# Removing the 'date' column
X_train.drop(labels='date', axis=True, inplace=True)
X_test.drop(labels='date', axis=True, inplace=True)


## Model Building
# Linear Regression

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train,y_train)

#Creating a pickle file
filename = 'Crick_Score_Prediction.pkl'
pickle.dump(model,open(filename,'wb'))