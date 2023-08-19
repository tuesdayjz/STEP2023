# STEP2023 Week1 Assignment 1
# Name: Kayo Tei

# this code receives random words from input file,
# and find words from [words.txt],
# then write the result to output file.

#       usage: python3 week1-1.py input.txt output.txt
#  input file: random words (one word per line)
# output file: founded words (several words per line)

import itertools
import sys


# Store words.txt to list
def store_dictionary_to_list(dictionary: list[str]) -> None:
    with open("words.txt", "r") as infile:
        for word in infile:
            dictionary.append(word.rstrip("\n"))
    return None


# Store input.txt to list
def store_input_to_list(inputs: list[str], input_file: str) -> None:
    with open(input_file, "r") as infile:
        for word in infile:
            inputs.append(word.rstrip("\n"))
    return None


# Write founded_words to output.txt
def write_output_to_file(founded_words: list[str], output_file: str) -> None:
    with open(output_file, "w") as outfile:
        for founded_word in founded_words:
            if founded_word:
                for word in founded_word:
                    if word == founded_word[-1]:
                        outfile.write(word)
                    else:
                        outfile.write(word + " ")
                outfile.write("\n")
            else:
                outfile.write("\n")
    return None


# Straight forward solution ( len(random_word) < 10 )
def straight_forward_solution(random_word: str, dictionary: list[str]) -> list[str]:
    rearranged_words: list = generate_possible_words(random_word)
    founded_words: list = []
    for rearranged_word in rearranged_words:
        if binary_search_word(rearranged_word, dictionary) is not None:
            founded_words.append(binary_search_word(
                rearranged_word, dictionary))
    return founded_words


# Generate all possible rearranged words from random_word
def generate_possible_words(word: str) -> list[str]:
    rearranged_set = set("".join(w) for w in itertools.permutations(word))
    rearranged_list = sorted(rearranged_set)
    return rearranged_list


# Binary search word from basic dictionary
def binary_search_word(word: str, dictionary: list[str]) -> str | None:
    low: int = 0
    high: int = len(dictionary) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if dictionary[mid] == word:
            return word
        elif dictionary[mid] < word:
            low = mid + 1
        else:
            high = mid - 1
    return None


# Better solution (10 <= len(random_word))
def better_solution(
    random_word: str, sorted_new_dictionary: list[tuple[str, str]]
) -> list[str]:
    sorted_random_word: str = generate_sorted_word(random_word)
    return binary_search_words_from_tuple_list(
        sorted_random_word, sorted_new_dictionary, []
    )


# sort random_word alphabetically
def generate_sorted_word(word: str) -> str:
    return "".join(sorted(word))


# sorted dictionary words and store in tuple list: [(sorted_word, word), ...]
def generate_sorted_new_dictionary(dictionary: list[str]) -> list[tuple[str, str]]:
    new_dictionary: list = []
    for word in dictionary:
        new_dictionary.append((generate_sorted_word(word), word))
    sorted_new_dictionary: list = sorted(new_dictionary, key=lambda x: x[0])
    return sorted_new_dictionary


# Binary search word from sorted new dictionary and store in list
def binary_search_words_from_tuple_list(
    word: str, new_dictionary: list[tuple[str, str]], founded_words: list[str]
) -> list[str]:
    low: int = 0
    high: int = len(new_dictionary) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if new_dictionary[mid][0] == word:
            founded_words.append(new_dictionary[mid][1])
            founded_words = binary_search_words_from_tuple_list(
                word, new_dictionary[:mid], founded_words
            )
            founded_words = binary_search_words_from_tuple_list(
                word, new_dictionary[mid + 1:], founded_words
            )
            return founded_words
        elif new_dictionary[mid][0] < word:
            low = mid + 1
        else:
            high = mid - 1
    return founded_words


# Check if the input word contains only alphabets and whitespaces
def is_alphabets(word: str) -> bool:
    for alphabet in word:
        if alphabet not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ":
            return False
    return True


# Main function
def main(input_file: str, output_file: str) -> None:
    dictionary: list = []
    store_dictionary_to_list(dictionary)
    inputs: list = []
    store_input_to_list(inputs, input_file)
    sorted_new_dictionary: list = generate_sorted_new_dictionary(dictionary)
    founded_words: list = []
    for random_word in inputs:
        if is_alphabets(random_word):
            # ignore whitespace and convert to lower case
            lower_random_word: str = random_word.replace(" ", "").lower()
            if len(random_word) < 10:
                founded_words.append(
                    straight_forward_solution(lower_random_word, dictionary)
                )
            else:
                founded_words.append(
                    better_solution(lower_random_word, sorted_new_dictionary)
                )
        else:
            # if the input word contains non-alphabets, append empty list
            founded_words.append([])
        write_output_to_file(founded_words, output_file)
    return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s input_file output_file" % sys.argv[0])
        exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
        print("result is succesfully written to [%s]" % sys.argv[2])
        exit(0)
