import os
import sys
import math
from operator import itemgetter


def insert_doc(folder, file_name, words, table):
    new_vector = [file_name]

    # append 0 to the vector until it's equal to words
    for i in range(1, len(words)):
        new_vector.append(0)

    with open(folder + os.path.sep + file_name, 'r') as doc:
        for line in doc:
            for word in line.split():
                # make every word lowercase and omit punctuation
                word = word.lower()
                if word[0] in ['(', '[', '{', '-']:
                    word = word[1:]
                if word[-1] in ['.', ',', ':', '!', '?', ';',
                                ')', ']', '}', '-']:
                    word = word[:-1]

                # if the current word already exists in words, then
                # the new vector's corresponding value is increased by 1
                # if index(word) raises a ValueError (occurs when the word
                # was not found), then the word is appended to the list
                # and a 1 is appended to the vector
                try:
                    index = words.index(word)
                    new_vector[index] += 1
                except ValueError:
                    words.append(word)
                    new_vector.append(1)

    table.append(new_vector)

    return words, table


# make every vector have the same amount of dimensions
def finalize_table(table):
    for i in range(1, len(table)):
        for j in range(len(table[i]), len(words)):
            table[i].append(0)

    return table


def calculate_similarity(vec1, vec2):
    inner_product = 0
    vec1_length = 0
    vec2_length = 0

    # at this point both vectors should be the same size because
    # finalize_table() was called before this function
    for i in range(0, len(vec1)):
        # calculate the inner product of the given vectors
        inner_product += vec1[i] * vec2[i]
        # calculate each vector's Euclidean length
        vec1_length += vec1[i] ** 2
        vec2_length += vec2[i] ** 2

    try:
        # sqrt is calculated here in order to reduce calls to math.sqrt
        result = inner_product / math.sqrt(vec1_length * vec2_length)
        # return the calculated similarity with precision of 4 decimals
        return float(str(result)[:6])
    except ZeroDivisionError:
        print("Unable to calculate document similarity\
 because one document is empty.")
        # -1 is returned as an error code, as 0 should be returned when
        # two documents have not any common words
        return -1.0


def similarity_ranking(K, table):
    ranking = []

    for i in range(1, len(table) - 1):
        for j in range(i + 1, len(table)):
            score = calculate_similarity(table[i][1:], table[j][1:])
            name = str(table[i][0]) + " - " + str(table[j][0])
            ranking.append([name, score])

    # sort the ranking by decreasing score
    ranking.sort(key=itemgetter(1), reverse=True)

    # print the first K pairs with the highest similarity score
    for i in range(0, K):
        print(ranking[i][0], '|', ranking[i][1])


def argument_validity(N, K):
    if N < 2:
        print("N can't be lower than 2. N set to 2.")
        N = 2

    combinations = math.factorial(N) / (2 * math.factorial(N - 2))

    if combinations == 1 and K > 0:
        K = 1
    elif K > combinations - 1:
        K = int(combinations) - 1

    return N, K


if __name__ == "__main__":
    words = ["Doc ID"]
    table = [words]
    documents_folder = "documents"
    added_documents = 0
    valid_file_types = [".txt", ".log", ".md"]
    N_documents_found = False

    if len(sys.argv) < 3:
        print("Not enough arguments. Please give two positive integers.")
        print("Usage: python3", sys.argv[0], "<N> <K> [documents_folder]")
        sys.exit()
    elif len(sys.argv) > 3:
        documents_folder = sys.argv[3]

    try:
        N, K = argument_validity(int(sys.argv[1]), int(sys.argv[2]))
    except ValueError:
        print("Wrong argument type. Please give two positive integers.")
        sys.exit()

    if not os.path.exists(documents_folder):
        try:
            os.makedirs(documents_folder)
            print("Not enough documents were found (at least 2 needed).")
        except OSError:
            print("Unable to create", documents_folder)

        sys.exit()

    for _, _, files in os.walk(documents_folder):
        for file in files:
            # check if the current file is a text file
            if str.lower(os.path.splitext(file)[1]) in valid_file_types:
                words, table = insert_doc(documents_folder, file, words, table)
                added_documents += 1

                if added_documents == N:
                    N_documents_found = True
                    break

    if added_documents < 2:
        print("Not enough documents were found (at least 2 needed).")
        sys.exit()

    if not N_documents_found:
        print("Unable to find", N, "documents. N set to", added_documents,
              "(amount of documents found). K adjusted accordingly.")
        N, K = argument_validity(added_documents, K)

    table = finalize_table(table)
    similarity_ranking(K, table)
