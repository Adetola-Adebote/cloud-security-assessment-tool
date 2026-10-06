import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SME Cloud Security Assessment Tool",
    page_icon="🔐",
    layout="wide"
)

# ---------------------------------------------------------
# RESPONSE OPTIONS AND SCORES
# ---------------------------------------------------------

OPTIONS = [
    "Select an answer",
    "Yes",
    "Partly",
    "Not sure",
    "No",
    "Not applicable"
]

RESPONSE_SCORES = {
    "Yes": 3,
    "Partly": 2,
    "Not sure": 1,
    "No": 0
}

# ---------------------------------------------------------
# ASSESSMENT QUESTIONS
# ---------------------------------------------------------

QUESTIONS = {

    "Identity and Access Management": [
        {
            "id": "IAM1",
            "question": "Is multi-factor authentication (MFA) enabled for important cloud accounts?",
            "why": "MFA reduces the risk of account compromise when passwords are stolen or guessed.",
            "action": "Enable MFA for important cloud accounts, especially administrator and privileged accounts.",
            "nist": "PR.AA — Identity Management, Authentication and Access Control",
            "csa": "IAM — Identity & Access Management"
        },
        {
            "id": "IAM2",
            "question": "Are users given only the cloud-system permissions they need to perform their work?",
            "why": "Limiting permissions reduces the potential impact of compromised or misused accounts.",
            "action": "Review user permissions and apply least-privilege access based on job responsibilities.",
            "nist": "PR.AA — Identity Management, Authentication and Access Control",
            "csa": "IAM — Identity & Access Management"
        },
        {
            "id": "IAM3",
            "question": "Are cloud access rights removed or updated when staff leave or change roles?",
            "why": "Old or unnecessary access rights can create avoidable security risks.",
            "action": "Establish a process for promptly removing or changing cloud access when employment or responsibilities change.",
            "nist": "PR.AA — Identity Management, Authentication and Access Control",
            "csa": "IAM — Identity & Access Management"
        }
    ],

    "Data Protection": [
        {
            "id": "DP1",
            "question": "Does the organisation know what sensitive or important information is stored in cloud services?",
            "why": "Organisations need to know where important information is stored before they can protect it appropriately.",
            "action": "Identify and document sensitive or business-critical information stored in cloud services.",
            "nist": "ID.AM — Asset Management; PR.DS — Data Security",
            "csa": "DSP — Data Security & Privacy Lifecycle Management"
        },
        {
            "id": "DP2",
            "question": "Is access to sensitive cloud-stored information restricted to authorised users?",
            "why": "Unnecessary access increases the risk of unauthorised disclosure or misuse.",
            "action": "Restrict sensitive information to authorised users and periodically review access permissions.",
            "nist": "PR.AA — Identity Management, Authentication and Access Control; PR.DS — Data Security",
            "csa": "IAM — Identity & Access Management; DSP — Data Security & Privacy Lifecycle Management"
        },
        {
            "id": "DP3",
            "question": "Is sensitive information appropriately protected or encrypted when stored and transmitted?",
            "why": "Appropriate protection and encryption reduce the risk of sensitive information being exposed.",
            "action": "Use appropriate encryption and data-protection controls for sensitive information at rest and in transit.",
            "nist": "PR.DS — Data Security",
            "csa": "CEK — Cryptography, Encryption & Key Management; DSP — Data Security & Privacy Lifecycle Management"
        }
    ],

    "Backup and Recovery": [
        {
            "id": "BR1",
            "question": "Is important cloud-based information backed up appropriately?",
            "why": "Backups help organisations recover from accidental deletion, cyber incidents, or service disruption.",
            "action": "Maintain appropriate backups of important cloud-based information.",
            "nist": "PR.IR — Technology Infrastructure Resilience",
            "csa": "BCR — Business Continuity Management & Operational Resilience"
        },
        {
            "id": "BR2",
            "question": "Are backups periodically tested to confirm that information can be restored?",
            "why": "A backup is only useful if information can be successfully recovered when needed.",
            "action": "Periodically test restoration procedures and document the results.",
            "nist": "PR.IR — Technology Infrastructure Resilience; ID.IM — Improvement",
            "csa": "BCR — Business Continuity Management & Operational Resilience"
        },
        {
            "id": "BR3",
            "question": "Is there a documented process for recovering important cloud services and information after disruption?",
            "why": "A documented recovery process supports a faster and more organised response to disruption.",
            "action": "Create and maintain a practical recovery process for important cloud services and information.",
            "nist": "RC.RP — Incident Recovery Plan Execution",
            "csa": "BCR — Business Continuity Management & Operational Resilience"
        }
    ],

    "Monitoring and Visibility": [
        {
            "id": "MV1",
            "question": "Does the organisation maintain an up-to-date understanding or inventory of the cloud services and accounts it uses?",
            "why": "Unknown or forgotten cloud services and accounts can create unmanaged security risks.",
            "action": "Maintain a simple inventory of cloud services, important accounts, and responsible owners.",
            "nist": "ID.AM — Asset Management",
            "csa": "IAM — Identity & Access Management; AIS — Application & Interface Security"
        },
        {
            "id": "MV2",
            "question": "Is security logging enabled for important cloud services where this capability is available?",
            "why": "Security logs can help identify suspicious activity and support investigation of incidents.",
            "action": "Enable appropriate security logging for important cloud services where available.",
            "nist": "DE.CM — Continuous Monitoring",
            "csa": "LOG — Logging & Monitoring"
        },
        {
            "id": "MV3",
            "question": "Are important cloud security alerts or logs reviewed regularly?",
            "why": "Collecting logs without reviewing relevant alerts can allow suspicious activity to go unnoticed.",
            "action": "Establish a practical routine for reviewing important security alerts and logs.",
            "nist": "DE.CM — Continuous Monitoring; DE.AE — Adverse Event Analysis",
            "csa": "LOG — Logging & Monitoring"
        }
    ],

    "Incident Response": [
        {
            "id": "IR1",
            "question": "Does the organisation have a documented process for responding to cloud-related cybersecurity incidents?",
            "why": "A documented process helps staff respond consistently and quickly when an incident occurs.",
            "action": "Create a simple incident-response process covering common cloud-related security incidents.",
            "nist": "RS.MA — Incident Management",
            "csa": "SEF — Security Incident Management, E-Discovery & Cloud Forensics"
        },
        {
            "id": "IR2",
            "question": "Are responsibilities for responding to cloud-related security incidents clearly assigned?",
            "why": "Clear responsibilities reduce confusion and delays during an incident.",
            "action": "Assign incident-response responsibilities and ensure relevant staff understand their roles.",
            "nist": "GV.RR — Roles, Responsibilities and Authorities; RS.MA — Incident Management",
            "csa": "SEF — Security Incident Management, E-Discovery & Cloud Forensics"
        },
        {
            "id": "IR3",
            "question": "Do staff know how and where to report suspected cloud-related security incidents?",
            "why": "Early reporting can help an organisation respond before an incident becomes more serious.",
            "action": "Provide staff with a clear and simple route for reporting suspected security incidents.",
            "nist": "RS.CO — Incident Response Reporting and Communication",
            "csa": "SEF — Security Incident Management, E-Discovery & Cloud Forensics"
        }
    ],

    "Governance and Cloud Responsibility": [
        {
            "id": "GC1",
            "question": "Is responsibility for cloud security clearly assigned within the organisation?",
            "why": "Unclear ownership can result in important security activities being overlooked.",
            "action": "Assign responsibility for overseeing cloud security and communicate that responsibility clearly.",
            "nist": "GV.RR — Roles, Responsibilities and Authorities",
            "csa": "GRC — Governance, Risk & Compliance"
        },
        {
            "id": "GC2",
            "question": "Does the organisation understand its security responsibilities compared with those of its cloud provider?",
            "why": "Cloud providers and customers have different responsibilities, and misunderstanding them can leave security gaps.",
            "action": "Review the shared-responsibility arrangements for important cloud services and document key organisational responsibilities.",
            "nist": "GV.RR — Roles, Responsibilities and Authorities; GV.SC — Cybersecurity Supply Chain Risk Management",
            "csa": "GRC — Governance, Risk & Compliance; STA — Supply Chain Management, Transparency & Accountability"
        },
        {
            "id": "GC3",
            "question": "Are cloud security practices reviewed periodically rather than only after a problem occurs?",
            "why": "Periodic review helps identify weaknesses before they contribute to an incident.",
            "action": "Schedule regular reviews of important cloud security practices and follow up identified improvements.",
            "nist": "GV.OV — Oversight; ID.IM — Improvement",
            "csa": "GRC — Governance, Risk & Compliance"
        }
    ],

    "Third-Party and Cloud Services": [
        {
            "id": "TP1",
            "question": "Are security and privacy considerations reviewed before adopting a new cloud service or provider?",
            "why": "Third-party cloud services can introduce risks that should be considered before adoption.",
            "action": "Include basic security and privacy checks when evaluating new cloud services or providers.",
            "nist": "GV.SC — Cybersecurity Supply Chain Risk Management",
            "csa": "STA — Supply Chain Management, Transparency & Accountability"
        },
        {
            "id": "TP2",
            "question": "Does the organisation consider how it would access or recover important information if a cloud provider became unavailable?",
            "why": "Dependence on a provider can disrupt business operations if the service becomes unavailable.",
            "action": "Identify critical provider dependencies and establish practical continuity or recovery arrangements.",
            "nist": "GV.SC — Cybersecurity Supply Chain Risk Management; PR.IR — Technology Infrastructure Resilience",
            "csa": "BCR — Business Continuity Management & Operational Resilience; STA — Supply Chain Management, Transparency & Accountability"
        },
        {
            "id": "TP3",
            "question": "Are important third-party cloud services periodically reviewed against the organisation's security needs?",
            "why": "A service that was suitable when adopted may no longer meet changing organisational or security needs.",
            "action": "Periodically review important third-party cloud services and their security arrangements.",
            "nist": "GV.SC — Cybersecurity Supply Chain Risk Management",
            "csa": "STA — Supply Chain Management, Transparency & Accountability"
        }
    ],

    "Security Awareness": [
        {
            "id": "SA1",
            "question": "Do staff receive guidance or training about phishing and credential theft?",
            "why": "Phishing and stolen credentials are common routes for attackers to gain access to cloud accounts.",
            "action": "Provide regular, practical guidance on recognising phishing attempts and protecting account credentials.",
            "nist": "PR.AT — Awareness and Training",
            "csa": "HRS — Human Resources Security"
        },
        {
            "id": "SA2",
            "question": "Do staff receive guidance on securely sharing information through cloud services?",
            "why": "Incorrect sharing settings can expose information to unintended people.",
            "action": "Provide clear guidance on secure cloud sharing and appropriate access settings.",
            "nist": "PR.AT — Awareness and Training; PR.DS — Data Security",
            "csa": "HRS — Human Resources Security; DSP — Data Security & Privacy Lifecycle Management"
        },
        {
            "id": "SA3",
            "question": "Are staff aware of their responsibilities for protecting cloud accounts and organisational information?",
            "why": "Staff behaviour plays an important role in maintaining cloud security.",
            "action": "Communicate clear staff responsibilities for cloud accounts, credentials, information, and security reporting.",
            "nist": "PR.AT — Awareness and Training; GV.RR — Roles, Responsibilities and Authorities",
            "csa": "HRS — Human Resources Security"
        }
    ]
}

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def calculate_domain_score(domain_questions, responses):
    obtained_score = 0
    maximum_score = 0

    for question in domain_questions:
        response = responses.get(question["id"])

        if response in RESPONSE_SCORES:
            obtained_score += RESPONSE_SCORES[response]
            maximum_score += 3

        elif response == "Not applicable":
            # Not applicable is deliberately excluded from both
            # the numerator and denominator.
            continue

    if maximum_score == 0:
        return None

    return (obtained_score / maximum_score) * 100


