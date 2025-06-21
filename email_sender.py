from os import path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from secretKey import SENDER_ADDRESS, SENDER_PASSWORD


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


if __name__ == "__main__":
   client_email = "ragibyasar11314@gmail.com"
   client_name = "Ragib Boss"
   file_path_list = ["Templates/proposal_template.pptx", "Templates/agreement_template.docx"]
   send_email_to_client(client_email, client_name, file_path_list)