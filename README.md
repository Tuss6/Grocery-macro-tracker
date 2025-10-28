# Grocery Macro Tracker 🥦

**Grocery Macro Tracker** is a simple Streamlit app that helps you search foods from USDA FoodData Central and view their nutrition macros (calories, protein, carbs, fat).  
The long-term vision is to build a smarter grocery and nutrition assistant that helps manage both health goals and grocery budgets.

---

## ⚙️ Current Features

- Search for multiple foods at once  
- Nutrition lookup powered by USDA FoodData Central API  
- Results displayed in a clean, filterable table  
- Macro totals across all foods entered  
- **Early OCR Integration:** The app now includes an initial Optical Character Recognition (OCR) setup for reading grocery receipts and extracting food names.  
  - Currently in the **fine-tuning stage** — OCR is being tested with varying image quality to understand its reliability.  
  - Testing continues with both **original lower-quality photos** and **higher-quality versions** to explore the model’s limits and improvement potential.

---

## 🧠 Planned Features

- Refined OCR parsing for automatic detection of foods and quantities  
- Handle cases where quantities are missing (default to 100 grams)  
- Bulk buying recommendations for cost savings  
- Recipe ideas based on ingredients on hand  
- Healthy substitute suggestions to satisfy cravings

---

## 🌱 Project Vision

Grocery costs continue to rise, and eating healthy can feel overwhelming without the right tools.  
This project bridges the gap between **budgeting and nutrition** by giving users a clear breakdown of the macros in their groceries.

- **For budgeting:** Smarter store choices and opportunities for bulk savings.  
- **For health:** Tracking macros at the grocery stage helps stick to dietary goals (cutting, bulking, or balanced living).  
- **For planning:** AI-powered features will suggest recipes, substitutions, and cost-saving shopping strategies.

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- Requests  
- USDA FoodData Central API  
- EasyOCR / Tesseract (OCR testing)

---

## 🚀 Getting Started

Clone the repository:
```bash
git clone https://github.com/Tuss6/Grocery-macro-tracker.git

pip install -r requirements.txt

streamlit run app.py


