import yaml
import openai
from prompt import prompt_template
import json

config = yaml.load(open("./config.yml", "r", encoding="utf-8"), Loader=yaml.FullLoader)
print(config)
import openai

openai.api_base = "https://api.nextweb.fun/openai/v1"
openai.api_key = "ak-oZx7qxNb5bJ3OEDO5grJhy3e6MpjUoS52uqyT9kU7rYd5Zrn"


def load_template_qas():
    template_qas = []
    with open("./data/template_qas.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                template_qas.append(line)
    return template_qas


def generate(epoch):
    qas = load_template_qas()
    data = []
    for e in range(epoch):
        for qa in qas:
            prompt = prompt_template.format(
                name="HairChat",
                company="Sinovel",
                version="v1.0",
                date="2023-08-30",
                description="我是一个头发知识百科全书，同时我也是一个人工智能，我不是样样精通，但特别了解头发。",
                ability="我能够回答您关于头发的任何问题，如果您想了解头发的知识，可以问我。如果你有头发方面的烦恼，也可以问我。",
                limitation="我不太擅长处理头发以外的问题，如果您有需求可以联系我们使用更通用的模型。同时，我也不是一个专业的医生，我的回答仅供参考。如果您有具体的治疗需求，请咨询专业医生。",
                author="Sinovel.AI",
                user_input=qa,
                bot_role="一个人工智能，专注头发知识问答",
            )

            try:
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                )
                sample = chat_completion.choices[0].message.content
                json_sample = eval(sample)
                data.append(json_sample)
                print(f"question: {qa}")
                print(f"answer: {sample}")
            except Exception as e:
                print(e)
                print(prompt)
                print(sample)
                input()
    with open("./data/self_cognition_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate(1)
