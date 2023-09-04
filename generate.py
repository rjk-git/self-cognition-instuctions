import json
import os
import time
import traceback

import openai
import yaml
from template.prompts import prompt_template
from template.questions import questions
from tqdm import tqdm

CONFIG = yaml.load(open("./config.yml", "r", encoding="utf-8"), Loader=yaml.FullLoader)

openai.api_base = CONFIG["openai"]["api_url"]
openai.api_key = CONFIG["openai"]["api_key"]


def main():
    samples = []
    max_samples = CONFIG["data"]["num_samples"]
    pbar = tqdm(total=max_samples, desc="Generating self cognition data")

    while True:
        exit_flag = False
        for question in questions:
            prompt = prompt_template.format(
                name=CONFIG["about"]["name"],
                company=CONFIG["about"]["company"],
                version=CONFIG["about"]["version"],
                date=CONFIG["about"]["date"],
                description=CONFIG["about"]["description"],
                ability=CONFIG["about"]["ability"],
                limitation=CONFIG["about"]["limitation"],
                author=CONFIG["about"]["author"],
                user_input=question,
                role=CONFIG["about"]["role"],
            )
            try:
                chat_completion = openai.ChatCompletion.create(
                    model=CONFIG["openai"]["model"],
                    messages=[{"role": "user", "content": prompt}],
                )
                sample = chat_completion.choices[0].message.content
                json_sample = eval(sample)
                samples.append(json_sample)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                exit_flag = True
                break

            pbar.update(1)

            if len(samples) >= CONFIG["data"]["num_samples"]:
                exit_flag = True
                break

        if exit_flag:
            break

    if not os.path.exists(CONFIG["data"]["output_dir"]):
        os.makedirs(CONFIG["data"]["output_dir"])
    local_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    num_samples = len(samples)
    output_filepath = os.path.join(
        CONFIG["data"]["output_dir"],
        f"{local_time}_{num_samples}_self_cognition_data.json",
    )

    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
