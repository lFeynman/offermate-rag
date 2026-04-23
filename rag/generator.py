from pathlib import Path
import yaml
import os
from openai import OpenAI


MODEL_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "model.yaml"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "rag_answer.txt"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompt(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class QwenGenerator:
    def __init__(self):
        model_cfg = load_yaml(MODEL_CONFIG_PATH)
        api_key = os.getenv(model_cfg["api_key_env"])
        if not api_key:
            raise ValueError(f"环境变量 {model_cfg['api_key_env']} 未设置")

        self.client = OpenAI(
            api_key=api_key,
            base_url=model_cfg["base_url"]
        )
        self.model = model_cfg["generation_model"]
        self.system_prompt = load_prompt(PROMPT_PATH)

    def generate(self, query: str, contexts: list[dict]) -> str:
        context_text = "\n\n".join(
            [
                f"[资料{i+1}] 文件：{c['file_name']} | 页码：{c.get('page', None)}\n内容：{c['text']}"
                for i, c in enumerate(contexts)
            ]
        )

        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": f"问题：{query}\n\n参考资料：\n{context_text}"
            }
        ]

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        return resp.choices[0].message.content.strip()