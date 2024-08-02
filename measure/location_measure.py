from const import MODEL
from desensitize.location_desensitize import Coord
from desensitize.utils import inMixzone

position_privacy_component = "[(42.640089555202366, 67.35983164586906)]"

position_to_measure = "(42.640089555202366, 67.35983164586906)"


def location_measure(position_to_measure: Coord, zone_coords: list[Coord], dist_thresh: float=1000) -> float:
    return inMixzone(position_to_measure, zone_coords, dist_thresh)

    from transformers import AutoModelForCausalLM
    from transformers import AutoProcessor

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
            "content": f"{position_privacy_component} contains a list of positions. Tell me if the position {position_to_measure} in the position list {position_privacy_component}. (only answer yes or no)",
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
    return 1.0 if 'yes' in response.lower() else 0.0

if __name__ == '__main__':
    zone1_x = 116.435842
    zone1_y = 39.941626
    # 西直门
    zone2_x = 116.353714
    zone2_y = 39.939588
    # 建国门
    zone3_x = 116.435806
    zone3_y = 39.908501
    # 复兴门
    zone4_x = 116.356866
    zone4_y = 39.907242

    coord = (116.435842, 39.941626)

    print(location_measure(coord, [(zone1_x, zone1_y), (zone2_x, zone2_y), (zone3_x, zone3_y), (zone4_x, zone4_y)]))
