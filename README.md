# Cosine Similarity

Script to find the TOP-K similar pairs of text among N given texts. The similarity ratio of a pair of texts is measured using the [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) method.
This script was made as a university project.

## Getting Started

### Prerequisites

Python 3

### Using the script

Run the script as follows:
```
$ python3 cosine_similarity.py <N> <K> [documents_folder]
```
Explanation of arguments
```
Necessary:
Ν                   Amount of texts to process.
Κ                   Amount of pairs to display (in descending order of similarity).

Options:
documents_folder    Directory to search for texts. Default value is "documents".
```
