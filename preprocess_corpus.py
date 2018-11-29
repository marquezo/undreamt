import nltk, re, string
from tqdm import tqdm
import argparse
from unicodedata import normalize
from euskalToken import EuskalToken
from collections import Counter
from nltk.tokenize.treebank import TreebankWordTokenizer


# clean a list of lines, tokenize using basque tokenizer and respect the min and max # of tokens per sentence
def clean_lines(lines, min_tokens, max_tokens, word_tokenizer):
    cleaned = []
    # prepare regex for char filtering
    re_print = re.compile('[^%s]' % re.escape(string.printable))
    # prepare translation table for removing punctuation
    table = str.maketrans('', '', string.punctuation)

    vocab = Counter()

    for line in tqdm(lines):
        # normalize unicode characters
        line = normalize('NFD', line).encode('ascii', 'ignore')
        line = line.decode('UTF-8')
        # tokenize
        line = word_tokenizer.tokenize(line)
        # convert to lower case
        line = [word.lower() for word in line]
        # remove punctuation from each token - Maybe not because we lose punctuation inside a sentence
        #line = [word.translate(table) for word in line]
        # remove non-printable chars from each token
        line = [re_print.sub('', w) for w in line]
        # remove tokens with numbers in them - Maybe not because we lose punctuation
        # line = [word for word in line if word.isalpha()]

        if min_tokens <= len(line) <= max_tokens:
            # store as string
            cleaned.append(' '.join(line))
            # Update vocabulary counter
            vocab.update(line)

    return cleaned, vocab


def process_corpus(corpus, min_tokens, max_tokens, size_vocab, sentence_tokenizer, word_tokenizer):

    with open(corpus, mode='rt', encoding='utf-8')as file:
        corpus_content = file.readlines()

    sentences = []

    print("Sentence tokenizing corpus")

    for paragraph in tqdm(corpus_content):
        sentences.extend(sentence_tokenizer.tokenize(paragraph))

    print("Cleaning and selecting sentences")

    sentences, vocab = clean_lines(sentences, min_tokens, max_tokens, word_tokenizer)

    print("Found {} sentences".format(len(sentences)))

    # Only keep the desired number of tokens in vocabulary
    most_common = vocab.most_common(size_vocab)
    vocab = [k for k, c in most_common]

    return vocab, sentences


def main():
    parser = argparse.ArgumentParser(description="Given a corpus, create vocabulary and tokenize sentences")
    parser.add_argument("corpus", help="Corpus", type=str)
    parser.add_argument("vocab", help="File where to output vocabulary", type=str)
    parser.add_argument("sentences", help="File where to output the pre-processed sentences", type=str)
    parser.add_argument("lang", help="English or Basque", type=str, choices=['eu', 'en'])
    parser.add_argument("--min_tokens", help="Minimum number of tokens per sentence", type=int, default=3)
    parser.add_argument("--max_tokens", help="Maximum number of tokens per sentence", type=int, default=50)
    parser.add_argument("--size_vocab", help="Size of vocabulary to create", type=int, default=50000)

    args = parser.parse_args()

    corpus = args.corpus
    vocab_file = args.vocab
    output_file = args.sentences
    lang = args.lang
    min_tokens = args.min_tokens
    max_tokens = args.max_tokens
    size_vocab = args.size_vocab

    # Let's tokenize the sentences using the French NLTK tool
    if lang == 'eu':
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')
        word_tokenizer = EuskalToken()
    else:
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        word_tokenizer = TreebankWordTokenizer()

    vocab, sentences = process_corpus(corpus, min_tokens, max_tokens, size_vocab, sentence_tokenizer,
                                      word_tokenizer)

    with open(vocab_file, 'w') as file:
        file.writelines("%s\n" % line for line in vocab)

    with open(output_file, 'w') as file:
        file.writelines("%s\n" % line for line in sentences)


if __name__ == "__main__":
    main()
