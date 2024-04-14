import tkinter as tk
from tkinter import filedialog
from PIL import Image
from tesserocr import PyTessBaseAPI
from github import Github
import os
import datetime
import time

def extract_text_and_save_to_github():
    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return  # User canceled selection

    # Extract text from the selected image
    column = Image.open(file_path)
    gray = column.convert('L')
    blackwhite = gray.point(lambda x: 0 if x < 230 else 255, '1')
    blackwhite.save("code_bw.jpg")

    with PyTessBaseAPI(path='C:/Users/ysra/PycharmProjects/pythonProject/tessdata', lang='eng') as api:
        api.SetImageFile('code_bw.jpg')
        extracted_text = api.GetUTF8Text()

        # Process and improve formatting
        formatted_text = ""
        lines = extracted_text.split('\n')
        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces
            line = line.replace('Question ', 'Question |', 1)
            if line:  # Skip empty lines
                line = line.replace('1outof', '1 out of')
                formatted_text += line + '\n'

        # Define the folder path within the repository


        # Get current date and time
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format the content to include a header with metadata
        formatted_text_with_header = f"Extracted Text\n\nDate and Time: {current_datetime}\n\n{formatted_text}"

        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_file_path = f'extracted_text_{timestamp}.txt'
        file_path_in_repo = f'text_files/extracted_text_{timestamp}.txt'

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(formatted_text)
        print(f"Extracted text saved to: {output_file_path}")

        github_token = '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'
        github_repo_name = 'canvas-screenshot-scraping'
        branch = 'testing'
        github_username = 'seclere'

        g = Github(github_token)
        repo = g.get_user().get_repo(github_repo_name)
        latest_commit = repo.get_branch(branch).commit
        latest_commit_sha = latest_commit.sha

        repo.create_file(file_path_in_repo, "Auto-updated extracted text", formatted_text_with_header, branch="testing")


        print("Text uploaded to GitHub.")

# GUI setup
root = tk.Tk()
root.title("Text Extraction and Upload")

button = tk.Button(root, text="Select Image and Extract Text", command=extract_text_and_save_to_github)
button.pack()

root.mainloop()