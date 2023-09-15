import streamlit as st
import pandas as pd
import plotly.express as px
from marketing_attribution_models import MAM
from PIL import Image

# App Title and Description
st.title("Marketing Attribution Models App")
st.write("""
Select a model, provide the necessary inputs, and get the attribution results.
This app supports Heuristic, Markov, and Shapley attribution models.
""")

# Sidebar for Model Descriptions and Dynamic Descriptions
st.sidebar.header("Model Descriptions")
model_choice = st.sidebar.selectbox("Choose an Attribution Model", ["Heuristic", "Markov", "Shapley"])

model_descriptions = {
    "Heuristic": "Assigns conversion value based on simple rules. E.g., Last Touch gives all credit to the last channel.",
    "Markov": "Considers the entire customer journey and calculates the importance of each channel.",
    "Shapley": "Based on cooperative game theory, it distributes the conversion value among all channels."
}
st.sidebar.write(model_descriptions[model_choice])

# Upload Data
uploaded_file = st.file_uploader("Upload your data file (CSV format)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Data Preview and Summary
    if st.checkbox("Show Data Preview"):
        st.dataframe(df.head())
    if st.checkbox("Show Data Summary"):
        st.write(df.describe())

    channel_col = st.text_input("Enter Channel Column Name", "channel")
    conversion_col = st.text_input("Enter Conversion Column Name", "conversion")
    value_col = st.text_input("Enter Value Column Name (Optional)", "")

    # Model-specific Inputs and Execution
    if model_choice == "Heuristic":
        heuristic_model = st.selectbox("Choose a Heuristic Model", ["last_touch", "first_touch", "linear", "time_decay"])
        result = MAM.heuristic_models(df, channel_col, conversion_col, value_col, heuristic_model)
        fig = px.bar(result, title="Heuristic Model Results")
        st.plotly_chart(fig)

    elif model_choice == "Markov":
        order = st.slider("Order", 1, 5, 1)
        output = st.selectbox("Output Type", ["transition_matrix", "attribution"])
        result = MAM.markov_model(df, channel_col, conversion_col, value_col, order, output)
        fig = px.bar(result, title="Markov Model Results")
        st.plotly_chart(fig)

    elif model_choice == "Shapley":
        n_simulations = st.slider("Number of Simulations", 1000, 20000, 10000)
        result = MAM.shapley_model(df, channel_col, conversion_col, value_col, n_simulations)
        fig = px.bar(result, title="Shapley Model Results")
        st.plotly_chart(fig)

    # Download Results
    if st.button("Download Results as CSV"):
        csv = result.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

# Feedback System
st.sidebar.header("Feedback")
if st.sidebar.button("👍"):
    st.sidebar.write("Thank you for your positive feedback!")
elif st.sidebar.button("👎"):
    feedback_text = st.sidebar.text_area("Please provide your feedback to help us improve.")
    if st.sidebar.button("Submit Feedback"):
        st.sidebar.write("Thank you for your feedback!")


