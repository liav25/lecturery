import logging
from abc import ABC, abstractmethod

from anthropic import Anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Summarizer(ABC):
    @abstractmethod
    def summarize_lecture_part(self, text, part_number):
        pass

    @abstractmethod
    def rearrange_summary(self, full_summary):
        pass


class AnthropicSummarizer(Summarizer):
    def __init__(self, model_name, max_tokens=4096):
        self.client = Anthropic()
        self.model_name = model_name
        self.max_tokens = max_tokens

    def summarize_lecture_part(self, text, part_number):
        prompt = f"""
        Summarize the following part {part_number} of a transcript. 
        Use bullet points and headers, as a student would in class notes. 
        Focus on key points, important concepts, and any examples mentioned:

        {text}

        Provide a concise summary of this section.
        Do not add any additional information that is not mentioned in this part.
        """
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
        prompt = f"""
        Given the following raw summary of a full class lecture, please rearrange and refine it 
        to create a more coherent and well-structured summary. Maintain the use of bullets and headers, 
        but improve the overall organization and flow of information:

        {full_summary}

        Please provide a refined and well-structured summary of the full lecture.
        """
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
