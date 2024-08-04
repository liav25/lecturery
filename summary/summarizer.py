import logging
import json

from abc import ABC, abstractmethod

from anthropic import Anthropic

PROMPTS_FILE = "summary/summary_prompts.json"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_prompts(language):
    with open(PROMPTS_FILE, "r", encoding="utf-8") as file:
        prompts = json.load(file)
    lang_prompt = prompts.get(language, prompts["en"])
    return lang_prompt


class Summarizer(ABC):
    @abstractmethod
    def summarize_lecture_part(self, text, part_number):
        pass

    @abstractmethod
    def rearrange_summary(self, full_summary):
        pass


class AnthropicSummarizer(Summarizer):
    def __init__(self, model_name, max_tokens=4096, language="en"):
        self.client = Anthropic()
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.prompts = load_prompts(language)

    def summarize_lecture_part(self, text, part_number):
        prompt = self.prompts["summarize_lecture_part_prompt"].format(
            text=text, part_number=part_number
        )

        try:
            response = self.client.messages.create(
                max_tokens=self.max_tokens,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            summary = response.content[0].text
            logging.info(f"Summarized part {part_number}")
            return summary
        except Exception as e:
            logging.error(f"Error summarizing lecture part {part_number}: {e}")
            raise

    def rearrange_summary(self, full_summary):
        prompt = self.prompts["rearrange_summary_prompt"].format(
            full_summary=full_summary
        )
        try:
            response = self.client.messages.create(
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            refined_summary = response.content[0].text
            logging.info("Refined full summary")
            return refined_summary
        except Exception as e:
            logging.error(f"Error refining full summary: {e}")
            raise
