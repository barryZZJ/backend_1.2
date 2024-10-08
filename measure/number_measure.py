number_privacy_component = ["100", '1000']

number_to_measure = "100"

def number_measure(num_to_measure: list, num_private) -> bool:
    return num_private in num_to_measure

    from global_vars import Global
    from const import MODEL

    model_id = f"{MODEL}/microsoft/Phi-3-vision-128k-instruct"

    model, processor = Global.load_measure_model(model_id)


    messages = [
        {
            "role": "user",
            "content": f"{num_to_measure} contains a list of numbers. Tell me if the number {num_private} in the list {num_to_measure}. (only answer yes or no)",
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
    return 'yes' in response.lower()


if __name__ == '__main__':
    print(number_measure(number_privacy_component, number_to_measure))