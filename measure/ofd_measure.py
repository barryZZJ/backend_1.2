import tqdm

from global_utils import ofd_to_img
from const import MODEL
from global_vars import Global


def ofd_measure(ofd_to_measure):

    ori_ofd_content = ofd_to_img(ofd_to_measure)

    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model, processor = Global.load_measure_model(model_id)

    messages = [
        {
            "role": "user",
            "content": "<|image_1|>\nEstimate the probability that there is privacy information in this image. (only answer the probability float number)",
        },
    ]

    counter = 0

    result = 0

    for image in tqdm.tqdm(ori_ofd_content, postfix='ofd_measure'):
        # 读取一帧

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

        # print("frame", counter, "measurement results -> ", response)
        result = max(result, float(response))
        counter += 1
    return result

if __name__ == '__main__':
    ofd_to_measure = "../src/upload/ori_ofd.ofd"
    print(ofd_measure(ofd_to_measure))