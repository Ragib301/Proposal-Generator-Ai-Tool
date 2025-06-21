import streamlit as st
from utils import generate_proposal, set_background, get_file_path
from doc_utils import replace_text_pptx, export_agreement
from email_sender import send_email_to_client
from os import makedirs
import pandas as pd


st.set_page_config(page_title="Proposal Generator AI Tool", page_icon="📄")
st.title("Proposal Generator Ai Tool (Full Offline Suite)")
set_background('bg.jpg')


if 'processed' not in st.session_state:
    st.session_state.processed = False

    st.session_state.client_email = None
    st.session_state.client_name = None
    st.session_state.attachments = None

    st.session_state.pptx_path = None
    st.session_state.agreement_path = None
    st.session_state.invoice_path = None
    st.session_state.csv = None


proposal_uploader = st.file_uploader(
    "Upload Proposal Template (Make sure to put placeholders!)", type='pptx')
agreement_uploader = st.file_uploader(
    "Upload Legal Agreement Template (Make sure to put placeholders!)", type='docx')


with st.form("proposal_form"):
    client_name = st.text_input("Client Name")
    client_email = st.text_input("Client Email")
    problem = st.text_area("Problem Statement")
    solution = st.text_area("Solution")
    project_scope = st.text_area("Project Scope")
    starting_date = str(st.date_input("Starting Date", format="DD/MM/YYYY"))
    timeline = st.text_input("Timeline (e.g. 4 weeks, 2 months)")
    budget = st.text_input("Estimated Budget (e.g. $5,000)")
    submitted = st.form_submit_button("Generate Proposal")


if submitted:
    proposal_template = get_file_path(proposal_uploader)
    agreement_template = get_file_path(agreement_uploader)

    with st.spinner("Generating proposal, agreement, invoice, and preparing email..."):
        proposal_data = generate_proposal(client_name, problem, solution,
                                          project_scope, starting_date, timeline, budget)
        makedirs("Exported Docs", exist_ok=True)

        # Generate PPTX
        pptx_path = f"Exported Docs/{client_name}_Proposal.pptx"
        replace_text_pptx(proposal_data, proposal_template, pptx_path)

        # Generate Agreement DOCX
        agreement_path = f"Exported Docs/{client_name}_Agreement.docx"
        export_agreement(proposal_data, agreement_template, agreement_path)

        # Generate Invoice CSV
        invoice_path = f"Exported Docs/{client_name}_Invoice.csv"
        invoice_dict = proposal_data['invoice_details']
        invoice_items = pd.DataFrame(invoice_dict)

        invoice_items.to_csv(invoice_path, index=False)
        csv = invoice_items.to_csv(index=False).encode('utf-8')

        attachments = [pptx_path, agreement_path, invoice_path]

        st.session_state.client_email = client_email
        st.session_state.client_name = client_name
        st.session_state.attachments = attachments

        st.session_state.pptx_path = pptx_path
        st.session_state.agreement_path = agreement_path
        st.session_state.invoice_path = invoice_path
        st.session_state.invoice_items = invoice_items
        st.session_state.csv = csv

        st.session_state.processed = True

if st.session_state.processed:
    invoice_items = st.session_state.invoice_items
    st.subheader("Invoice in BOM Format")
    st.dataframe(invoice_items, use_container_width=True)

    client_email = st.session_state.client_email
    client_name = st.session_state.client_name
    attachments = st.session_state.attachments

    if st.button("Send in Email"):
        email_sent = send_email_to_client(
            client_email, client_name, attachments)
        if email_sent:
            st.success(f"Proposal, Legal Agreement, and Invoice sent to - {client_email}!")

    pptx_path = st.session_state.pptx_path
    agreement_path = st.session_state.agreement_path
    invoice_path = st.session_state.invoice_path
    csv = st.session_state.csv

    st.download_button("Download Proposal (PPTX)",
                       open(pptx_path, "rb"), file_name=pptx_path)
    st.download_button("Download Agreement (DOCX)",
                       open(agreement_path, "rb"), file_name=agreement_path)
    st.download_button("Download Invoice (CSV)", data=csv,
                       file_name=invoice_path, mime="text/csv")


st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("<center><small>Made with ❤️ by Ragib Yasar Rahman</small></center>",
            unsafe_allow_html=True)
