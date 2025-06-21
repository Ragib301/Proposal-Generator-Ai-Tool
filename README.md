![Screenshot (80)](https://github.com/user-attachments/assets/d471c109-c233-46c8-990b-604e0b60eda6)# Proposal-Generator-Ai-Tool
An automated AI-driven tool that generates Client-ready Proposals, Legal Agreements, and Invoices from simple user input — complete with one-click Email Delivery, all powered by Streamlit and Gemini API.

---

## 📌 What It Does

The Proposal Generator AI Tool simplifies the post-meeting hustle:

* Accepts simple Project Input via a Form
* Uses Gemini API to auto-generate:
  * A PowerPoint Proposal
  * A DOCX Legal Agreement
  * A CSV Invoice
* Displays the invoice in a clean Pandas DataFrame
* Allows download distinguishly or direct Email delivery of all generated documents

---

## ⚙️ Technologies Used

* `Streamlit`: GUI for form, display & downloads
* `Gemini API`: for proposal logic, text generation & structuring
* `python-pptx`, `python-docx`, `docx_replace`: for dynamic document generation
* `Pandas`: for invoice table and CSV export
* `smtplib`, `email.mime`: for email sending functionality
* `json`, `re`: for parsing and preprocessing Gemini API output

---

## 🧪 How It Works

1. **User fills in form fields:**
   * Client Name
   * Client Email
   * Problem, Solution, Scope
   * Start Date, Timeline, Budget
   * Uploads Proposal Template (.pptx) including placeholders
   * Uploads Legal Agreement Template (.docx) including placeholders

2. **On Submit:**
   * Data is sent to Gemini API for structured JSON output
   * JSON is cleaned using `json` and `re` modules
   * Text is injected into uploaded templates using Placeholder Replacement
   * Proposal, Legal Agreement and Invoice are generated

3. **Output:**
   * Proposal (.pptx), Legal Agreement (.docx) and Invoice (.csv)
   * Invoice also displayed as a dataframe in app
   * One-click button to send all docs to client via email

---

## 🚀 Features
* Plug-and-play templates (custom branding)
* Placeholder replacement in templates
* CSV + DataFrame rendering for invoices
* All-in-one email dispatch with attachments
* Easy and quick setup using Streamlit

---

## 📁 Folder Structure
```
Proposal-Generator-Ai-Tool
├── Templates
│   ├── proposal_template.pptx
│   └── agreement_template.docx
├── main.py
├── utils.py
├── doc_utils.py
├── email_sender.py
├── secretKey.py
├── bg.jpg
├── requirements.txt
└── README.md
```

---

## 🖼️ Screenshots
![Screenshot (72)](https://github.com/user-attachments/assets/134f3e45-1b3e-4117-99d0-c18501a1a928)
![Screenshot (75)](https://github.com/user-attachments/assets/631cbecf-7a61-4d67-aa27-a4d3553bdc1c)
![Screenshot (76)](https://github.com/user-attachments/assets/71f6fe95-4a10-42e9-92a9-e7a6763d2fdd)
![Screenshot (78)](https://github.com/user-attachments/assets/150e5ae9-b0a3-4f53-8be2-923b9857ae49)
![Screenshot (79)](https://github.com/user-attachments/assets/2ea25bc5-32c2-4b24-8817-a5222dd5c41e)
![Screenshot (80)](https://github.com/user-attachments/assets/a36e69e0-fb82-49ed-a427-967df093bfc4)
---

## 🔧 Setup

```bash
pip install -r requirements.txt
streamlit run main.py
```

---

## 🧩 Code Snippets

### Parsing Gemini API JSON Response
```python
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
```

### Replacing Placeholders in Template
```python
def replace_text_pptx(replacements, template_path, output_path):
    prs = Presentation(template_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        for key, value in replacements.items():
                            placeholder = f"$[{key}]"
                            if placeholder in run.text:
                                run.text = run.text.replace(
                                    placeholder, str(value))
    prs.save(output_path)
    return output_path


def export_agreement(replacements, template_path, output_path):
    doc = Document(template_path)
    docx_replace(doc, **replacements)
    doc.save(output_path)
```

### Sender function for Email to Client
```python
def send_email_to_client(recipient_email, client_name, file_path_list):
   subject = "Project Collaboration with ORVYN – Proposal, Agreement & Invoice Attached"
   body = f"""Dear {client_name},
I hope you're doing well. Please find attached the proposal for our upcoming collaboration, along with the legal agreement and invoice for your review. The proposal outlines the scope, deliverables, timeline, and budget as discussed.
If you have any questions, feel free to reach out. We’re excited about the opportunity to work with you and look forward to your feedback.

Attachments:
 1. Proposal Presentation (.pptx)
 2. Legal Agreement (.docx)
 3. Invoice (.csv)

Thank you for your time and consideration.

Warm regards,
Ragib Yasar Rahman
Co-founder, ORVYN
✉️ orvynsoul@gmail.com
🌐 https://orvyn.framer.website/
   """
   smtp_server = 'smtp.gmail.com'
   smtp_port = 465

   message = MIMEMultipart()
   message['Subject'] = subject
   message['From'] = SENDER_ADDRESS
   message['To'] = recipient_email
   body_part = MIMEText(body)
   message.attach(body_part)

   for file_path in file_path_list:
      file_name = path.basename(file_path)
      with open(file_path, 'rb') as file:
          message.attach(MIMEApplication(file.read(), Name=file_name))

   with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
       server.login(SENDER_ADDRESS, SENDER_PASSWORD)
       server.sendmail(SENDER_ADDRESS, recipient_email, message.as_string())

   return True
```
---
## 📄 License
* MIT License. Use freely with attribution.
---
> Built as a side-project with love, curiosity, and coffee ☕. Contributions welcome!
