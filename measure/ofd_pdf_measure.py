import tqdm
from PIL import Image
import cv2

from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

import tempfile
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)

from const import MODEL

pdf_to_measure = "./data/data_to_measure/ofd_pdf/ori_pdf.pdf"

def pdf_measure(pdf_to_measure):

    ori_pdf_content = convert_from_path(pdf_to_measure)

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
            "content": "<|image_1|>\nEstimate the probability that there is privacy information in this image. (only answer the probability float number)",
        },
    ]

    counter = 0

    result = 0

    for image in tqdm.tqdm(ori_pdf_content):
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
    print(pdf_measure(pdf_to_measure))