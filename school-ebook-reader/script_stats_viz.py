import glob
import os
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

# Define the directory pattern
directory_pattern = 'books/*/*'

# Create dictionaries to store the total words and total sections for each book
book_word_counts = defaultdict(int)
book_section_counts = defaultdict(int)

# Use glob to find files that match the pattern
for file_path in glob.glob(directory_pattern):
    # Check if the path is a file (not a directory)
    if os.path.isfile(file_path):
        # Extract the book name from the file path
        book_name = os.path.basename(os.path.dirname(file_path))
        
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the file and split it into words
            words = file.read().split()
            # Count the number of words in the file
            num_words = len(words)
            # Add the number of words in the file to the total count for the book
            book_word_counts[book_name] += num_words
            # Increment the section count for the book
            book_section_counts[book_name] += 1

# Print the number of words and sections for each book
for book, word_count in book_word_counts.items():
    section_count = book_section_counts[book]
    print(f"Book: {book}, Total Words: {word_count}, Total Sections: {section_count}")

# Calculate and print the total number of words for all books
total_words = sum(book_word_counts.values())
print(f"Total Words for All Books: {total_words}")

# Plot the number of words for each book
plt.figure(figsize=(12, 6))
sns.barplot(x=list(book_word_counts.keys()), y=list(book_word_counts.values()))
plt.grid(axis='y', color='black', linestyle='-', linewidth=0.25, alpha=0.5)
plt.gca().set_facecolor('#155a7b')
plt.xlabel('Book')
plt.ylabel('Number of Words')
plt.title('Number of Words in Each Book')
plt.xticks(rotation=90)




# Create a pie chart for the number of words in each book using Seaborn
plt.figure(figsize=(8, 8))
sns.set_palette("Set3")  # Set a color palette for the pie chart
plt.pie(book_word_counts.values(),  autopct='%1.1f%%', startangle=140)
plt.title('Percentage of Words in Each Book')
# set color for the background to dark gray:
plt.gca().set_facecolor('#155a7b')
# Show the pie chart
# dont show book name but annotate the colors on the right
plt.legend(book_word_counts.keys(), loc="center right", bbox_to_anchor=(1, 0, 0.5, 1))
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()