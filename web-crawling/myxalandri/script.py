import os

def find_missing_number(folder_path):
    # Get a list of all filenames in the folder
    filenames = os.listdir(folder_path)
    
    # Extract the numbers from the filenames and convert them to integers
    numbers = [int(filename.split('.')[0]) for filename in filenames if filename.endswith('.txt')]
    
    # Sort the numbers in ascending order
    numbers.sort()
    
    # Find the missing number
    for i, num in enumerate(numbers):
        if i != num:
            return i
    
    # If no missing number found, the missing number is the next number after the last one in the sequence
    return len(numbers)

# Example usage:
folder_path = "txt_files"
missing_number = find_missing_number(folder_path)
print("The missing number is:", missing_number)
