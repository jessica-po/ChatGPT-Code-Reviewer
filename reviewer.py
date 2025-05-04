from openai import OpenAI
import json
import os

#seeks the API key which you will set in the terminal prior to running the program (see README.md) 
APIkey = OpenAI(api_key=os.getenv("OpenAI_API_Key"))


# function to load code snippets from the JSON file 
# (should be in format 'id' and 'code')
# where id is a string with the code's name and the code contains the code to be reviewed
def load_code_snippets(path):
    with open(path, "r") as file:
        return json.load(file)
    
# Sends the code snippets as well as instructions for the review to ChatGPT as a prompt
# Note: I decided to add the ```python {code}``` enclosing as the AI responded better to the proper formatting in the prompt
def send_prompt(code_snippet):
    return f"""You are a code reviewer. Analyze the following Python code snippet and return:
    1. a brief quality summary
    2. Line-specific comments for any issues (only for the lines that require improvement)
    3. a quality rating: Good / Needs Improvement / Buggy

Code: 
``` python
{code_snippet} 
```\n
"""

# Sends the code snippet and prompt to ChatGPT and returns the review
def review_code(code_snippet):
    prompt = send_prompt(code_snippet)
    AIresponse = APIkey.chat.completions.create (
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    review_output = AIresponse.choices[0].message.content.strip()
    return f"{prompt}Review:\n\n{review_output}"

#creates a unique filename which is not present in the current directory. 
# Ex. if review_output_1.txt exists, it will choose the next available increment aka review_output_2.txt
def unique_output_file(base_name="review_output", extension=".txt"):
    i=1
    while True:
        fname = f"{base_name}_{i}{extension}"
        if not os.path.exists(fname):
            return fname
        i+=1

#Saves and nicely formats the reviews into a text file
def format_reviews(reviews, output_name):
    with open(output_name, "w") as file:
        for review in reviews:
            file.write(f"Code ID: {review['id']}\n\n")
            file.write(f"{review['review_full_text']}\n")
            file.write("-"*50+"\n\n") #seperator between code reviews

def main():
    #get user input for filename
    input_file = input("Enter the input JSON filename (e.g snippets.json): ")
    
    #check if file exists
    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found. Please double check the filename and try again")
        return
    
    output_file = unique_output_file()
    code_snippets = load_code_snippets(input_file)
    all_reviews = []

    for item in code_snippets:
        code_id = item.get("id")
        code = item.get("code")
        print(f"Revewing snippet '{code_id}'...")
        review = review_code(code)
        all_reviews.append({
            "id":code_id,
            "review_full_text": review
        })

    format_reviews(all_reviews, output_file)
    print(f"All reviews saved to {output_file}")

if __name__ == "__main__":
    main()

