#!/usr/bin/env python

# Author: Steven Dang stevencdang.com

import nltk
from nltk.corpus import wordnet as wn
import numpy as np
from file_manager import read_data


def cosine(doc1, doc2, doc_topic_weights):
    weights1 = doc_topic_weights[doc1]
    weights2 = doc_topic_weights[doc2]
    dotProduct = np.dot(weights1, weights2)
    mag1 = np.sqrt(sum([np.square(weight) for weight in weights1]))
    mag2 = np.sqrt(sum([np.square(weight) for weight in weights2]))
    if mag1 and mag2:
        return dotProduct / (mag1 * mag2)
    else:
        return 0.0


def get_wordnet_pos(treebank_tag):
    """
    helper method to convert treebank tags
    into wordnet pos tags for query expansion
    """
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return ''


def expand_text(pos_tokens):
    """
    interface with wordnet to recursively add
    all synonyms and hypernyms for each token in input list of token-posTag tuples
    return expanded list of tokens that includes synonyms and hypernyms
    """

    # first expand with synonyms
    synonyms = set()
    for item in pos_tokens:
        synsets = wn.synsets(item[0], get_wordnet_pos(item[1]))
        for synset in synsets:
            synonyms.add(synset)

    # start making the list of tokens to be output
    # initialize with lemmas of the synonyms
    bowTokens = set([t[0] for t in pos_tokens])
    for synonym in synonyms:
        for lemma in synonym.lemmas():
            bowTokens.add(lemma.name())

    # now recursively add hypernyms
    nextStack = set(synonyms)  # initialize stack
    while(len(nextStack)):

        currentStack = set(nextStack)
        nextStack.clear()

        # get all hypernyms, put in nextStack
        for s in currentStack:
            for hypernym in s.hypernyms():
                nextStack.add(hypernym)

        # add lemmas from the current level of hypernyms to the master bag of tokens
        for hypernym in nextStack:
            for lemma in hypernym.lemmas():
                bowTokens.add(lemma.name())

    return sorted(list(bowTokens))


def get_stopwords():
    """
    Returns a list of stop words. Currently uses a list of words in
    a text file

    """
    return read_data("englishstopwords-jc.txt")


def bag_of_words(ideas, stopwords):
    """
    Initial processing of ideas for Mike Terri's Ideaforest algorithm

    """
    expandedText = []
    data = []
    for idea in ideas:
        # read the text
        text = idea['content'].encode('utf-8', 'ignore')

        # split into sentences (PunktSentenceTokenizer)
        sentences = nltk.sent_tokenize(text)

        # tokenize and pos tag words (TreeBank)
        pos_tokens = []
        for sentence in sentences:
            tokens = [token.lower() for token in nltk.word_tokenize(sentence)]  # tokenize
            pos_tokens += nltk.pos_tag(tokens)  # pos tag

        # remove stopwords
        pos_tokens = [t for t in pos_tokens if t[0] not in stopwords]

        # remove "words" with no letters in them!
        pos_tokens = [t for t in pos_tokens if any(c.isalpha() for c in t[0])]

        # query expansion
        expandedTokens = expand_text(pos_tokens)

        # add the enriched bag of words as value to current d
        expandedText.append(expandedTokens)
        data.append(idea)

    return data, expandedText
