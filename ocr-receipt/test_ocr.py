import cv2
from PIL import Image
import pytesseract

# Path to your image file
image_path = "WIN_20251014_19_41_22_Pro.jpg"

# Read image with OpenCV
img = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding (turns image black & white)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Save processed image to view result
cv2.imwrite("processed_receipt.jpg", thresh)

# Use Tesseract to extract text
text = pytesseract.image_to_string(thresh)

print("🧾 Extracted Text After Cleaning:")
print("----------------------------------")
print(text)