def concern_level(score):
    if score is None:
        return "Not assessed"
    elif score >= 75:
        return "Lower concern"
    elif score >= 50:
        return "Moderate concern"
    else:
        return "Higher concern"


def recommendation_priority(response):
    if response == "No":
        return "High"
    elif response in ["Partly", "Not sure"]:
        return "Medium"
    return None


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "context" not in st.session_state:
    st.session_state.context = {}

if "assessment_complete" not in st.session_state:
    st.session_state.assessment_complete = False


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("Cloud Security Assessment")

page = st.sidebar.radio(
    "Navigation",
    [
        "Welcome",
        "Organisation Context",
        "Security Assessment",
        "Results"
    ]
)


# ---------------------------------------------------------
# WELCOME PAGE
# ---------------------------------------------------------

if page == "Welcome":

    st.title("🔐 SME Cloud Security Assessment Tool")

    st.write(
        """
        This prototype is designed to help small and medium enterprises
        (SMEs) reflect on important cloud security practices and identify
        areas that may require further attention.
        """
    )

    st.info(
        """
        This is a questionnaire-based self-assessment tool. It does not
        directly scan cloud systems and does not require access to cloud
        accounts, passwords, API keys, secret keys, access tokens, or
        other credentials.
        """
    )

    st.subheader("Assessment areas")

    st.write(
        """
        The assessment covers eight areas:

        1. Identity and Access Management
        2. Data Protection
        3. Backup and Recovery
        4. Monitoring and Visibility
        5. Incident Response
        6. Governance and Cloud Responsibility
        7. Third-Party and Cloud Services
        8. Security Awareness
        """
    )

    st.subheader("Framework basis")

    st.write(
        """
        The assessment is informed by the **NIST Cybersecurity Framework
        (CSF) 2.0** and the **Cloud Security Alliance Cloud Controls
        Matrix (CCM) v4.1**.

        Framework mappings are included to provide traceability to
        recognised cybersecurity guidance. They do not mean that this
        prototype provides certification, verifies compliance, or
        represents a complete assessment of either framework.
        """
    )

    st.subheader("Important limitation")

    st.warning(
        """
        The results reflect the answers provided in this self-assessment.
        They do not prove that an organisation is secure and should not
        replace vulnerability scanning, penetration testing, formal
        security audits, compliance assessments, or professional
        cybersecurity advice.
        """
    )

    st.write(
        "Use the navigation menu on the left to begin with **Organisation Context**."
    )


