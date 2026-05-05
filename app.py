import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="PwD KYC Compliance System", layout="wide")

# ---------------- STATE ----------------
if "records" not in st.session_state:
    st.session_state.records = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["KYC Form", "Dashboard", "PwD Register"])

if st.sidebar.button("Reset Data"):
    st.session_state.records = []

# ================= KYC FORM =================
if page == "KYC Form":

    st.title("🧾 PwD KYC Onboarding")

    # BASIC DETAILS
    st.header("1️⃣ Basic Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Client Name")
        client_id = st.text_input("Client ID")
        pan = st.text_input("PAN")

    with col2:
        date = st.date_input("Onboarding Date", datetime.date.today())
        mode = st.selectbox("Mode", ["Online", "Assisted", "Offline"])

    # DISABILITY
    st.header("2️⃣ Disability")

    disability = st.selectbox(
        "Type of Disability",
        ["None", "Visual", "Hearing", "Speech", "Physical", "Cognitive", "Multiple"]
    )

    pwd_flag = "Yes" if disability != "None" else "No"

    # DEVIATION
    st.header("3️⃣ Deviation")

    thumb = st.checkbox("Unable to sign (Thumb Impression)")
    alt_consent = st.checkbox("Alternative Consent Used")
    guardian_used = st.checkbox("Guardian Involved")
    witness_required = st.checkbox("Witness Required")

    # VKYC
    st.header("4️⃣ KYC & VKYC")

    pan_verified = st.checkbox("PAN Verified")
    address_verified = st.checkbox("Address Verified")
    vkyc_done = st.checkbox("VKYC Completed")
    face_match = st.checkbox("Face Match Verified")
    geo_tag = st.checkbox("Geo-tag Captured")
    vkyc_id = st.text_input("VKYC Recording ID")

    # CONSENT
    st.header("5️⃣ Consent")

    consent = st.selectbox("Consent Type", ["Verbal", "Written", "Gesture"])
    declaration = st.checkbox("Declaration Explained")
    understood = st.checkbox("Client Understood")

    # DOCUMENTS
    st.header("6️⃣ Documentation")

    kyc_docs = st.checkbox("KYC Documents Uploaded")
    vkyc_record = st.checkbox("VKYC Recording Available")
    consent_proof = st.checkbox("Consent Proof Available")

    # GUARDIAN / WITNESS
    st.header("7️⃣ Guardian & Witness")

    guardian_name = st.text_input("Guardian Name")
    witness_name = st.text_input("Witness Name")

    # RISK
    st.header("8️⃣ Risk")

    risk = st.selectbox("Risk Observed", ["No", "Yes"])
    remarks = st.text_area("Remarks")

    # APPROVAL
    st.header("9️⃣ Approval")

    approval = st.selectbox(
        "Final Decision",
        ["Approved", "Approved with Conditions", "Rejected"]
    )

    approver = st.text_input("Approved By")

    # ANNEXURE DECLARATION
    st.header("📜 Declaration")

    st.info("The client has been onboarded through an inclusive process with appropriate accommodations provided as per regulatory requirements, and informed consent has been duly obtained and recorded.")

    # SUBMIT
    if st.button("Submit KYC"):

        record = {
            "Client Name": name,
            "Client ID": client_id,
            "PAN": pan,
            "Date": str(date),
            "Mode": mode,
            "Disability": disability,
            "PwD Flag": pwd_flag,
            "Consent": consent,
            "Declaration": declaration,
            "Understood": understood,
            "KYC Docs": kyc_docs,
            "VKYC Recording": vkyc_record,
            "Consent Proof": consent_proof,
            "Guardian Used": guardian_used,
            "Witness Required": witness_required,
            "Guardian Name": guardian_name,
            "Witness Name": witness_name,
            "VKYC Done": vkyc_done,
            "VKYC ID": vkyc_id,
            "Risk": risk,
            "Remarks": remarks,
            "Approval": approval,
            "Approved By": approver
        }

        st.session_state.records.append(record)
        st.success("KYC Submitted Successfully")

# ================= DASHBOARD =================
elif page == "Dashboard":

    st.title("📊 Compliance Dashboard")

    if len(st.session_state.records) == 0:
        st.info("No records available")

    else:
        df = pd.DataFrame(st.session_state.records).fillna("")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Clients", len(df))
        col2.metric("PwD Cases", len(df[df["PwD Flag"] == "Yes"]))
        col3.metric("VKYC Completed", len(df[df["VKYC Done"] == True]))
        col4.metric("Approved", len(df[df["Approval"] == "Approved"]))

        st.divider()

        st.subheader("All Cases")
        st.dataframe(df, use_container_width=True)

        st.subheader("⚠️ Exception Cases")

        exception_df = df[
            (df["Guardian Used"] == True) |
            (df["Witness Required"] == True) |
            (df["Consent"] == "Gesture")
        ]

        if len(exception_df) > 0:
            st.error("Requires Compliance Review")
            st.dataframe(exception_df)
        else:
            st.success("No exception cases")

# ================= REGISTER =================
elif page == "PwD Register":

    st.title("📋 PwD Onboarding Register (Annexure A)")

    if len(st.session_state.records) == 0:
        st.warning("No data available")

    else:
        df = pd.DataFrame(st.session_state.records)

        register = df[[
            "Client Name",
            "Client ID",
            "Disability",
            "Mode",
            "Consent",
            "Witness Required",
            "Guardian Used",
            "Remarks",
            "Approved By"
        ]]

        st.dataframe(register, use_container_width=True)