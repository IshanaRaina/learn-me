#! python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

xl = pd.ExcelFile("Insurance.xlsx")
df = xl.parse(1)
print("The shape of the insurance data frame is: ", df.shape)
print(df.info())

plt.figure(num = 1, figsize = (8,6)) # Num argument allows multiple plots to be displayed with a single plt.show() 
sns.set(style="darkgrid")
ax = sns.countplot(df["Location Code & Description"], 
    order = df["Location Code & Description"].value_counts().iloc[:10].index)

# Rotate x labels to avoid overlapping with each other
ax.set_xticklabels(ax.get_xticklabels(), rotation=70, ha="right")

# Adding data labels
for p in ax.patches: #looping through all bars of the bar plot since ax.patches outputs a list of rectangle objects
    ax.text(p.get_x() + p.get_width()/2, p.get_height(), '%d' % int(p.get_height()), 
            fontsize=12, color='black', ha='center')

plt.title('Top 10 Claims by Location')
plt.tight_layout()

plt.figure(num = 2, figsize = (10,8))
sns.set(style="darkgrid")
ax = sns.countplot(df["Type of Claim"], order = df["Type of Claim"].value_counts().iloc[:10].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=75, ha="right")
for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2, p.get_height(), '%d' % int(p.get_height()), 
            fontsize=12, color='black', ha='center')
plt.title('Top 10 Claims by Cause')
plt.tight_layout()

plt.show()
