from transformers import AutoModelForCausalLM
from transformers import AutoProcessor
import whisper

import pyaudio
import wave
import tempfile
import subprocess

from const import MODEL

# 配置音频录制参数
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 44100  # 采样率
CHUNK = 1024  # 块大小
RECORD_SECONDS = 5  # 录制时长


def record_audio():
    audio = pyaudio.PyAudio()

    # 开始录制
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # 停止录制
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 创建一个临时的wav文件
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_wav.name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    return temp_wav.name


def convert_to_flac(wav_filename):
    # 创建一个临时的flac文件
    temp_flac = tempfile.NamedTemporaryFile(delete=False, suffix=".flac")

    # 使用ffmpeg将wav转换成flac
    subprocess.run(["ffmpeg", "-y", "-i", wav_filename, temp_flac.name])

    return temp_flac.name



def audio_stream_measure(wav_file_to_measure, keyword: str=''):
    '''输入文件路径'''
    flac_file = convert_to_flac(wav_file_to_measure)

    model = whisper.load_model("base")
    result = model.transcribe(flac_file)

    text_to_measure = result["text"]
    print(text_to_measure)
    print(keyword)

    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        trust_remote_code=True,
        torch_dtype="auto",
        _attn_implementation="eager",
    )  # use _attn_implementation='eager' to disable flash attention

    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    if keyword:
        messages = [
            {
                "role": "user",
                "content": f"Is there any form of the word \"{keyword}\" contained in the following text (only answer yes or no):\n{text_to_measure}",
            },
        ]
    else:
        messages = [
            {
                "role": "user",
                "content": f"{text_to_measure} \n Estimate the probability that there is privacy information in this text. (only answer the probability float number)",
            },
        ]

    prompt = processor.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = processor(prompt, return_tensors="pt").to("cuda:0")

    generation_args = {
        "max_new_tokens": 500,
        "temperature": 0.0,
        "do_sample": False,
    }

    generate_ids = model.generate(
        **inputs, eos_token_id=processor.tokenizer.eos_token_id, **generation_args
    )

    # remove input tokens
    generate_ids = generate_ids[:, inputs["input_ids"].shape[1] :]
    response = processor.batch_decode(
        generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]

    # print("measurement results -> ", response)

    if keyword:
        return 1.0 if 'yes' in response.lower() else 0.0
    return float(response)

if __name__ == '__main__':
    wav_file = record_audio()
    # print(f"Saved FLAC file: {flac_file}")