import streamlit as st
import openai
from dotenv import load_dotenv
import os
import json
import difflib

differ = difflib.Differ()

categories = """
1. Grammar and Syntax Errors:
    - Subject-Verb Agreement
    - Pronoun Agreement
    - Verb Tense
    - Run-on Sentences
    - Sentence Fragments
    - Misplaced Modifiers
    - Parallelism
    - Comma Splices
    - Dangling Participles
    - Agreement in Number
    - Apostrophe Misuse
2. Punctuation Errors:
    - Misplaced Commas
    - Missing Commas
    - Incorrect Use of Semicolons
    - Misused Colons
    - Overuse of Dashes
    - Improper Use of Hyphens
    - Inconsistent Quotation Marks
    - Ellipsis Errors
3. Spelling and Word Choice Errors:
    - Misspelled Words
    - Homophones Confusion (e.g., their/there/they're)
    - Word Usage Errors (e.g., affect/effect)
    - Redundancy
    - Jargon or Cliché Use
    - Inappropriate Colloquial Language
    - Ambiguous Words or Phrases
    - Wordiness
4. Capitalization Errors:
    - Incorrect Capitalization of Proper Nouns
    - Overuse of Capital Letters
    - Capitalization of Common Nouns
5. Sentence Structure Errors:
    - Lack of Sentence Variety
    - Awkward Sentence Construction
    - Lack of Clarity in Sentence Structure
    - Overly Complex Sentences
6. Paragraph and Organization Errors:
    - Lack of Clear Transitions
    - Inconsistent Organization
    - Off-Topic or Irrelevant Information
    - Poor Paragraph Structure
7. Tone and Style Errors:
    - Inconsistent Tone
    - Lack of Conciseness
    - Lack of Politeness 
8. Cohesion and Coherence Errors:
    - Lack of Logical Flow
    - Repetition of Ideas
    - Inconsistent or Disjointed Argumentation
"""

example_output = """
{{
    "Grammar and Syntax Errors":{{
        "Subject-Verb Agreement":[
            {{ 
                original: "I'm exactly the same as you.",
                corrected: "I'm in the same situation as you."
            }}
        ]
        "Verb Tense":[
            {{ 
                original: "and build my career before start the business.",
                corrected: "and building my career before starting the business"
            }}
        ]
    ""
    }}
    "Punctuation Errors":{{
        "Missing Commas":[
            {{ 
                original: "Hi Amir I found your story on the website.",
                corrected: "Hi Amir, I found your story on the website."
            }}
        ]
    }}
}}
"""

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

correction = ""


def askGPT(input):
    prompt_correction = f"""
Improve the writing of input delimitted with ###.
Make sure to:

- Fix spelling and grammar
- Make sentences more clear and concise
- Split up run-on sentences
- Reduce repetition
- When replacing words, do not make them more complex or difficult than the original
- If the text contains quotes, repeat the text inside the quotes verbatim
- Do not change the meaning of the text
- Do not remove any markdown formatting in the text, like headers, bullets, or checkboxes
- Do not use overly formal language

Enclose your output in ```.

###{input}###
"""
    messages = [{"role": "user", "content": prompt_correction}]
    if input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        correction = response.choices[0].message["content"]
        correction = correction.replace("```", "")
        st.markdown(correction)
        # split input into lists of words to compare them word by word
        differences = list(differ.compare(input.split(), correction.split()))

        result = ""

        for idx in range(len(differences)):
            word = differences[idx]
            if word.startswith("  "):  # Unchanged words
                result += word[2:] + " "  # Add unchanged word
            elif word.startswith("- "):  # Removed words
                result += f"~~{word[2:]}~~ "  # Strikethrough for removed word
            elif word.startswith("+ "):  # Added words
                result += f"**{word[2:]}** "  # Bold for added word

        st.markdown(result, unsafe_allow_html=True)

        parseCorrection(result)


def parseCorrection(result):
    prompt_parse = f"""
You are a professional English writing tutor with 30 years of experience. You excel at providing constructive feedback on students' writing, and you have the ability to categorize their mistakes and archive them to identify recurring patterns.
You have already corrected the student's writing. Your task is to categorize the mistakes that the student have made from the document delimitted with ###.
First detect which parts of writing has corrected. 
Then, find which category the correction fits best.
Finally, Output the result in python dictionary format with primary and secondary categories for each correction. 

Allowed categories: {categories}

###{result}###
"""
    messages = [{"role": "user", "content": prompt_parse}]
    if input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        parse = json.loads(response.choices[0].message["content"])
        st.write(parse)


st.title("Your very own Enlgish Tutor")
st.subheader("Keep your mistakes systematically")
input = st.text_area(
    "Write on",
    value="""Hi Amir, I found your story on "MILA" website. I'm exactly the same as you. I came to Canada to start a company and now thinking of pursuing master's degree in MILA and build my career before start the business. I have few questions want to ask you. Can you spare some time for me?""",
    height=100,
)
st.button("Improve", on_click=askGPT(input))