# ---------------------------------------------------------
# ORGANISATION CONTEXT PAGE
# ---------------------------------------------------------

elif page == "Organisation Context":

    st.title("Organisation Context")

    st.write(
        """
        These questions provide basic context for interpreting the
        assessment. They are not included in the security score.
        """
    )

    size_options = [
        "Select an answer",
        "1–9 employees",
        "10–49 employees",
        "50–249 employees"
    ]

    cloud_use_options = [
        "Select an answer",
        "Software as a Service (SaaS)",
        "Cloud-hosted infrastructure or applications",
        "Both",
        "Not sure"
    ]

    platform_options = [
        "Select an answer",
        "Microsoft 365 / Azure",
        "AWS",
        "Google Cloud / Google Workspace",
        "Other",
        "Not sure"
    ]

    knowledge_options = [
        "Select an answer",
        "Limited",
        "Moderate",
        "Advanced"
    ]

    current_context = st.session_state.context

    c1_default = current_context.get("C1", "Select an answer")
    c2_default = current_context.get("C2", "Select an answer")
    c3_default = current_context.get("C3", "Select an answer")
    c4_default = current_context.get("C4", "Select an answer")

    c1 = st.selectbox(
        "C1. Organisation size",
        size_options,
        index=size_options.index(c1_default)
        if c1_default in size_options else 0
    )

    c2 = st.selectbox(
        "C2. Main use of cloud services",
        cloud_use_options,
        index=cloud_use_options.index(c2_default)
        if c2_default in cloud_use_options else 0
    )

    c3 = st.selectbox(
        "C3. Main cloud platform or service environment",
        platform_options,
        index=platform_options.index(c3_default)
        if c3_default in platform_options else 0
    )

    c4 = st.selectbox(
        "C4. Level of technical/cloud security knowledge",
        knowledge_options,
        index=knowledge_options.index(c4_default)
        if c4_default in knowledge_options else 0
    )

    if st.button("Save Organisation Context"):

        context_answers = [c1, c2, c3, c4]

        if "Select an answer" in context_answers:
            st.error("Please answer all organisation context questions.")
        else:
            st.session_state.context = {
                "C1": c1,
                "C2": c2,
                "C3": c3,
                "C4": c4
            }

            st.success(
                "Organisation context saved. Continue to Security Assessment."
            )


