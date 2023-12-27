import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_echarts import st_echarts

# Set the page layout to wide
st.set_page_config(layout="wide")

# Load or preprocess your data here
# For example, you can load a CSV file into a pandas DataFrame
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('proven-yen-409211-2ee88f35110a.json', scope)

# Authorize the clientsheet
client = gspread.authorize(creds)

# Open the spreadhseet
sheet = client.open('mealmetrics_data').sheet1

# Get the data
data_ = sheet.get_all_records()

# Convert to DataFrame
data = pd.DataFrame(data_)

# Add on_change callback
def on_change(key):
    selection = st.session_state[key]

selected_page = option_menu(None, ["Home", "Dashboard", "About Us", 'Contact Us'],
                            icons=['house', 'list-task', "info-circle", 'envelope'],
                            on_change=on_change, key='menu', orientation="horizontal",
                            styles={
                                "container": {"padding": "5px", "background-color": "#f0f0f0", "border-radius": "8px"},
                                "icon": {"color": "#606060", "font-size": "20px"},
                                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "color": "#505050"},  # Reduced font size
                                "nav-link-selected": {"background-color": "#E6E6FA", "color": "black"},
                            })


# Page layouts
if selected_page == 'Home':
    st.title('Welcome to MealMetrics!')

    # Banner Image
    # st.image('homepage_banner.jpg', use_column_width=True)

    # Introduction and Description
    st.markdown("""
    ## 🥗 MealMetrics: Your Dietary Insight Tool
    MealMetrics is a webapp designed to analyze and visualize dietary habits based on user-submitted data. 
    The data is collected from various sources and is used to provide insights into dietary patterns, preferences, and nutrition considerations.

    - **Data Collection:** Through online surveys focusing on dietary habits, meal frequency, nutritional considerations, and more.
    - **Purpose:** To help users understand eating habits and make informed decisions about their diet and nutrition.
    - **Data Description:** Metrics like meal frequency, dietary preferences, nutritional value, etc., from diverse individuals.
    """)

    # Interactive Data Preview Section
    st.subheader('🔍 Preview of Collected Data')
    # Load and display a snippet of the data
    # Assuming 'data' is your DataFrame
    data_to_display = data.drop(data.columns[[0, 1]], axis=1)  # Dropping the first two columns
    st.dataframe(data_to_display)  # Display the modified DataFrame

    # Detailed Data Description
    st.markdown("""
    ### 📊 Detailed Data Description

    - **Gender:** The gender of the respondent.
    - **Dietary Preferences:** Choices like vegetarian, vegan, keto, etc.
    - **Meal Frequency:** Number of meals eaten in a day.
    - **Nutritional Consideration:** Focus on nutritional info when choosing food.
    - **Fruits and Vegetables Consumption:** Frequency of consumption.
    - **Whole Grains Consumption:** Inclusion of whole grains in meals.
    - **Snacking Habits:** Information about snacking between meals.
    - **Eating Out Frequency:** How often eating out occurs weekly.
    - **Food Label Reading Habits:** Regular reading of food labels for nutrition.
    - **Steps to Improve Diet:** Actions taken to improve diet.
    - **Health Consciousness:** Measure of diet-related health awareness.
    - **Food Selection Priorities:** Factors prioritized in food selection (taste, cost, health benefits).

    This data helps create interactive visualizations for insights into dietary habits.
    """)

    # Visual Element: Interactive Charts or Graphs
    st.subheader('📈 Interactive Diet Insights')
    # Example: Display an interactive chart based on the data
    # st.plotly_chart(some_plotly_chart_based_on_data)

    # Footer
    st.markdown("---")
    st.markdown("© 2023 MealMetrics - Unveiling Dietary Patterns")

