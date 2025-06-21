import base64
import json
import re
import streamlit as st
from os import makedirs, path
from google import genai
from secretKey import GEMINI_API

client = genai.Client(api_key=GEMINI_API)
model = "gemini-2.0-flash"


@st.cache_data
def generate_proposal(client_name, problem, solution, project_scope, starting_date, timeline, budget):
    prompt = f"""
    You are a highly recognized business, which provides valuable products or services, 
    operates ethically, and demonstrates a commitment to its stakeholders, including 
    employees and customers, also adaptable, scalable, and focused on long-term sustainability, 
    not just short-term profits. Your company name is - Orvyn.
    Your task is to generate a sophisticated, structured & professional Business proposal to 
    clients in JSON format with the following keys, just return the JSON, nothing else should 
    be printed, also make it humanized, make every description SMALL enough to fit in a small
    textbox of a Powerpoint presentation, also make the title small:
    - proposalTitle
    - description (in short)
    - oneParagraphProblemStatement
    - solutionHeadingOne
    - solutionDescriptionOne (in one-two lines)
    - solutionHeadingTwo
    - solutionDescriptionTwo (in one-two lines)
    - solutionHeadingThree
    - solutionDescriptionThree (in one-two lines)
    - shortScopeTitleOne
    - shortScopeDescriptionOne
    - shortScopeTitleTwo
    - shortScopeDescriptionTwo
    - shortScopeTitleThree
    - shortScopeDescriptionThree
    - milestoneDayOne (in "MMM DD, YYYY" format)
    - milestoneDescriptionOne
    - milestoneDayTwo (in "MMM DD, YYYY" format)
    - milestoneDescriptionTwo
    - milestoneDayThree (in "MMM DD, YYYY" format)
    - milestoneDescriptionThree
    - milestoneDayFour
    - milestoneDescriptionFour
    - cost (half amount, with currency, eg: $1500)
    - legal_agreement_text (make it a sophisticated and professional, 
                            and also comprehensive, in 150 words)
    - your_company_name
    - client_name
    - invoice_details (in BOM format, EXACTLY the format be like below:
                       "invoice_details": 
                            [{{"item": "", "quantity": "", 
                              "unit_cost": "", "total_cost": ""}},
                            {{"item": "", "quantity": "", 
                              "unit_cost": "", "total_cost": ""}},] )

    Input:
     - Client: {client_name}
     - Problem: {problem}
     - Solution: {solution}
     - Scope: {project_scope}
     - Starting Date: {starting_date}
     - Timeline: {timeline}
     - Budget: {budget}
    """
    try:
        response = client.models.generate_content(
            model=model, contents=prompt)
        match = re.search(r'\{[\s\S]*\}', response.text)
        data = json.loads(match.group())
        return data

    except Exception as e:
        return str(e)


def get_file_path(uploaded_file):
    if uploaded_file is not None:
        file_path = path.join("temp_uploads", uploaded_file.name)
        makedirs("temp_uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path


@st.cache_data
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


if __name__ == "__main__":
    client_name = "SpiceNest Foods"
    problem = """
     Delivery delays and missing ingredient reports."""
    solution = """
     Simple dashboard for tracking and supplier coordination."""
    project_scope = """
     Fresh spices and herb supply chain visibility for their city vendors."""
    starting_date = "July 15, 2025"
    timeline = "3 weeks"
    budget = "$3000"

    replacements = generate_proposal(client_name, problem, solution,
                                     project_scope, starting_date, timeline, budget)
    print(replacements)