# ---------------------------------------------------------
# SECURITY ASSESSMENT PAGE
# ---------------------------------------------------------

elif page == "Security Assessment":

    st.title("Security Assessment")

    st.write(
        """
        Answer each question based on the organisation's current practice.

        **Response options**

        - **Yes** – the practice is in place.
        - **Partly** – the practice is only partly implemented.
        - **Not sure** – you do not know whether the practice is in place.
        - **No** – the practice is not currently in place.
        - **Not applicable** – the question does not apply to the organisation.
        """
    )

    with st.form("security_assessment_form"):

        form_responses = {}

        for domain, domain_questions in QUESTIONS.items():

            st.header(domain)

            for question in domain_questions:

                previous_answer = st.session_state.responses.get(
                    question["id"],
                    "Select an answer"
                )

                default_index = (
                    OPTIONS.index(previous_answer)
                    if previous_answer in OPTIONS
                    else 0
                )

                answer = st.selectbox(
                    f'{question["id"]}. {question["question"]}',
                    OPTIONS,
                    index=default_index,
                    key=f'answer_{question["id"]}'
                )

                form_responses[question["id"]] = answer

        submitted = st.form_submit_button("Complete Assessment")

        if submitted:

            unanswered = [
                question_id
                for question_id, answer in form_responses.items()
                if answer == "Select an answer"
            ]

            if unanswered:
                st.error(
                    "Please answer all assessment questions before completing the assessment."
                )
            else:
                st.session_state.responses = form_responses
                st.session_state.assessment_complete = True

                st.success(
                    "Assessment completed. Select Results from the navigation menu."
                )


