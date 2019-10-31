from overrides import overrides

from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer, PretrainedBertIndexer
from allennlp.data.tokenizers.word_splitter import BertBasicWordSplitter
from allennlp.data.fields import Field, TextField, LabelField
from allennlp.data.instance import Instance

from allennlp.data.dataset_readers import DatasetReader

from allennlp.modules.elmo import batch_to_ids


@DatasetReader.register('probe-reader')
class ProbeReader(DatasetReader):
    def __init__(self, model) -> None:
        super().__init__()
        self._tokenizer = BertBasicWordSplitter(do_lower_case='uncased' in model)
        self._indexer = {'bert': PretrainedBertIndexer(model.replace('.tar.gz', '-vocab.txt'), do_lowercase='uncased' in model)}

    @overrides
    def _read(self, file_path: str):
        with open(file_path, 'r') as probe_file:
            for line in probe_file:
                sentence, label = line.rstrip("\n").split("\t")

                yield self.text_to_instance(sentence, label)

    @overrides
    def text_to_instance(self, sentence, label) -> Instance:
        fields = {}

        fields['sentence'] = TextField(self._tokenizer.split_words(sentence), self._indexer)
        fields['label'] = LabelField(label)

        return Instance(fields)
