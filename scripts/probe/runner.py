import torch

from argparse import ArgumentParser

from allennlp.data.vocabulary import Vocabulary
from allennlp.modules.token_embedders import PretrainedBertEmbedder
from allennlp.training.trainer import Trainer
from allennlp.training.util import evaluate
from allennlp.data.iterators import BasicIterator
from allennlp.common.tqdm import Tqdm

from loader import ProbeReader
from models import Probe

def main():
    parser = ArgumentParser()
    parser.add_argument('--train', action='store')
    parser.add_argument('--val', action='store')
    parser.add_argument('--test', action='store')
    parser.add_argument('--model', action='store')
    parser.add_argument('--cuda', action='store', type=int)
    parser.add_argument('--logdir', action='store', default='experiments/models/bertie')
    args = parser.parse_args()

    reader = ProbeReader(args.model)
    train_dataset = reader.read(args.train)
    val_dataset = reader.read(args.val)
    test_dataset = reader.read(args.test)

    vocab = Vocabulary.from_instances(train_dataset + val_dataset + test_dataset)
   
    bert_embedder = PretrainedBertEmbedder(args.model) 
    model = Probe(vocab, bert_embedder)

    if args.cuda != -1:
        model = model.cuda(args.cuda)    

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    iterator = BasicIterator(batch_size=32)
    iterator.index_with(vocab)

    trainer = Trainer(model=model,
                      optimizer=optimizer,
                      iterator=iterator,
                      train_dataset=train_dataset,
                      validation_dataset=val_dataset,
                      patience=1,
                      num_epochs=1,
                      cuda_device=args.cuda)

    trainer.train()

    print(evaluate(model, test_dataset, iterator, args.cuda, batch_weight_key=None))

main()
