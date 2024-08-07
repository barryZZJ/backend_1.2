from PIL import Image
import cv2

from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

from const import MODEL

video_to_measure = "./data/data_to_measure/videos/text.avi"

def video_measure(video_to_measure):
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
            "content": "<|image_1|>\nEstimate the probability that there is privacy information in this image. (only answer the probability number)",
        },
    ]

    cap = cv2.VideoCapture(video_to_measure)

    counter = 0
    result = 0
    READ_FRAME_INTERVAL = 30

    while cap.isOpened():
        print(counter, '/', cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 读取一帧
        ret, frame = cap.read()
        if ret:
            counter += 1
            if (counter-1) % READ_FRAME_INTERVAL != 0:
                continue
            # 将opencv的图像格式转换为PIL的图像格式
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

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
        else:
            break

    # 释放视频文件
    cap.release()
    return result

if __name__ == '__main__':
    print(video_measure(video_to_measure))