# ---------------------------------------------------------
# RESULTS PAGE
# ---------------------------------------------------------

elif page == "Results":

    st.title("Assessment Results")

    if not st.session_state.assessment_complete:

        st.warning(
            "Complete the Security Assessment before viewing results."
        )

    else:

        responses = st.session_state.responses

        # -------------------------------------------------
        # ORGANISATION CONTEXT SUMMARY
        # -------------------------------------------------

        st.subheader("Organisation Context")

        if st.session_state.context:

            context = st.session_state.context

            st.write(
                f"**Organisation size:** {context.get('C1', 'Not provided')}"
            )
            st.write(
                f"**Main cloud use:** {context.get('C2', 'Not provided')}"
            )
            st.write(
                f"**Cloud platform/environment:** {context.get('C3', 'Not provided')}"
            )
            st.write(
                f"**Technical knowledge:** {context.get('C4', 'Not provided')}"
            )

        else:
            st.info("Organisation context was not provided.")

        # -------------------------------------------------
        # DOMAIN RESULTS
        # -------------------------------------------------

        st.subheader("Domain Results")

        domain_results = []

        for domain, domain_questions in QUESTIONS.items():

            score = calculate_domain_score(
                domain_questions,
                responses
            )

            classification = concern_level(score)

            if score is None:
                score_display = "Not assessed"
            else:
                score_display = f"{score:.1f}%"

            domain_results.append(
                {
                    "Security Domain": domain,
                    "Assessment Score": score_display,
                    "Classification": classification
                }
            )

        results_df = pd.DataFrame(domain_results)

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            """
            Scores indicate areas of relative concern based on responses
            to this prototype self-assessment. They are not validated
            measures of overall cybersecurity maturity or security.
            """
        )

        # -------------------------------------------------
        # PRIORITISED FINDINGS
        # -------------------------------------------------

        st.subheader("Prioritised Findings and Recommendations")

        findings = []

        for domain, domain_questions in QUESTIONS.items():

            for question in domain_questions:

                response = responses.get(question["id"])

                priority = recommendation_priority(response)

                if priority:

                    findings.append(
                        {
                            "domain": domain,
                            "id": question["id"],
                            "question": question["question"],
                            "response": response,
                            "priority": priority,
                            "why": question["why"],
                            "action": question["action"],
                            "nist": question["nist"],
                            "csa": question["csa"]
                        }
                    )

        priority_order = {
            "High": 0,
            "Medium": 1
        }

        findings.sort(
            key=lambda item: priority_order[item["priority"]]
        )

        high_count = sum(
            1 for item in findings
            if item["priority"] == "High"
        )

        medium_count = sum(
            1 for item in findings
            if item["priority"] == "Medium"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("High Priority Findings", high_count)

        with col2:
            st.metric("Medium Priority Findings", medium_count)

        if not findings:

            st.success(
                """
                No High or Medium Priority findings were generated from
                the responses provided. This does not certify that the
                organisation is secure.
                """
            )

        else:

            for finding in findings:

                if finding["priority"] == "High":
                    priority_icon = "🔴"
                else:
                    priority_icon = "🟠"

                with st.expander(
                    f'{priority_icon} {finding["priority"]} Priority — '
                    f'{finding["id"]}: {finding["domain"]}'
                ):

                    st.write(
                        f'**Assessment question:** {finding["question"]}'
                    )

                    st.write(
                        f'**Response:** {finding["response"]}'
                    )

                    st.write(
                        f'**Why this matters:** {finding["why"]}'
                    )

                    st.write(
                        f'**Recommended action:** {finding["action"]}'
                    )

                    st.markdown("**Guidance basis**")

                    st.write(
                        f'**NIST CSF 2.0:** {finding["nist"]}'
                    )

                    st.write(
                        f'**CSA CCM v4.1:** {finding["csa"]}'
                    )

                    st.caption(
                        """
                        This mapping provides traceability to recognised
                        cybersecurity guidance. It does not indicate
                        certification or demonstrate compliance with the
                        referenced framework.
                        """
                    )

        # -------------------------------------------------
        # INTERPRETATION
        # -------------------------------------------------

        st.subheader("How to Interpret the Results")

        st.write(
            """
            For each applicable question:

            - **Yes = 3 points**
            - **Partly = 2 points**
            - **Not sure = 1 point**
            - **No = 0 points**
            - **Not applicable = excluded from scoring**

            Each domain score is calculated as:

            **points obtained ÷ maximum applicable points × 100**
            """
        )

        st.write(
            """
            Prototype classification rules:

            - **75–100%: Lower concern**
            - **50–74%: Moderate concern**
            - **0–49%: Higher concern**
            """
        )

        st.warning(
            """
            These thresholds are prototype classification rules created
            for this assessment tool. They are not validated
            cybersecurity risk thresholds and should not be interpreted
            as a percentage measure of how secure an organisation is.
            """
        )

        # -------------------------------------------------
        # FRAMEWORK TRACEABILITY
        # -------------------------------------------------

        st.subheader("Framework Traceability")

        st.write(
            """
            Assessment questions and recommendations are conceptually
            aligned with relevant areas of the **NIST Cybersecurity
            Framework (CSF) 2.0** and the **Cloud Security Alliance
            Cloud Controls Matrix (CCM) v4.1**.

            The mappings are intended to make the basis of the
            assessment transparent. This lightweight prototype does not
            assess every requirement or control within either framework
            and does not provide certification or formal compliance
            assurance.
            """
        )

        # -------------------------------------------------
        # LIMITATIONS
        # -------------------------------------------------

        st.subheader("Limitations")

        st.write(
            """
            This tool is a questionnaire-based self-assessment aid.

            It:

            - does not directly inspect or scan cloud environments;
            - does not verify that responses are technically accurate;
            - does not provide certification;
            - does not demonstrate compliance with NIST CSF or CSA CCM;
            - does not replace vulnerability scanning;
            - does not replace penetration testing;
            - does not replace a formal security audit; and
            - does not replace professional cybersecurity assessment.
            """
        )

        st.info(
            """
            No passwords, API keys, secret keys, access tokens,
            credentials, or direct cloud-system access are required by
            this prototype.
            """
        )

        # -------------------------------------------------
        # REASSESSMENT
        # -------------------------------------------------

        st.subheader("Reassessment")

        st.write(
            """
            Organisations can repeat the assessment after implementing
            improvements and compare their responses over time. Any
            change in scores reflects changes in self-reported answers
            and should not be interpreted as independent verification
            of improved cybersecurity.
            """
        )
