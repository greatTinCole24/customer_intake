import streamlit as st
import pandas as pd

# Function to load the CSV file
def load_csv(file):
    return pd.read_csv(file)

# Function to display the filters and table
def display_vehicle_selection(data):
    st.title("Vehicle Selection App")

    # Display column names for debugging
    st.write("Column names in the uploaded file:")
    st.write(data.columns)

    # Normalize column names (remove leading/trailing spaces and lower case)
    data.columns = data.columns.str.strip().str.lower()

    # Expected column names (normalize them for comparison)
    expected_columns = {
        'make': 'make of vehicle',
        'model': 'model of vehicle',
        'price': 'price'
    }

    # Check if 'Make of vehicle' column exists (case-insensitive)
    if expected_columns['make'] in data.columns:
        make = st.selectbox("Select Make of Vehicle", data[expected_columns['make']].unique())
        
        # Filter the data based on selected make
        filtered_data_by_make = data[data[expected_columns['make']] == make]

        # Check if 'Model of vehicle' column exists
        if expected_columns['model'] in filtered_data_by_make.columns:
            model = st.selectbox("Select Model of Vehicle", filtered_data_by_make[expected_columns['model']].unique())

            # Further filter the data based on selected model
            filtered_data_by_model = filtered_data_by_make[filtered_data_by_make[expected_columns['model']] == model]

            # Pricing Filter (if the 'Price' column exists)
            if expected_columns['price'] in filtered_data_by_model.columns:
                min_price, max_price = st.slider(
                    "Select Price Range",
                    int(filtered_data_by_model[expected_columns['price']].min()),
                    int(filtered_data_by_model[expected_columns['price']].max()),
                    (int(filtered_data_by_model[expected_columns['price']].min()), int(filtered_data_by_model[expected_columns['price']].max()))
                )
                filtered_data_by_model = filtered_data_by_model[
                    (filtered_data_by_model[expected_columns['price']] >= min_price) & 
                    (filtered_data_by_model[expected_columns['price']] <= max_price)
                ]

            # Display filtered table
            st.subheader("Filtered Results")
            st.dataframe(filtered_data_by_model)
        else:
            st.error(f"'{expected_columns['model']}' column not found in the uploaded data.")
    else:
        st.error(f"'{expected_columns['make']}' column not found in the uploaded data.")

# Streamlit app code
st.title("Upload Vehicle Data")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# If a file is uploaded, load and display the data
if uploaded_file is not None:
    data = load_csv(uploaded_file)
    st.subheader("Uploaded Data")
    st.dataframe(data)

    # Display the vehicle selection filters
    display_vehicle_selection(data)
