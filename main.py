import os
from collections import Counter
import re

# Define the path to the texts folder
texts_folder = "./gutenberg_books"

# Initialize a Counter to store letter frequencies
letter_freq = Counter()
total_letters = 0


# Function to clean and extract letters
def clean_text(text):
    # Keep only alphabetic characters and make them lowercase
    letters = re.findall(r"[a-z]", text.lower())
    return letters


# Iterate over each file in the texts folder
for filename in os.listdir(texts_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(texts_folder, filename)
        # Use 'latin-1' encoding to avoid UnicodeDecodeError
        with open(file_path, "r", encoding="latin-1") as file:
            text = file.read()
            # Extract letters only
            letters = clean_text(text)
            # Update the Counter with the letters from this file
            letter_freq.update(letters)
            # Update the total letter count
            total_letters += len(letters)

# Calculate letter percentages
letter_percentage = {
    letter: (count / total_letters) * 100 for letter, count in letter_freq.items()
}

# Display the top 10 most common letters and their percentages
print("Top 10 most common letters (percentage):")
for letter, percentage in sorted(
    letter_percentage.items(), key=lambda item: item[1], reverse=True
)[:10]:
    print(f"{letter}: {percentage:.2f}%")

# If you want to save the results to a file
output_file = "letter_percentage_frequencies.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for letter, percentage in sorted(
        letter_percentage.items(), key=lambda item: item[1], reverse=True
    ):
        f.write(f"{letter}: {percentage:.2f}%\n")

print(f"Letter percentages saved to {output_file}")