if selected_page == 'Dashboard':
    st.title('📊 Dashboard')
    st.markdown('''
        This dashboard presents a visual analysis of dietary habits, offering insights into the balance between healthy and junk food choices.
        ''')

    # Banner Image for Dashboard
    # st.image('dashboard_banner.jpg', use_column_width=True)

    # Sunburst Chart for Healthy vs Junk Food
    st.subheader('🍏 Healthy Food vs Junk Food 🍔')
    st.markdown('Explore the comparative overview of healthy and junk food items:')

    # Example data structure for healthy and junk foods
    food_data = [
        {
            "name": "Healthy Food",
            "children": [
                {
                    "name": "Fruits",
                    "children": [
                        {"name": "Mango", "value": 5},
                        {"name": "Papaya", "value": 5},
                        {"name": "Guava", "value": 5},
                        # Add more fruits as needed
                    ],
                },
                {
                    "name": "Vegetables",
                    "children": [
                        {"name": "Spinach", "value": 5},
                        {"name": "Okra", "value": 5},
                        {"name": "Eggplant", "value": 5},
                        # Add more vegetables as needed
                    ],
                },
                {
                    "name": "Whole Grains",
                    "children": [
                        {"name": "Chapati", "value": 5},
                        {"name": "Brown Rice", "value": 5},
                        {"name": "Millet", "value": 5},
                        # Add more whole grains as needed
                    ],
                },
                # Add more healthy food categories as needed
            ],
        },
        {
            "name": "Junk Food",
            "children": [
                {
                    "name": "Fast Food",
                    "children": [
                        {"name": "Samosa", "value": 5},
                        {"name": "Vada Pav", "value": 5},
                        {"name": "Pani Puri", "value": 5},
                        # Add more fast food items as needed
                    ],
                },
                {
                    "name": "Sugary Snacks",
                    "children": [
                        {"name": "Jalebi", "value": 5},
                        {"name": "Gulab Jamun", "value": 5},
                        {"name": "Rasgulla", "value": 5},
                        # Add more sugary snacks as needed
                    ],
                },
                {
                    "name": "Fried Foods",
                    "children": [
                        {"name": "Pakora", "value": 5},
                        {"name": "Bhatura", "value": 5},
                        {"name": "Poori", "value": 5},
                        # Add more fried foods as needed
                    ],
                },
                # Add more junk food categories as needed
            ],
        },
    ]

    # The sunburst chart option
    option = {
        "title": {
            "text": "Healthy Food vs Junk Food",
            "subtext": "A Comparative Overview",
            "textStyle": {"fontSize": 14, "align": "center"},
            "subtextStyle": {"align": "center"},
        },
        "series": {
            "type": "sunburst",
            "data": food_data,
            "radius": [0, "95%"],
            "sort": None,
            "emphasis": {"focus": "ancestor"},
            "levels": [
                {},
                {
                    "r0": "15%",
                    "r": "35%",
                    "itemStyle": {"borderWidth": 2},
                    "label": {"rotate": "tangential"},
                },
                {"r0": "35%", "r": "70%", "label": {"align": "right"}},
                {
                    "r0": "70%",
                    "r": "72%",
                    "label": {"position": "outside", "padding": 3, "silent": False},
                    "itemStyle": {"borderWidth": 3},
                },
            ],
        },
    }

    # Render the sunburst chart in full width
    st_echarts(option, height="700px", key="sunburst")

    # Adding a Divider
    st.markdown('---')

    # Creating three columns for additional visualizations
    st.subheader('🔍 In-Depth Dietary Analysis')

    # Creating three columns for the visualizations
    col1, col2, col3 = st.columns(3)

    # Visualization 1: Nutritional Value Consideration
    with col1:
        st.write('Nutritional Value Consideration')
        fig, ax = plt.subplots()
        sns.countplot(x='Nutritional Consideration', data=data, palette='viridis')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Visualization 1: Meal Frequency
        st.write('Dietary Preferences')
        fig, ax = plt.subplots()
        sns.countplot(x='Dietary Preferences', data=data, palette='tab10')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Visualization 1: Meal Frequency
        st.write('Eating Out Frequency')
        fig, ax = plt.subplots()
        sns.countplot(x='Eating Out Frequency', data=data, palette='viridis')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Visualization 2: Food Label Reading Habits
    with col2:
        st.write('Food Label Reading Habits')
        fig, ax = plt.subplots()
        sns.countplot(x='Food Label Reading Habits', data=data, palette='tab10')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Visualization 1: Meal Frequency
        st.write('Fruits and Vegetables Consumption')
        fig, ax = plt.subplots()
        sns.countplot(x='Fruits and Vegetables Consumption', data=data, palette='viridis')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Visualization 1: Meal Frequency
        st.write('Snacking Habits')
        fig, ax = plt.subplots()
        sns.countplot(x='Snacking Habits', data=data, palette='tab10')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Visualization 3: Meal Frequency
    with col3:
        st.write('Meal Frequency')
        fig, ax = plt.subplots()
        sns.countplot(x='Meal Frequency', data=data, palette='viridis')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Visualization 1: Meal Frequency
        st.write('Whole Grains Consumption')
        fig, ax = plt.subplots()
        sns.countplot(x='Whole Grains Consumption', data=data, palette='tab10')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Visualization 1: Meal Frequency
        st.write('Food Preference')
        fig, ax = plt.subplots()
        sns.countplot(x='Food Preference', data=data, palette='viridis')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Adding a Divider
    st.markdown('---')

    # Health Consciousness and Food Selection Priorities Analysis
    st.subheader('📈 Health Consciousness & Food Selection Priorities')

    # Calculate category frequencies for 'Health Consciousness'
    category_counts_health = data['Health Consciousness'].value_counts().reset_index()
    category_counts_health.columns = ['Category', 'Count']
    xAxis_data_health = category_counts_health['Category'].tolist()
    series_data_health = [{"value": count, "name": category} for category, count in
                          zip(xAxis_data_health, category_counts_health['Count'])]

    # Options for 'Health Consciousness' bar chart
    options_health = {
        "title": {"text": "Health Consciousness Analysis", "subtext": "Distribution of Health Consciousness Responses",
                  "left": "center"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {"type": "category", "data": xAxis_data_health, "axisLabel": {"rotate": 25, "interval": 0}},
        "yAxis": {"type": "value"},
        "series": [{"data": series_data_health, "type": "bar"}],
    }

    # Processing the 'Food Selection Priorities' column
    priorities_data = data['Food Selection Priorities'].str.get_dummies(sep=', ')
    priorities_counts = priorities_data.sum().reset_index()
    priorities_counts.columns = ['Category', 'Count']
    xAxis_data_priorities = priorities_counts['Category'].tolist()
    series_data_priorities = [{"value": count, "name": category} for category, count in
                              zip(xAxis_data_priorities, priorities_counts['Count'])]

    # Options for 'Food Selection Priorities' bar chart
    options_priorities = {
        "title": {"text": "Food Selection Priorities Analysis", "subtext": "Distribution of Food Selection Priorities",
                  "left": "center"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {"type": "category", "data": xAxis_data_priorities, "axisLabel": {"rotate": 25, "interval": 0}},
        "yAxis": {"type": "value"},
        "series": [{"data": series_data_priorities, "type": "bar"}],
    }

    # Use columns to organize the charts
    col1, col2 = st.columns(2)

    with col1:
        st_echarts(options=options_health, height="550px")

    with col2:
        st_echarts(options=options_priorities, height="550px")

    # Adding a Divider
    st.markdown('---')

    # Whole Grains Consumption and Steps to Improve Diet Analysis
    st.subheader('🥗 Diet Improvement & Whole Grains Analysis')

    # Pie Chart for 'Whole Grains Consumption'
    category_counts_whole_grains = data['Whole Grains Consumption'].value_counts().reset_index()
    category_counts_whole_grains.columns = ['name', 'value']
    chart_data_whole_grains = category_counts_whole_grains.to_dict(orient='records')

    # Options for 'Whole Grains Consumption' pie chart
    options_pie_whole_grains = {
        "title": {
            "text": "Whole Grains Consumption",
            "subtext": "How often do people include whole grains in your meals?",
            "left": "center"
        },
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [
            {
                "name": "Consumption",
                "type": "pie",
                "radius": "50%",
                "data": chart_data_whole_grains,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    }

    # Pie Chart for 'Steps to Improve Diet'
    category_counts_improve_diet = data['Steps to Improve Diet'].value_counts().reset_index()
    category_counts_improve_diet.columns = ['name', 'value']
    chart_data_improve_diet = category_counts_improve_diet.to_dict(orient='records')

    # Options for 'Steps to Improve Diet' pie chart
    options_pie_improve_diet = {
        "title": {
            "text": "Steps to Improve Diet",
            "subtext": "Are you currently taking any steps to improve your dietary habits?",
            "left": "center"
        },
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "left"},
        "series": [
            {
                "name": "Steps to Improve Diet",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": chart_data_improve_diet,
            }
        ],
    }

    # Use columns to organize the charts
    col1, col2 = st.columns(2)

    with col1:
        st_echarts(options=options_pie_whole_grains, height="500px")

    with col2:
        st_echarts(options=options_pie_improve_diet, height="500px")

    # Adding a Divider
    st.markdown('---')

    # Diet Types Tree Chart
    st.subheader('🌱 Diet Types Overview')
    st.markdown('An interactive exploration of various diet types and their characteristics:')

    diet_data = {
        "name": "Diet Types",
        "children": [
            {
                "name": "Vegetarian",
                "children": [
                    {"name": "Lacto-vegetarian",
                     "children": [{"name": "Dairy products included"}, {"name": "No eggs or meat"}]},
                    {"name": "Ovo-vegetarian", "children": [{"name": "Eggs included"}, {"name": "No dairy or meat"}]},
                    {"name": "Lacto-ovo vegetarian",
                     "children": [{"name": "Includes dairy and eggs"}, {"name": "No meat"}]},
                    {"name": "Flexitarian",
                     "children": [{"name": "Primarily vegetarian"}, {"name": "Occasional meat consumption"}]},
                ],
            },
            {
                "name": "Vegan",
                "children": [
                    {"name": "Raw vegan",
                     "children": [{"name": "Only uncooked foods"}, {"name": "No animal products"}]},
                    {"name": "Whole-food vegan",
                     "children": [{"name": "Whole plant foods"}, {"name": "Minimally processed"}]},
                ],
            },
            {
                "name": "Pescatarian",
                "children": [
                    {"name": "Mediterranean",
                     "children": [{"name": "Fish and seafood"}, {"name": "Plant-based with olive oil"}]},
                    {"name": "Nordic", "children": [{"name": "Seafood-rich"}, {"name": "Includes root vegetables"}]},
                ],
            },
            {
                "name": "Ketogenic",
                "children": [
                    {"name": "Standard Ketogenic",
                     "children": [{"name": "High fat"}, {"name": "Low carb"}, {"name": "Moderate protein"}]},
                    {"name": "Targeted Ketogenic",
                     "children": [{"name": "Carbs around workouts"}, {"name": "High fat"}]},
                ],
            },
            {
                "name": "Paleo",
                "children": [
                    {"name": "Primal", "children": [{"name": "Includes dairy"}, {"name": "Grain-free"}]},
                    {"name": "Autoimmune Paleo",
                     "children": [{"name": "Avoids inflammatory foods"}, {"name": "Focus on nutrient density"}]},
                ],
            },
            # Add more diet types and subcategories as needed
            {
                "name": "Fast Food Diet",
                "children": [
                    {"name": "Convenience-focused",
                     "children": [{"name": "Readily available meals"}, {"name": "Includes processed foods"}]},
                    {"name": "Snack-oriented",
                     "children": [{"name": "High in snacks"}, {"name": "Low in whole foods"}]},
                ],
            },
            {
                "name": "Junk Food Diet",
                "children": [
                    {"name": "High Sugar",
                     "children": [{"name": "Soda and candies"}, {"name": "Processed sweet snacks"}]},
                    {"name": "High Fat", "children": [{"name": "Fried foods"}, {"name": "Processed meat products"}]},
                ],
            },
            {
                "name": "Gluten-Free Diet",
                "children": [
                    {"name": "Celiac-friendly",
                     "children": [{"name": "Strictly no gluten"}, {"name": "Focus on gluten-free grains"}]},
                    {"name": "Non-Celiac Gluten Sensitivity",
                     "children": [{"name": "Reduced gluten intake"}, {"name": "Emphasis on whole foods"}]},
                ],
            },
            {
                "name": "Low Carb Diet",
                "children": [
                    {"name": "Atkins Diet",
                     "children": [{"name": "Phases of carb intake"}, {"name": "High protein and fat"}]},
                    {"name": "South Beach Diet",
                     "children": [{"name": "Low glycemic index foods"}, {"name": "Phased approach to carbs"}]},
                ],
            },
            {
                "name": "Mediterranean Diet",
                "children": [
                    {"name": "Heart-healthy", "children": [{"name": "Rich in fruits and vegetables"},
                                                           {"name": "Includes whole grains and lean proteins"}]},
                    {"name": "Wine-inclusive",
                     "children": [{"name": "Moderate wine consumption"}, {"name": "Balanced diet with healthy fats"}]},
                ],
            },
        ],
    }

    # The tree chart option
    option = {
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "series": [
            {
                "type": "tree",
                "data": [diet_data],
                "top": "1%",
                "left": "7%",
                "bottom": "1%",
                "right": "20%",
                "symbolSize": 7,
                "label": {
                    "position": "left",
                    "verticalAlign": "middle",
                    "align": "right",
                    "fontSize": 9,
                },
                "leaves": {
                    "label": {
                        "position": "right",
                        "verticalAlign": "middle",
                        "align": "left",
                    }
                },
                "emphasis": {"focus": "descendant"},
                "expandAndCollapse": True,
                "animationDuration": 550,
                "animationDurationUpdate": 750,
            }
        ],
    }

    # Render the tree chart in Streamlit
    st_echarts(option, height="700px")

    # Footer
    st.markdown("---")
    st.markdown("© 2023 MealMetrics - Unveiling Nutritional Insights")

if selected_page == 'About Us':
    st.title('🌟 About Us')

    # Banner Image for About Page
    # st.image('about_banner.jpg', use_column_width=True)

    st.markdown('''
        ## Welcome to MealMetrics!

        ### 🚀 Project Overview:
        MealMetrics is an innovative, data-driven project focused on dietary habits and nutritional patterns. Our goal is to uncover eating behaviors, preferences, and nutritional choices, using the power of data analytics to provide insights for individuals, health professionals, and policymakers.

        ### 🌱 Our Mission:
        Our mission at MealMetrics is two-pronged:
        - **Empower Individuals:** Providing actionable insights for better dietary habits and lifestyle choices.
        - **Inform Policy and Practice:** Supplying data to professionals for effective nutritional guidelines and health interventions.

        ### 👥 Our Team:
        Led by dedicated professionals like Pravin Tiwari, our team combines expertise in Power BI Development, data visualization, and more to bring complex data to life.

        ### 🛠️ Technologies Used:
        Our approach is underpinned by the use of cutting-edge technologies and tools:

        - Python: Serving as the backbone of our data analysis, Python empowers us to process and analyze large datasets with both efficiency and accuracy. It's the foundation that supports our complex data manipulations and analysis.

        - Streamlit: This powerful tool is instrumental in developing user-friendly web applications. It allows us to make our insights and findings accessible to a wider audience, enhancing interaction and understanding.

        - Plotly: We employ Plotly for its superior capabilities in crafting interactive and engaging visualizations. This enables users to explore data in a more dynamic and intuitive way, making complex data more understandable and visually appealing.

        - Google Forms and Google Sheets: Leveraging Google Forms for data collection and Google Sheets for data storage and preliminary processing, we streamline our data workflow. Google Sheets acts as a flexible and accessible platform for data manipulation, enhanced by Gspread API for seamless integration with Python.

        - Google Cloud Platform (GCP): GCP provides us with essential cloud-based resources, allowing for the automation of our Python scripts and applications. Utilizing services like Compute Engine and Cloud Functions, GCP offers scalability and high availability, critical for managing extensive data workloads.

        - Gspread API: This API is key to integrating Python with Google Sheets, enabling programmatic manipulation of sheets. It's crucial for handling large datasets efficiently, reducing the need for manual data entry and management.

        Together, these technologies form the core of our robust data processing and analysis framework, driving forward our ability to handle complex data challenges with agility and precision.    

        ### 💡 Our Approach:
        We start by collecting a wide array of dietary data through surveys and public datasets. This data is then meticulously analyzed to uncover trends and patterns. Using advanced visualization tools, we translate these findings into easy-to-understand graphs and charts.

        Our web app, developed with Streamlit, serves as an interactive platform for users to explore these insights. Whether it’s identifying the most common dietary preferences or understanding how different factors like age, gender, and lifestyle influence eating habits, MealMetrics brings a new level of clarity to the field of nutritional analysis.

        ### 🤝 Join Us on the Journey:
        Discover and engage with MealMetrics to learn more about dietary habits and nutrition. Let's work towards a healthier future together!
        ''')

    # Footer
    st.markdown("---")
    st.markdown("© 2023 MealMetrics - Pioneering Nutritional Insights")

# Contact Us page
if selected_page == 'Contact Us':
    st.title('📞 Contact Us')

    # Use columns for a structured layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### We'd Love to Hear From You!")
        st.markdown('''
            Your questions, feedback, and ideas are important to us. Feel free to reach out, and we'll make sure to get back to you as soon as possible.
            ''')

    with col2:
        # st.image('D:/MealMetrics/contact_us_image.png.png', width=300)  # Consider adding a relevant image
        pass

    st.markdown("#### 📬 Get in Touch")
    st.markdown('''
        - **Email:** [tiwaripravin114@gmail.com](mailto:tiwaripravin114@gmail.com)
        - **Phone:** [+91 9768878800](tel:+919768878800)
        - **Address:** Nalasopara East, Palghar, Maharashtra 401209
        ''')

    st.markdown("#### 🌐 For More Content")
    st.markdown('''
        Stay updated with our latest news and information. Follow us on:

        - [Github](https://github.com/PravinTiwari023)
        - [LinkedIn](https://www.linkedin.com/in/tiwari-pravin/)
        ''')

    # Optionally, add a contact form
    st.markdown("#### 💬 Send Us a Message")
    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            st.success("Thank you for your message. We'll be in touch soon!")

    # Footer
    st.markdown("---")
    st.markdown("© 2023 MealMetrics - Pioneering Nutritional Insights")