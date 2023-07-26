import os
import re
from collections import defaultdict
import numpy as np

class WebsiteDataAnalyzer():
    """
    This class is responsible for analyzing the data extracted from the crawled websites.
    """
    def __init__(self, directory = None):
        self.directory = directory

    def get_sentences_from_text(self, text):
        """
        Split text into sentences using a regular expression.
        """
        # Split text into sentences using a regular expression.
        sentences = re.split(r'[.!?]', text)
        # Remove any leading/trailing whitespaces from sentences.
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences

    def get_sentences_and_files(self,):
        """
        Get the sentences and the files in which they were found.
        """
        sentences_dict = defaultdict(list)
        for filename in os.listdir(f'{self.directory}/txt_files/'):
            # print('--', filename)
            if filename.endswith('.txt'):
                with open(f'{self.directory}/txt_files/'+filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Extract the description section using regex.
                    description_match = re.search(r'Description:(.+)', content, re.DOTALL)
                    if description_match:
                        description_text = description_match.group(1)
                        sentences = self.get_sentences_from_text(description_text)
                        for sentence in sentences:
                            sentences_dict[sentence].append(filename)
        return sentences_dict

    def print_duplicates(self, sentences_dict):
        """
        Print the sentences that were found in more than one files.
        """
        for sentence, files in sentences_dict.items():
            # if length of sentence is greater than 10 characters:
            if len(sentence) > 50:
                if len(np.unique(files)) > 1 and len(files) > 1:
                    print(f"Sentence: {sentence}")
                    print("Found in files:", ", ".join(np.unique(files)))
                    print()

