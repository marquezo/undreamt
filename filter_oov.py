import math
import concurrent.futures
from itertools import repeat
from update_corpus import chunks
import io


def filter_oov(lines, vocab):
    filtered = []

    for line in lines:
        tokens = line.rstrip().split()
        num_oov = 0.

        for token in tokens:
            if token not in vocab:
                num_oov += 1

        if num_oov / len(tokens) <= 0.1:
            filtered.append(line)

    return filtered


embeddings_handler = io.open("train_emb_full_mapped.eu", 'r', encoding='utf-8', newline='\n', errors='ignore')

n, d = map(int, embeddings_handler.readline().split())
print("Found {} embeddings with dimension {}".format(n, d))

vocab = []

for line in embeddings_handler:
    tokens = line.rstrip().split(' ')
    vocab.append(tokens[0])

print(len(vocab))


with open("all_sentences.eu", "r") as f:
    sentences = f.readlines()

num_chunks = 1000
chunked_sentences = chunks(sentences, num_chunks)
vocab_repeated = repeat(vocab, math.ceil(len(sentences) / num_chunks))
result = []

with concurrent.futures.ProcessPoolExecutor() as executor:
    for updated_sents in executor.map(filter_oov, chunked_sentences, vocab_repeated):
        result.extend(updated_sents)

        if len(result) % 100000 == 0:
            print("Processed {} sentences".format(len(result)))

with open("clean_mono.eu", 'w') as file:
    file.writelines("%s" % line for line in result)