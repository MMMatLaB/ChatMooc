from langchain_core.prompts import load_prompt
with open("few_shot.yaml", "r", encoding='utf-8') as f:
    with open("few_shot1.yaml", "w", encoding='utf-8') as output:
        output.write(f.read())
prompt = load_prompt("few_shot1.yaml")
print(prompt.format(adjective="funny", content="chickens"))