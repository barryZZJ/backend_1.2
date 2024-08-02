from PIL import Image
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

from const import MODEL

image_to_measure = "./data/data_to_measure/images/face.jpg"
def image_measure(image_to_measure):
    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        trust_remote_code=True,
        torch_dtype="auto",
        _attn_implementation="eager",
    )  # use _attn_implementation='eager' to disable flash attention, to use flash attention, use _attn_implementation='flash_attention_2'

    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    messages = [
        {
            "role": "user",
            # "content": "<|image_1|>\nDoes the image contains any privacy information? (only answer yes or no)",
            "content": "<|image_1|>\nEstimate the probability that there is privacy information in this picture. (only answer the probability float number)",
        },
    ]

    print(image_to_measure)
    image = Image.open(image_to_measure)

    prompt = processor.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = processor(prompt, [image], return_tensors="pt").to("cuda:0")

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

    return float(response)

if __name__ == '__main__':
    print(image_measure(image_to_measure))
