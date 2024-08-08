import torch
import whisper
from imagebind.models import imagebind_model
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

from const import MODEL


def load_models():
    req = dict(
        measure='1',
        whisper='1',
        assess='1',
    )
    loaded = []
    if req.setdefault('measure', '1') == '1':
        Global.load_measure_model()
        loaded.append('measure')
    if req.setdefault('whisper', '1') == '1':
        Global.load_whisper_model()
        loaded.append('whisper')
    if req.setdefault('assess', '1') == '1':
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        Global.load_assess_model(device)
        loaded.append('assess')
    print(loaded)

class Global:
    _model_measure = None
    _processor_measure = None
    _model_assess = None
    _model_whisper = None
    @classmethod
    def load_measure_model(cls, model_id=f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"):
        # TODO 换成小模型，优化加载速度
        if cls._model_measure is not None:
            return cls._model_measure, cls._processor_measure
        print('loading measure model')
        cls._model_measure = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="cuda",
            trust_remote_code=True,
            torch_dtype="auto",
            _attn_implementation="eager",
        )  # use _attn_implementation='eager' to disable flash attention

        cls._processor_measure = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        return cls._model_measure, cls._processor_measure

    @classmethod
    def load_whisper_model(cls):
        if cls._model_whisper is not None:
            return cls._model_whisper
        print('loading whisper')
        cls._model_whisper = whisper.load_model("base")
        return cls._model_whisper

    @classmethod
    def load_assess_model(cls, device):
        if cls._model_assess is not None:
            return cls._model_assess
        print('loading assess model')
        cls._model_assess = imagebind_model.imagebind_huge(pretrained=True)
        cls._model_assess.eval()
        cls._model_assess.to(device)
        return cls._model_assess