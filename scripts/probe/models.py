import torch
from torch import nn

from allennlp.modules.token_embedders import TokenEmbedder
from allennlp.modules.feedforward import FeedForward
from allennlp.modules.elmo import Elmo, batch_to_ids, _ElmoBiLm
from allennlp.data.vocabulary import Vocabulary
from allennlp.training.metrics import CategoricalAccuracy

from allennlp.models import Model

from elmo_layers import ElmoLayers

@Model.register('probe')
class Probe(Model):
    def __init__(self, vocab, bert):
        super().__init__(vocab)

        self._bert = bert
        self._vocab = vocab
        self._clf = FeedForward(768, 2, [50, self._vocab.get_vocab_size('labels')], nn.Sigmoid())

        self._crit = nn.CrossEntropyLoss()
        self._acc = CategoricalAccuracy()

    def forward(self, sentence, label):
        output = {}

        with torch.no_grad():
            encoded_sentence = self._bert(sentence['bert'])
            bert_cls = encoded_sentence[:,0,:]

        clf = self._clf(bert_cls)

        output['loss'] = self._crit(clf, label)
        self._acc(clf, label)

        return output

    def get_metrics(self, reset=False):
        if not self.training:
            return {'acc': self._acc.get_metric(reset)}
        else:
            return {} 
        
