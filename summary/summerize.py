import logging
import os

from anthropic import Anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = Anthropic()
MODEL_NAME = "claude-3-sonnet-20240229"
MAX_TOKENS = 4096


def read_transcripts(folder_path):
    transcripts = []
    try:
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".txt"):
                with open(os.path.join(folder_path, filename), "r") as file:
                    transcripts.append((filename, file.read()))
        logging.info(f"Read {len(transcripts)} transcripts from {folder_path}")
    except Exception as e:
        logging.error(f"Error reading transcripts: {e}")
        raise
    return transcripts


def summarize_lecture_part(text, part_number):

    prompt = f"""
    Summarize the following part {part_number} of a transcript. 
    Use bullet points and headers, as a student would in class notes. 
    Focus on key points, important concepts, and any examples mentioned:

    {text}

    Provide a concise summary of this section.
    Do not add any additional information that is not mentioned in this part.
    """

    try:
        response = client.messages.create(
            max_tokens=MAX_TOKENS,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
        )
        summary = response.content[0].text
        logging.info(f"Summarized part {part_number}")
        return summary
    except Exception as e:
        logging.error(f"Error summarizing lecture part {part_number}: {e}")
        raise


def rearrange_summary(full_summary):
    prompt = f"""
    Given the following raw summary of a full class lecture, please rearrange and refine it 
    to create a more coherent and well-structured summary. Maintain the use of bullets and headers, 
    but improve the overall organization and flow of information:

    {full_summary}

    Please provide a refined and well-structured summary of the full lecture."""

    try:
        response = client.messages.create(
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
        )
        refined_summary = response.content[0].text
        logging.info("Refined full summary")
        return refined_summary
    except Exception as e:
        logging.error("Error refining full summary: {e}")
        raise


def save_summary(filename, content, output_path):
    try:
        with open(output_path, "w") as file:
            file.write(content)
        logging.info(f"Saved summary to {output_path}")
    except Exception as e:
        logging.error(f"Error saving summary to {output_path}: {e}")
        raise


def summarize(input_path):
    transcripts = read_transcripts(input_path)
    summaries = []
    full_summary = ""

    for i, (filename, transcript) in enumerate(transcripts, 1):
        summary = summarize_lecture_part(transcript, i)
        summaries.append((filename, summary))
        full_summary += f"\n\nPart {i} Summary:\n{summary}"

    for filename, summary in summaries:
        output_filename = f"summary_{filename}"
        output_path = os.path.join(input_path, output_filename)
        save_summary(output_filename, summary, output_path)

    raw_summary_path = os.path.join(input_path, "raw_full_summary.txt")
    save_summary("raw_full_summary.txt", full_summary, raw_summary_path)

    refined_summary = rearrange_summary(full_summary)
    refined_summary_path = os.path.join(input_path, "refined_full_summary.txt")
    save_summary("refined_full_summary.txt", refined_summary, refined_summary_path)


if __name__ == "__main__":
    input_path = "lecture_06_05/transcriptions"
    summarize(input_path)
