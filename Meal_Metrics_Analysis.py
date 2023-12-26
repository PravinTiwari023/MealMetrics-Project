import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define the scope
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('proven-yen-409211-2ee88f35110a.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open('mealmetrics_data').sheet1

# Get the data
data_ = sheet.get_all_records()

# Convert to DataFrame
data = pd.DataFrame(data_)

# Setting a diverse color palette for visualization
sns.set_palette("tab10")

# Creating different types of charts for various columns in the dataset
plt.figure(figsize=(15, 24))

# 1. Nutritional Value Consideration
plt.subplot(4, 2, 1)
sns.countplot(x='Nutritional Consideration', data=data)
plt.title('Nutritional Value Consideration')
plt.xticks(rotation=45)

# 2. Reading Food Labels for Nutritional Information
plt.subplot(4, 2, 2)
sns.countplot(x='Food Label Reading Habits', data=data)
plt.title('Reading Food Labels for Nutritional Information')
plt.xticks(rotation=45)

# 3. Meal Frequency
plt.subplot(4, 2, 3)
sns.countplot(x='Meal Frequency', data=data)
plt.title('Meal Frequency')
plt.xticks(rotation=45)

# 4. Diet Plan Following
plt.subplot(4, 2, 4)
sns.countplot(x='Dietary Preferences', data=data)
plt.title('Diet Plan Following')
plt.xticks(rotation=45)

# 5. Fruits and Vegetables in Diet
plt.subplot(4, 2, 5)
sns.countplot(x='Fruits and Vegetables Consumption', data=data)
plt.title('Fruits and Vegetables in Diet')
plt.xticks(rotation=45)

# 6. Whole Grains Consumption
plt.subplot(4, 2, 6)
sns.countplot(x='Whole Grains Consumption', data=data)
plt.title('Whole Grains Consumption')
plt.xticks(rotation=45)

# 7. Eating Out Frequency
plt.subplot(4, 2, 7)
sns.countplot(x='Eating Out Frequency', data=data)
plt.title('Eating Out Frequency')
plt.xticks(rotation=45)

# 8. Snacking Between Meals
plt.subplot(4, 2, 8)
sns.countplot(x='Snacking Habits', data=data)
plt.title('Snacking Between Meals')
plt.xticks(rotation=45)

plt.tight_layout()

# Since the "top priorities" column contains multiple choices, we need to preprocess this data
priorities_data = data['Food Selection Priorities'].str.get_dummies(sep=', ')
priorities_counts = priorities_data.sum().sort_values(ascending=False)

plt.figure(figsize=(12, 8))
priorities_counts.plot(kind='bar', color=sns.color_palette("tab10"))
plt.title('Top Priorities When Selecting Food')
plt.xlabel('Priorities')
plt.ylabel('Number of Responses')
plt.xticks(rotation=45)

# Creating a chart for the responses to "Are you currently taking any steps to improve your dietary habits?"
steps_to_improve_diet_counts = data['Steps to Improve Diet'].value_counts()

plt.figure(figsize=(8, 8))
steps_to_improve_diet_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette("tab10"))
plt.title('Steps to Improve Dietary Habits')
plt.ylabel('')

# Analyzing indicators of healthy habits
indicators = {
    "Nutritional Value Consideration": data['Nutritional Consideration'].isin(['Always', 'Often']).sum(),
    "Read Food Labels": data['Food Label Reading Habits'].isin(['Always', 'Often']).sum(),
    "Follow Diet Plan": data['Dietary Preferences'].ne('No specific diet').sum(),
    "High Fruits & Vegetables": data['Fruits and Vegetables Consumption'].isin(['51% - 75%', 'More than 75%']).sum(),
    "Frequent Whole Grains": data['Whole Grains Consumption'].isin(['Every meal', 'Most meals']).sum(),
    "Taking Steps to Improve Diet": data['Steps to Improve Diet'].eq('Yes').sum()
}

total_respondents = len(data)
healthy_choices_percentage = {key: (value / total_respondents * 100) for key, value in indicators.items()}

healthy_choices_df = pd.DataFrame(list(healthy_choices_percentage.items()), columns=['Indicator', 'Percentage'])

plt.figure(figsize=(10, 6))
sns.barplot(x='Percentage', y='Indicator', data=healthy_choices_df, palette="viridis")
plt.title('Percentage of Respondents Showing Healthier Choices')
plt.xlabel('Percentage of Respondents')
plt.ylabel('Health Indicators')
plt.xlim(0, 100)
plt.show()

# Gender-based analysis using Plotly
male_data = data[data['Gender'] == 'Male']
female_data = data[data['Gender'] == 'Female']

fig = make_subplots(
    rows=4, cols=2,
    subplot_titles=("Nutritional Value Consideration (Male)", "Nutritional Value Consideration (Female)",
                    "Meal Frequency (Male)", "Meal Frequency (Female)",
                    "Diet Plan Following (Male)", "Diet Plan Following (Female)",
                    "Fruits and Vegetables in Diet (Male)", "Fruits and Vegetables in Diet (Female)")
)

fig.add_trace(go.Bar(x=male_data['Nutritional Consideration'].value_counts().index,
                     y=male_data['Nutritional Consideration'].value_counts(),
                     name='Nutritional Value (Male)'), row=1, col=1)

fig.add_trace(go.Bar(x=female_data['Nutritional Consideration'].value_counts().index,
                     y=female_data['Nutritional Consideration'].value_counts(),
                     name='Nutritional Value (Female)'), row=1, col=2)

# ... (Add other traces following the same pattern for male and female data)

fig.update_layout(height=800, showlegend=False, title_text="MealMetrics: Gender-Based Analysis Dashboard")
fig.show()
