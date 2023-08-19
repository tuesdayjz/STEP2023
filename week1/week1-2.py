# STEP2023 Week1 Assignment 2
# Name: Kayo Tei

# this code receives random words from input file,
# and find highest-score-word from [words.txt],
# then write the result to output file.

#       usage: python3 week1-2.py input.txt output.txt
#  input file: random words (one word per line)
# output file: founded words (one word per line)

import itertools
import sys

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# Store words.txt to list
def store_dictionary_to_list(dictionary: list[str]) -> None:
    with open('words.txt', 'r') as infile:
        for word in infile:
            dictionary.append(word.rstrip('\n'))
    return None

# Store input.txt to list
def store_input_to_list(inputs: list[str], input_file: str) -> None:
    with open(input_file, 'r') as infile:
        for word in infile:
            inputs.append(word.rstrip('\n'))
    return None

# Write founded_words to output.txt
def write_output_to_file(founded_words: list[str], output_file: str) -> None:
    with open(output_file, 'w') as outfile:
        for founded_word in founded_words:
            if founded_word:
                outfile.write(founded_word + '\n')
            else:
                outfile.write('\n')
    return None

def generate_word_score_tuple_list(dictionary: list[str]) -> list[tuple[str, int]]:
    words_score_tuple_list: list = []
    for word in dictionary:
        words_score_tuple_list.append((word, calculate_score(word)))
    return words_score_tuple_list

# Calculate score of word
def calculate_score(word: str) -> int:
    score : int = 0
    for alphabet in word:
        score += SCORES[ord(alphabet) - ord('a')]
    return score

### Solution 1 ( len(random_word) < 13 ) ###
def solution_1(random_word: str, sorted_new_dictionary: list[tuple[str, tuple[str, int]]]) -> str:
    rearranged_words : list = generate_possible_words_allow_substrings(random_word)
    founded_words : list = []
    found: bool = False
    founded_max_length: int = 0
    for rearranged_word in rearranged_words:
        if len(rearranged_word) < founded_max_length - 2:
            break
        if binary_search_word(rearranged_word, sorted_new_dictionary) != None:
            if not found and len(rearranged_word) > founded_max_length:
                found = True
                founded_max_length = len(rearranged_word)
                founded_words.append(binary_search_word(rearranged_word, sorted_new_dictionary))
            if found:
                founded_words.append(binary_search_word(rearranged_word, sorted_new_dictionary))
    founded_words.sort(key=len)
    return find_highest_score_word_sol1(founded_words)

# Generate all possible rearranged words from random_word (allow substrings)
def generate_possible_words_allow_substrings(word: str) -> list[str]:
    possible_words = []
    for i in range(1, len(word) + 1):
        substrings = itertools.permutations(word, i)
        possible_substring_words = [''.join(substring) for substring in substrings]
        possible_words.extend(possible_substring_words)
    possible_words.sort(key=len, reverse=True)
    return possible_words

# sorted dictionary words and store in tuple list: [(sorted_word, word), ...]
def generate_sorted_new_dictionary(dictionary: list[tuple[str, int]]) -> list[tuple[str, tuple[str, int]]]:
    new_dictionary: list = []
    for word in dictionary:
        new_dictionary.append((generate_sorted_word(word[0]), word))
    sorted_new_dictionary: list = sorted(new_dictionary, key=lambda x: x[0])
    return sorted_new_dictionary

# sort word alphabetically
def generate_sorted_word(word: str) -> str:
    return ''.join(sorted(word))

# Binary search word from tuple-list dictionary
def binary_search_word(word: str, dictionary: list[tuple[str, tuple[str, int]]]) -> tuple[str, tuple[str, int]] | None:
    low: int = 0
    high: int = len(dictionary) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if dictionary[mid][0] == word:
            return dictionary[mid]
        elif dictionary[mid][0] < word:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Find highest-score-word from list of founded words
def find_highest_score_word_sol1(founded_words: list[tuple[str, tuple[str, int]]]) -> str:
    highest_score : int = 0
    highest_score_word : str = ''
    for founded_word in founded_words:
        if founded_word[1][1] > highest_score:
            highest_score = founded_word[1][1]
            highest_score_word = founded_word[1][0]
    return highest_score_word

### Solution 2 ( len(random_word) >= 13 ) ###
def solution_2(alphabet_dictionary: list[tuple[dict[str, int], tuple[str, int]]], random_word_alphabet_nums: dict[str, int]) -> str:
    for alphabet_dict, word in alphabet_dictionary:
        if is_subset(random_word_alphabet_nums, alphabet_dict):
            highest_score_word: str = word[0]
            return highest_score_word
    return ''

# Generate alphabet dictionary = [({a:?, b:?, ... , z:?}, (word, score)), ...]
def generate_alphabet_dictionary(dictionary: list[tuple[str, int]]) -> list[tuple[dict[str, int], tuple[str, int]]]:
    alphabet_dictionary : list = []
    for word in dictionary:
        alphabet_dictionary.append((count_alphabets(word[0]), (word[0], word[1])))
    # sort by score
    alphabet_dictionary.sort(key=lambda x: x[1][1], reverse=True)
    return alphabet_dictionary

# Count alphabets in word and store in tuple = {a:?, b:?, ... , z:?}
def count_alphabets(word: str) -> dict[str, int]:
    alphabet_counts: dict[str, int] = {}
    for alphabet in word:
        if alphabet in alphabet_counts:
            alphabet_counts[alphabet] += 1
        else:
            alphabet_counts[alphabet] = 1
    return alphabet_counts

# Check if target_dict is subset of dict
def is_subset(dict: dict[str, int], target_dict: dict[str, int]) -> bool:
    for key, value in target_dict.items():
        if key not in dict or value > dict[key]:
            return False
    return True

# Check if the input word contains only alphabets and whitespace
def is_alphabets(word: str):
    for alphabet in word:
        if alphabet not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ':
            return False
    return True

# Main function
def main(input_file: str, output_file: str) -> None:
    dictionary: list = []
    store_dictionary_to_list(dictionary)
    word_score_tuple_list : list[tuple[str,int]] = generate_word_score_tuple_list(dictionary)
    sorted_new_dictionary : list = generate_sorted_new_dictionary(word_score_tuple_list)
    alphabet_dictionary : list = generate_alphabet_dictionary(word_score_tuple_list)
    inputs: list = []
    store_input_to_list(inputs, input_file)
    founded_words: list = []
    for input_word in inputs:
        if is_alphabets(input_word):
            lower_input_word = input_word.replace(' ', '').lower()
            if len(lower_input_word) < 13:
                founded_words.append(solution_1(lower_input_word, sorted_new_dictionary))
            else:
                random_word_alphabet_nums : dict = count_alphabets(lower_input_word)
                founded_words.append(solution_2(alphabet_dictionary, random_word_alphabet_nums))
        else:
            founded_words.append('')
        write_output_to_file(founded_words, output_file)
    return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s input_file output_file" % sys.argv[0])
        exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
        print("result is succesfully written to [%s]" % sys.argv[2])
