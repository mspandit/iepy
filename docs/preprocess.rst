About the Pre-Process
=====================

The preprocessing adds the metadata that iepy needs to detect the relations, which includes:

    * Text tokenization and sentence splitting.
    * Text lemmatization
    * Part-Of-Speech (POS) tagging.
    * Named Entity Recognition (NER).
    * Gazettes resolution
    * Syntactic parsing.
    * TextSegments creation (internal IEPY text unit).

We're currently running all this steps (except the last one) using the `Stanford CoreNLP <http://nlp.stanford.edu/software/corenlp.shtml>`_ tools.
This runs in a all-in-one run, but every step can be :ref:`modified to use a custom version <customize>` that adjust your needs.


About the Tokenization and Sentence splitting
---------------------------------------------

The text of each Document is split on tokens and sentences, and that information is stored
on the document itself, preserving (and also storing) for each token the offset (in chars)
to the original document text.

The one used by default it's the one that the `Stanford CoreNLP <http://nlp.stanford.edu/software/corenlp.shtml>`_ provides.

Lemmatization
-------------

.. note::

    Lemmatization was added on the version 0.9.2, all instances that were created before that,
    need to run the preprocess script again. This will run only the lemmatization step.

The text runs through a step of lemmatization where each token gets a lemma. This is a canonical form of the word that
can be used in the classifier features or the rules core.


Part of speech tagging (POS)
----------------------------

Each token is augmented with metadata about its part of speech such as noun, verb,
adjective and other grammatical tags.
Along the token itself, this may used by the NER to detect an entity occurrence.
This information is also stored on the Document itself, together with the tokens.

The one used by default it's the one that the `Stanford CoreNLP <http://nlp.stanford.edu/software/corenlp.shtml>`_ provides.

Named Entity Recognition (NER)
------------------------------

To find a relation between entities one must first recognize these entities in the text.

As an result of NER, each document is added with information about all the found
Named Entities (together with which tokens are involved in each occurrence).

An automatic NER is used to find occurrences of an entity in the text.

The default pre-process uses the Stanford NER, check the Stanford CoreNLP's `documentation <http://nlp.stanford.edu/software/corenlp.shtml>`_
to find out which entity kinds are supported, but includes:

    * Location
    * Person
    * Organization
    * Date
    * Number
    * Time
    * Money
    * Percent

Others remarkable features of this NER (that are incorporated to the default pre-process) are:

    - pronoun resolution
    - simple co-reference resolution

This step can be customized to find entities of kinds defined by you, or anything else you may need.

Gazettes resolution
-------------------

In case you want to add named entity recognition by matching literals, iepy provides a system of gazettes.
This is a mapping of literals and entity kinds that will be run on top of the basic stanford NER.
With this, you'll be able to recognize entities out of the ones done by the stanford NER, or even correct
those that are incorrectly tagged.

:doc:`Learn more about here. <gazettes>`


Syntactic parsing
-----------------

.. note::

    Syntactic parsing was added on the version 0.9.3, all instances that were created before that,
    need to run the preprocess script again. This will run only the syntactic parsing step.

The sentences are parsed to works out the syntactic structure. Each sentence gets an structure tree
that is stored in `Penn Treebank notation <http://en.wikipedia.org/wiki/Treebank>`__. IEPY presents
this to the user using a `NLTK Tree object <http://www.nltk.org/howto/tree.html>`__.

By default the sentences are processed with the `Stanford Parser <http://nlp.stanford.edu/software/lex-parser.shtml>`__
provided within the `Stanford CoreNLP <http://nlp.stanford.edu/software/corenlp.shtml>`__.

For example, the syntactic parsing of the sentence ``Join the dark side, we have cookies`` would be:

::

    (ROOT
      (S
        (S
          (VP (VBN Join)
            (NP (DT the) (JJ dark) (NN side))))
        (, ,)
        (NP (PRP we))
        (VP (VBP have)
          (NP (NNS cookies)))))

About the Text Segmentation
---------------------------

IEPY works on a **text segment** (or simply **segment**) level, meaning that will
try to find if a relation is present within a segment of text. The
pre-process is the responsible for splitting the documents into segments.

The default pre-process uses a segmenter that creates for documents with the following criteria:

 * for each sentence on the document, if there are at least 2 Entity Occurrences in there


.. _customize:

How to customize
----------------

On your own IEPY instances, there's a file called ``preprocess.py`` located in the ``bin`` folder.
There you'll find that the default is simply run the Stanford preprocess, and later the segmenter.
This can be changed to run a sequence of steps defined by you

For example, take this pseudo-code to guide you:

.. code-block:: python

    pipeline = PreProcessPipeline([
        CustomTokenizer(),
        CustomSentencer(),
        CustomLemmatizer(),
        CustomPOSTagger(),
        CustomNER(),
        CustomSegmenter(),
    ], docs)
    pipeline.process_everything()


.. note::

    The steps can be functions or callable objects. We recommend objects because generally you'll
    want to do some load up of things on the `__init__` method to avoid loading everything over and over again.

Each one of those steps will be called with each one of the documents, meaning that every step will be called
with all the documents, after finishing with that the next step will be called with each one of the documents.
