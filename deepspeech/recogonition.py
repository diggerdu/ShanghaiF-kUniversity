#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from timeit import default_timer as timer

import argparse
import sys
import scipy.io.wavfile as wav
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"

from deepspeech.model import Model

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_WEIGHT = 1.75

# The beta hyperparameter of the CTC decoder. Word insertion weight (penalty)
WORD_COUNT_WEIGHT = 1.00

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
VALID_WORD_COUNT_WEIGHT = 1.00


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9



class transciber(object):
    def __init__(self, modelPath, alphabet, lmPath, trie, numFeatures=26, numContext=9, beamWidth=500):
        print('Loading model from file %s' % modelPath, file=sys.stderr)
        model_load_start = timer()
        self.model = Model(modelPath, numFeatures, numContext, alphabet, beamWidth)
        self.model.enableDecoderWithLM(alphabet, lmPath, trie, LM_WEIGHT, WORD_COUNT_WEIGHT, VALID_WORD_COUNT_WEIGHT)
        model_load_end = timer() - model_load_start
        print('Loaded model in %0.3fs.' % (model_load_end), file=sys.stderr)

    def transcribe(self, audioPath):
        fs, audio = wav.read(audioPath)
        audio_length = len(audio) * ( 1 / 16000)
        label = self.model.stt(audio, fs)
        print(label)
        return label



if __name__ == '__main__':
    TR = transciber(modelPath="models/output_graph.pb",
                    alphabet='models/alphabet.txt',
                    lmPath='models/lm.binary',
                    trie='models/trie')
    import pickle
    candiDict = dict()
    persistFile = open('candiDict.pkl', 'wb')
    for dn in os.listdir('/home/diggerdu/dataset/tfsrc/train/audio'):
        candidateSet = set()
        for fn in os.listdir('/home/diggerdu/dataset/tfsrc/train/audio/{0}'.format(dn)):
            try:
                assert fn.endswith('.wav')
                label = TR.transcribe('/home/diggerdu/dataset/tfsrc/train/audio/{0}/{1}'.format(dn, fn))
                candidateSet.add(label)
            except:
                continue
        candiDict.update({dn:candidateSet})
        pickle.dump(candiDict, persistFile, True)
    persistFile.close()
    TR.transcribe('/home/diggerdu/dataset/Large/clean/p225/p225_003.wav')
