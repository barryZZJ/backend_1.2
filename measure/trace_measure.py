from const import MODEL
from desensitize.location_desensitize import Coord
from global_utils import inMixzone

trace_privacy_component = "[(11.901378941584682  12.22942292176873  12.066038023121017  55.23030665591961  44.94763228076714  96.62325208596081  31.05192714969048  86.98415451179197  31.368460551036904  24.94897670685573)]"

trace_to_measure = "(11.901378941584682  12.22942292176873  12.066038023121017  55.23030665591961  44.94763228076714  96.62325208596081  31.05192714969048  86.98415451179197  31.368460551036904  24.94897670685573)"

def trace_measure(trace_to_measure: list[Coord], zone_coords: list[Coord], dist_thresh=1000) -> bool:
    return any(inMixzone(position_to_measure, zone_coords, dist_thresh) for position_to_measure in trace_to_measure)

    from global_vars import Global

    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model, processor = Global.load_measure_model(model_id)

    messages = [
        {
            "role": "user",
            "content": f"{trace_privacy_component} contains a list of positions. Tell me if the position {trace_to_measure} in the position list {trace_privacy_component}. (only answer yes or no)",
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
    return 'yes' in response.lower()

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

    trace = [(1.0, 2.0), (116.435842, 39.941626), (3.0, 4.0)]
    #[(116.435842, 39.941626), (116.353714, 39.939588), (116.435806, 39.908501), (116.356866, 39.907242)]
    print(trace_measure(trace, [(zone1_x, zone1_y), (zone2_x, zone2_y), (zone3_x, zone3_y), (zone4_x, zone4_y)]))