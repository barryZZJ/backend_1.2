from const import MODEL
from global_vars import Global

# audio_to_measure = "./data/data_to_measure/audios/test.flac"
audio_to_measure = "../src/upload/test.flac"
keyword = "America"

def audio_measure(audio_to_measure, keyword: str=''):
    model = Global.load_whisper_model()
    result = model.transcribe(audio_to_measure)
    print(result["text"])
    print(keyword)

    text_to_measure = result["text"]

    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model, processor = Global.load_measure_model(model_id)

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

    if keyword:
        return 1.0 if 'yes' in response.lower() else 0.0
    return float(response)

if __name__ == '__main__':
    print(audio_measure(audio_to_measure, keyword))
    # print(audio_measure(audio_to_measure, 'profiling'))
