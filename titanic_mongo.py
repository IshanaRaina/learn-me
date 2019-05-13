from pymongo import MongoClient

##########################
#Establishing a connection 
##########################
client = MongoClient() #connects to localhost by default
db = client["test"]

################################
#Verifying connection to MongoDB
################################
print("Total number of documents in the 'titanic' collection: ", db.titanic.count_documents({}))
print(db.titanic.find_one())

##########
#Filtering
##########
print("\n----------------Filtering--------------------")

#The most compelling question when it comes to Titanic - How many survivors?
print(db.titanic.count_documents({"survived":1}))
print(db.titanic.count_documents({"age":{"$lt":18}}))

print(db.titanic.count_documents({"$and":[{"survived":1}, {"age":{"$lt":18}}]}))

print(db.titanic.count_documents({"name":{"$regex":"Mrs"}}))

#Unlike relational databases, presence isn't compulsory in MongoDB. 
#There's a filter to check for presence.
#Do all passengers have a ticket_number?
print(db.titanic.count_documents({"ticket_number":{"$exists":False}}))

################
#Distinct values
################
print("\n--------------Distinct Values----------------")

print(db.titanic.distinct("point_of_embarkation"))
print(db.titanic.distinct("class", {"fare_paid":0}))

############
#Projections
############
print("\n----------------Projections------------------")

#Counting documents is straightforward but on using the find() method, a cursor is returned.
print(db.titanic.find({"parents_children":{"$gte":5}}))

#We can send the cursor over to a list and slice the list to limit the results
print(list(db.titanic.find({"parents_children":{"$gte":5}}))[:3])

#This cursor can also be iterated over using a loop
from pprint import pprint
for doc in db.titanic.find({"parents_children":{"$gte":5}}):
    pprint(doc)

#How do we limit the fields that we see in the results?
for doc in db.titanic.find({"parents_children":{"$gte":5}}, {"name":1, "age":1, "_id":0}):
    print(doc)

#If we aren't excluding any fields in our projections, pymongo accepts another simpler format.
for doc in db.titanic.find({"parents_children":{"$gte":5}}, ["name", "age"]):
    print(doc)

#Writing the above code in a single line using list comprehension
[print(doc) for doc in db.titanic.find({"parents_children":{"$gte":5}}, ["name", "age"])]

#Python's use in dealing with iterables like cursors and MongoDB's projection can be used to
#slim down the documents returned. Togther, they make for powerful querying!

########
#Sorting
########
print("\n----------------Sorting------------------")
for doc in db.titanic.find({"age":{"$lt":18}}, sort = [("class", 1)]):
    print(doc["class"], doc["survived"])

for doc in db.titanic.find({"age":{"$lt":18}}, sort = [("class", 1), ("gender", 1)]):
    print(doc["class"], doc["gender"], doc["survived"])
    
#Sorting in the Mongo shell is slightly different. Instead of tuples, they have to be entered 
#as key-value pairs. Eg: {"class":1, "gender":1}    

######################
#Limiting and Skipping  
######################
print("\n------------Limiting & Skipping---------------")

for doc in db.titanic.find({"parents_children":{"$gte":5}}, skip = 3, limit = 3):
    print("{name}: {survived}".format(**doc))

#####################
#Aggregation Pipeline
#####################
print("\n------------Aggregation Pipeline---------------")

print(db.titanic.count_documents({"age":{"$gte":70}}))

from collections import OrderedDict
cursor = db.titanic.aggregate([ \
    {"$match":{"age":{"$gte":70}}}, \
    {"$project":{"class":1, "gender":1, "survived":1}}, \
    {"$sort":OrderedDict([("class", 1), ("gender", 1)])}, \
    {"$limit":5}])
for doc in cursor:
    print(doc["class"], doc["gender"], doc["survived"])

################################
#Importing data into a dataframe
################################
print("\n------------Importing into DataFrame---------------")

import pandas as pd
df = pd.DataFrame(list(db.titanic.find()))
print(df.info())
print(df.head())
#In a dataframe, blank/missing values are automatically assigned NaN. But empty strings can exist
#which would need to be replaced
assert df.iloc[1,2] == "" #asserting that an empty string exists
import numpy as np
df = df.replace("",np.nan)
print(df.info())
print(df.head())

###################
#Data visualization
###################
print("\n-------------Data visualization--------------")

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='darkgrid')
sns.catplot('class', 'survived', data=df, kind='point', hue='gender')
#sns.lmplot('age', 'survived', data=df)
#df.plot(x='age', y='class', kind='scatter')
plt.title('Titanic Survivors')
plt.show()

# # Display the box plots on 3 separate rows and 1 column
# fig, axes = plt.subplots(nrows=3, ncols=1)

# # Generate a box plot of the fare prices for the First passenger class
# titanic.loc[titanic['pclass'] == 1].plot(ax=axes[0], y='fare', kind='box')

# # Generate a box plot of the fare prices for the Second passenger class
# titanic.loc[titanic['pclass'] == 2].plot(ax=axes[1], y='fare', kind='box')

# # Generate a box plot of the fare prices for the Third passenger class
# titanic.loc[titanic['pclass'] == 3].plot(ax=axes[2], y='fare', kind='box')

# # Display the plot
# plt.show()
