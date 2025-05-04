# ChatGPT-Code-Reviewer

This program utilizes OpenAI's GPT-4.1 API to send short Python code snippets formatted in a JSON file for revision and saves the formatted reviews into a text file.


ChatGPT will be given the the following prompt along with the python code snippet. 

"You are a code reviewer. Analyze the following Python code snippet and return:
    1. a brief quality summary
    2. Line-specific comments for any issues (only for the lines that require improvement)
    3. a quality rating: Good / Needs Improvement / Buggy"


### Requirements

- Python 3.x
- OpenAI API Key

## Setup
1. Switch into the ChatGPT-Code-Reviewer Directory
    ```bash
    cd ChatGPT-Code-Reviewer Directory

2. Install the required libaries
    ```bash
        pip3 install openai

3. Set your OpenAI API key as an environment variable from the terminal
    export OpenAI_API_Key="your-api-key"

4. Create a JSON file with code snippets to be reviewed. Sample formatting can be found in the sampleSnippets.json file

### Running the Program

1. run the script
    python3 reviewer.py

2. When prompted enter the name of the JSON file ex. sampleSnippets.json

3. All reviews will be saved into a uniquely named text file e.g review_output_1.txt