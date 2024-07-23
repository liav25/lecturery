# Lectury - Lecture Summerizing

## Overview

This project is an automated system for processing, transcribing, and summarizing video lectures. It's designed to streamline the workflow of handling educational content, making it easier for educators and students to manage and review lecture materials.

## Key Features

- **Video Download**: Automatically downloads lecture videos from provided URLs.
- **Video Processing**: Segments videos into manageable chunks for efficient processing.
- **Transcription**: Utilizes OpenAI's Whisper model to generate accurate transcriptions of lecture content.
- **Summarization**: Employs Anthropic's Claude model to create concise summaries of lecture transcripts.
- **File Management**: Organizes processed files and cleans up unnecessary data to maintain a tidy workspace.

## Important: API Key Requirements

To use this project, you must have valid API keys for:

1. **OpenAI**: Required for the Whisper transcription model.
2. **Anthropic**: Required for the Claude summarization model.

Ensure you have obtained these API keys before attempting to run the project. You will need to set them as environment variables or configure them in the project settings.

## Components

1. **File Downloader**: Downloads lecture videos from specified URLs.
2. **Video Processor**: Segments videos and manages the transcription process.
3. **Transcriber**: Converts speech to text using OpenAI's Whisper model.
4. **Summarizer**: Generates summaries of transcribed content using Anthropic's Claude model.
5. **Transcript Reader**: Reads and processes transcription files.
6. **Summary Saver**: Saves both raw and refined summaries.

## Usage

The system processes lectures defined in a JSON file (`lectures.json`). Each lecture entry should include:

- Name
- Video URL
- Start time
- End time
- Language (optional, defaults to English)

To process lectures:

1. Ensure all dependencies are installed.
2. Set up your API keys for OpenAI and Anthropic.
3. Prepare your `lectures.json` file with the necessary lecture information.
4. Run `python process_lectures.py`

The system will then:
- Download each lecture video
- Process and transcribe the video
- Generate summaries
- Save transcriptions and summaries
- Clean up unnecessary files

## Project Structure

- `process_lectures.py`: Main script to process multiple lectures from JSON input.
- `process_lecture.py`: Core functionality for processing a single lecture.
- `download/`: Contains classes for file downloading.
- `transcribe/`: Houses video processing and transcription classes.
- `summary/`: Includes summarization and summary management classes.

## Requirements

- Python 3.7+
- OpenAI API key (for Whisper transcription)
- Anthropic API key (for Claude summarization)
- Additional dependencies listed in `requirements.txt`

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up API keys for OpenAI and Anthropic as environment variables: