import os

# Root directory containing the lecture folders
ROOT_DIR = "data/transcriptions"
# Output directory for merged files (Downloads folder)
OUTPUT_DIR = os.path.expanduser("~/Downloads")


def merge_lecture_files(root_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all folders in the root directory
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        if os.path.isdir(folder_path):
            transcriptions_dir = os.path.join(folder_path, "transcriptions")
            # Check if the 'transcriptions' subfolder exists
            if os.path.isdir(transcriptions_dir):
                # Initialize a string to hold all file contents
                combined_content = ""
                # Iterate over all files in the 'transcriptions' subfolder
                for filename in os.listdir(transcriptions_dir):
                    if filename.startswith("output") and filename.endswith(".txt"):
                        file_path = os.path.join(transcriptions_dir, filename)
                        if os.path.isfile(file_path):
                            # Append the content of each file
                            with open(file_path, "r") as infile:
                                combined_content += f"\n--- File: {filename} ---\n"
                                combined_content += infile.read()
                                combined_content += "\n"  # Optional: Add a newline between file contents
                # Write all combined content to a single file in the output directory
                output_file = os.path.join(output_dir, f"{folder}_merged_transcript.txt")
                with open(output_file, "w") as outfile:
                    outfile.write(combined_content)
                print(f'Merged files for {folder} into "{output_file}".')


# Run the function
merge_lecture_files(ROOT_DIR, OUTPUT_DIR)
