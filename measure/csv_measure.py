from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

from const import MODEL

csv_to_measure = "./data/data_to_measure/csv/ori_csv.csv"

def csv_measure(csv_to_measure):

    with open(csv_to_measure, "r") as f:
        ori_csv = f.read()

    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        trust_remote_code=True,
        torch_dtype="auto",
        _attn_implementation="eager",
    )  # use _attn_implementation='eager' to disable flash attention

    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    messages = [
        {
            "role": "user",
            # "content": f"{ori_csv} \n Does the text contains any privacy information? (only answer yes or no)",
            "content": f"{ori_csv} \n Estimate the probability that there is privacy information in this text. (only answer the probability float number)",
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

    return float(response)

if __name__ == '__main__':
    print(csv_measure(csv_to_measure))