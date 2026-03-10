from dotenv import load_dotenv
import os
import streamlit as st
import requests
import pandas as pd

load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

st.title("🥦 Grocery Macro Tracker")
st.write("Search for foods and get nutrition info from USDA FoodData Central")

foods_input = st.text_area("Enter foods (comma separated)", "chicken breast, rice, broccoli")

if st.button("Get Nutrition Info"):
    foods = [f.strip() for f in foods_input.split(",")]
    results = []

    for food in foods:
        params = {
            "query": food,
            "api_key": API_KEY,
            "pageSize": 1
        }

        try:  # NEW: wrap the API call in a try block
            response = requests.get(BASE_URL, params=params, timeout=10)  # NEW: timeout=10 prevents hanging forever
            response.raise_for_status()  # NEW: raises an exception if the server returned an error (like 403, 500)
            data = response.json()

        except requests.exceptions.Timeout:  # NEW: specifically catches a slow/no response
            st.warning(f"⏱️ Request timed out for '{food}'. Try again.")
            results.append({"Food": food, "Calories": None, "Protein (g)": None, "Carbs (g)": None, "Fat (g)": None})
            continue  # NEW: skips to the next food in the loop instead of crashing

        except requests.exceptions.HTTPError as e:  # NEW: catches bad status codes (403 = bad API key, 500 = server error)
            st.warning(f"⚠️ API error for '{food}': {e}")
            results.append({"Food": food, "Calories": None, "Protein (g)": None, "Carbs (g)": None, "Fat (g)": None})
            continue

        except requests.exceptions.RequestException as e:  # NEW: catches anything else network-related
            st.warning(f"🔌 Network error for '{food}': {e}")
            results.append({"Food": food, "Calories": None, "Protein (g)": None, "Carbs (g)": None, "Fat (g)": None})
            continue

        # Everything below this line is your original logic, unchanged
        if "foods" in data and len(data["foods"]) > 0:
            food_data = data["foods"][0]
            food_name = food_data["description"]
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

    df = pd.DataFrame(results)
    for col in ["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    totals = df[["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]].sum(numeric_only=True)
    totals_row = pd.DataFrame([["TOTAL", totals["Calories"], totals["Protein (g)"], totals["Carbs (g)"], totals["Fat (g)"]]],
                              columns=["Food", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)"])
    final_df = pd.concat([df, totals_row], ignore_index=True)
    st.dataframe(final_df)
