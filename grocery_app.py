from dotenv import load_dotenv
import os
import streamlit as st
import requests
import pandas as pd

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

st.title("🥦 Grocery Macro Tracker")
st.write("Search for foods and get nutrition info from USDA FoodData Central")

# Input for multiple foods
foods_input = st.text_area("Enter foods (comma separated)", "chicken breast, rice, broccoli")

if st.button("Get Nutrition Info"):
    foods = [f.strip() for f in foods_input.split(",")]
    results = []

    for food in foods:
        params = {
            "query": food,
            "api_key": API_KEY,
            "pageSize": 1  # Just take the best match
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "foods" in data and len(data["foods"]) > 0:
            food_data = data["foods"][0]
            food_name = food_data["description"]

            # Extract nutrients (USDA standard codes for macros)
            nutrients = {nutrient["nutrientName"]: nutrient["value"] for nutrient in food_data["foodNutrients"]}

            results.append({
                "Food": food_name,
                "Calories": nutrients.get("Energy", None),
                "Protein (g)": nutrients.get("Protein", None),
                "Carbs (g)": nutrients.get("Carbohydrate, by difference", None),
                "Fat (g)": nutrients.get("Total lipid (fat)", None)
            })
        else:
            results.append({"Food": food, "Calories": None, "Protein (g)": None, "Carbs (g)": None, "Fat (g)": None})

    # Build DataFrame
    df = pd.DataFrame(results)

    # Convert numeric columns to numbers
    for col in ["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Add totals row
    totals = df[["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]].sum(numeric_only=True)
    totals_row = pd.DataFrame([["TOTAL", totals["Calories"], totals["Protein (g)"], totals["Carbs (g)"], totals["Fat (g)"]]],
                              columns=["Food", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)"])

    final_df = pd.concat([df, totals_row], ignore_index=True)

    # Show table
    st.dataframe(final_df)
