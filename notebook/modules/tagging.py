# Required imports
import torch
import numpy as np
import pandas as pd
import pickle
from torch.nn import Linear, Embedding, RNN, GRU, LSTM
from torch.nn import Sigmoid, LogSoftmax, Softmax
from torch.optim import SGD
from torch.nn import BCELoss, NLLLoss, CrossEntropyLoss
from string import punctuation
import itertools
from tqdm import tqdm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

class pos_tagger(torch.nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, batch_size):
        super(pos_tagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.embedding = Embedding(num_embeddings=vocab_size, 
                                   embedding_dim=embedding_dim)
        self.rnn = LSTM(input_size=embedding_dim, 
                       hidden_size=hidden_dim)
        self.linear = Linear(hidden_dim, output_dim)
        self.batch_size = batch_size
        self.softmax = LogSoftmax(dim=2)
        self.hidden = self.init_hidden()
                
    def forward(self, x):
        e = self.embedding(x)
        e = e.view(len(x), self.batch_size, -1)
        out, self.hidden = self.rnn(e, self.hidden)
        output = self.linear(out)
        so = self.softmax(output).squeeze(1)
        return so
                  
    def init_hidden(self):
        h0 = torch.autograd.Variable(torch.zeros(1, self.batch_size, self.hidden_dim))
        c0 = torch.autograd.Variable(torch.zeros(1, self.batch_size, self.hidden_dim))
        return (h0, c0)