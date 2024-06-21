import sys
!{sys.executable} -m pip install joblib
!{sys.executable} -m pip install streamlit
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import date

# Load the trained model
#loaded_regressor = joblib.load("C:\\Users\\Adminpc2\\Downloads\\trained_random_forest_model.joblib")

# Save the trained model to a file
#joblib.dump(loaded_regressor, 'trained_random_forest_model.joblib')

# Load the saved trained model
loaded_regressor = joblib.load('trained_random_forest_model.joblib')

# Define a function for the login page
def login_page():
    st.markdown("""
    <style>
    body {
        background-color: #004080;
    }
    .main {
        background-color: #004080;
    }
    .stButton button {
        background-color: #008080;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #007070;
    }
    .stTextInput input {
        border: 2px solid #008080;
        border-radius: 5px;
        padding: 10px;
    }
    .stTitle {
        color: white;
    }
    .stImage {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.image("https://nycdsa-blog-files.s3.us-east-2.amazonaws.com/2021/03/chaitali-majumder/house-price-497112-KhCJQICS.jpg", use_column_width=True)
    st.title("House Price Prediction")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":  # Simple authentication, replace with secure method
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Define a function for the prediction form page
def prediction_page():
    st.markdown("""
    <style>
    body {
        background-color: #004080;
    }
    .main {
        background-color: #004080;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #008080;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #007070;
    }
    .stSidebar {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
    }
    .stTitle {
        color: white;
    }
    .stSelectbox, .stSlider, .stTextInput input {
        border: 2px solid #008080;
        border-radius: 5px;
        padding: 10px;
    }
    .result-box {
        background-color: #004080;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("House Price Predictor")
    
    st.sidebar.header("Input Features")
    st.sidebar.markdown("<div class='stSidebar'>", unsafe_allow_html=True)
    bedrooms = st.sidebar.slider("Number of Bedrooms", 1, 10, 3)
    bathrooms = st.sidebar.slider("Number of Bathrooms", 1, 5, 2)
    sqft_living = st.sidebar.slider("Square Feet Living", 1000, 5000, 2000)
    sqft_lot = st.sidebar.slider("Square Feet Lot", 5000, 20000, 10000)
    floors = st.sidebar.selectbox("Number of Floors", [1, 2, 3])
    waterfront = st.sidebar.selectbox("Waterfront?", [0, 1])
    view = st.sidebar.selectbox("View?", [0, 1])
    condition = st.sidebar.selectbox("Condition", [1, 2, 3])
    grade = st.sidebar.selectbox("Grade", list(range(1, 11)))
    sqft_above = sqft_living
    sqft_basement = st.sidebar.slider("Square Feet Basement", 0, 2000, 0)
    yr_built = st.sidebar.slider("Year Built", 1900, 2024, 1990)
    yr_renovated = st.sidebar.slider("Year Renovated (if applicable)", yr_built - 50, yr_built + 50, yr_built)
    zipcode = st.sidebar.text_input("Zipcode", value="98001")
    lat = st.sidebar.text_input("Latitude", value="47.5480")
    long = st.sidebar.text_input("Longitude", value="-121.9836")
    sqft_living15 = sqft_living
    sqft_lot15 = sqft_lot

    current_year = date.today().year
    current_year_input = st.sidebar.date_input('Current Year', value=date(current_year, 1, 1))

    if current_year_input:
        age = current_year_input.year - yr_built
    else:
        age = current_year - yr_built

    input_data_dict = {
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'sqft_living': sqft_living,
        'sqft_lot': sqft_lot,
        'floors': floors,
        'waterfront': waterfront,
        'view': view,
        'condition': condition,
        'grade': grade,
        'sqft_above': sqft_above,
        'sqft_basement': sqft_basement,
        'age': age,
        'renovated': yr_renovated,
        'zipcode': zipcode,
        'lat': lat,
        'long': long,
        'sqft_living15': sqft_living15,
        'sqft_lot15': sqft_lot15
    }

    input_data_array = np.array([[input_data_dict[feature] for feature in loaded_regressor.feature_names_in_]])

    if st.button('Predict'):
        prediction = loaded_regressor.predict(input_data_array)[0]
        result = f"Estimated House Price: ${prediction:,.2f}"
        st.markdown(f"""
        <div class='result-box'>
            <p style='font-size: 20px;'>{result}</p>
        </div>
        """, unsafe_allow_html=True)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Show the login page if not logged in, else show the prediction page
if not st.session_state.logged_in:
    login_page()
else:
    prediction_page()
