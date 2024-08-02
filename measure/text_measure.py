from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

from const import MODEL

text_to_measure = "I went to the park and saw a dog."

def text_measure(text_to_measure, keyword: str=''):
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
                "content": f"Is the word \"{keyword}\" or any of its forms contained in the following text (only answer yes or no):\n{text_to_measure}",
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

    print("measurement results -> ", response)

    if keyword:
        return 1.0 if 'yes' in response.lower() else 0.0
    return float(response)

if __name__ == '__main__':
    # print(text_measure(text_to_measure))
    print(text_measure(text_to_measure, 'go'))
    # print(text_measure(text_to_measure, 'dog'))
