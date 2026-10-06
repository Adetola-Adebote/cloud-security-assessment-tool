import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SME Cloud Security Assessment Tool",
    page_icon="🔐",
    layout="wide"
)

# =========================================================
# RESPONSE OPTIONS AND SCORING
# =========================================================

OPTIONS = [
    "Select an answer",
    "Yes",
    "Partly",
    "No",
    "Not sure",
    "Not applicable"
]

RESPONSE_SCORES = {
    "Yes": 3,
    "Partly": 2,
    "Not sure": 1,
    "No": 0,
    "Not applicable": None
}

# =========================================================
# ASSESSMENT QUESTIONS
# =========================================================

DOMAINS = {
    "Identity and Access Management": [
        {
            "id": "IAM1",
            "question": "Is multi-factor authentication (MFA) enabled for accounts that access important cloud services?",
            "why": "Password compromise could allow unauthorised access to important cloud accounts.",
            "action": "Enable MFA for cloud accounts, prioritising privileged and administrator accounts."
        },
        {
            "id": "IAM2",
            "question": "Are users given only the cloud-system permissions they need to perform their work?",
            "why": "Excessive permissions can increase the impact of account compromise or inappropriate access.",
            "action": "Review user permissions and restrict access according to job responsibilities."
        },
        {
            "id": "IAM3",
            "question": "Are user accounts and access permissions promptly removed or updated when employees leave or change roles?",
            "why": "Unused or outdated accounts can provide unnecessary access to cloud systems.",
            "action": "Establish a process for promptly removing or changing access when staff leave or change roles."
        }
    ],

    "Data Protection": [
        {
            "id": "DP1",
            "question": "Does your organisation know what sensitive or important information is stored in its cloud services?",
            "why": "An organisation cannot adequately protect information if it does not know what sensitive data it holds.",
            "action": "Identify and document important or sensitive information stored in cloud services."
        },
        {
            "id": "DP2",
            "question": "Is access to sensitive cloud-stored information restricted to authorised users?",
            "why": "Unnecessary access increases the risk of accidental or unauthorised disclosure.",
            "action": "Review access to sensitive information and restrict it to authorised users."
        },
        {
            "id": "DP3",
            "question": "Does your organisation use appropriate protection, such as encryption, for sensitive information stored or transmitted through cloud services?",
            "why": "Sensitive information may be exposed if appropriate protection is not used.",
            "action": "Review encryption and other data-protection settings provided by your cloud services."
        }
    ],

    "Backup and Recovery": [
        {
            "id": "BR1",
            "question": "Is important cloud-based business information backed up appropriately?",
            "why": "Loss or corruption of important information can disrupt business operations.",
            "action": "Ensure important cloud-based information is included in an appropriate backup process."
        },
        {
            "id": "BR2",
            "question": "Are backups tested periodically to confirm that information can be successfully restored?",
            "why": "A backup may provide little protection if information cannot be restored when needed.",
            "action": "Perform and document periodic restoration tests."
        },
        {
            "id": "BR3",
            "question": "Does your organisation have a documented process for recovering important systems or information following disruption or data loss?",
            "why": "Recovery can be delayed when responsibilities and procedures have not been established.",
            "action": "Create a simple documented recovery process for important cloud systems and information."
        }
    ],

    "Monitoring and Visibility": [
        {
            "id": "MV1",
            "question": "Does your organisation maintain an up-to-date understanding of the cloud services and accounts it uses?",
            "why": "Unknown or unmanaged cloud services can create security gaps.",
            "action": "Maintain an inventory of important cloud services, accounts and responsible owners."
        },
        {
            "id": "MV2",
            "question": "Is security logging enabled for important cloud services where available?",
            "why": "Without appropriate logging, suspicious or harmful activity may be difficult to investigate.",
            "action": "Review important cloud services and enable suitable security logging where available."
        },
        {
            "id": "MV3",
            "question": "Are cloud-security alerts or logs reviewed so that suspicious activity can be identified?",
            "why": "Security events can remain unnoticed if available alerts and logs are not reviewed.",
            "action": "Assign responsibility for regularly reviewing important security alerts and logs."
        }
    ],

    "Incident Response": [
        {
            "id": "IR1",
            "question": "Does your organisation have a documented process for responding to a cybersecurity incident affecting cloud services?",
            "why": "An unclear response process can increase disruption during a security incident.",
            "action": "Document the basic steps to follow when a cloud-security incident occurs."
        },
        {
            "id": "IR2",
            "question": "Are responsibilities for responding to a cloud-security incident clearly assigned?",
            "why": "Incident response can be delayed when staff do not know who is responsible.",
            "action": "Assign clear incident-response responsibilities and relevant contact details."
        },
        {
            "id": "IR3",
            "question": "Do relevant staff know how to report suspected cloud-security incidents or suspicious activity?",
            "why": "Potential incidents may remain unreported when staff do not know the reporting process.",
            "action": "Provide staff with a clear and simple method for reporting suspected security incidents."
        }
    ],

    "Governance and Cloud Responsibility": [
        {
            "id": "GC1",
            "question": "Is responsibility for managing cloud security clearly assigned within your organisation or to an authorised service provider?",
            "why": "Security activities may be overlooked when responsibility is unclear.",
            "action": "Assign responsibility for cloud-security management to a named role or authorised provider."
        },
        {
            "id": "GC2",
            "question": "Does your organisation understand which security responsibilities belong to it and which belong to its cloud provider?",
            "why": "Cloud providers do not automatically manage every aspect of customer security.",
            "action": "Review the shared-responsibility information provided by your cloud-service providers."
        },
        {
            "id": "GC3",
            "question": "Are cloud-security practices reviewed periodically rather than only following an incident or external request?",
            "why": "Reactive security reviews can allow weaknesses to remain unidentified.",
            "action": "Schedule periodic reviews of important cloud-security practices."
        }
    ],

    "Third-Party and Cloud Services": [
        {
            "id": "TP1",
            "question": "Does your organisation consider security and privacy before adopting a new cloud service or provider?",
            "why": "A new service may introduce security, privacy or data-handling risks.",
            "action": "Include basic security and privacy checks when evaluating new cloud services."
        },
        {
            "id": "TP2",
            "question": "Does your organisation consider how important information can be recovered or accessed if a cloud provider experiences an outage or service failure?",
            "why": "Dependence on a provider can disrupt operations if continuity arrangements are unclear.",
            "action": "Review provider continuity arrangements and determine how important information would be recovered or accessed."
        },
        {
            "id": "TP3",
            "question": "Are third-party cloud services periodically reviewed to determine whether they continue to meet the organisation's security needs?",
            "why": "Security requirements and cloud services can change over time.",
            "action": "Periodically review important third-party cloud services and their security arrangements."
        }
    ],

    "Security Awareness": [
        {
            "id": "SA1",
            "question": "Do staff receive guidance or training on recognising phishing and other attempts to steal cloud-account credentials?",
            "why": "Phishing can lead to compromised cloud accounts and unauthorised access.",
            "action": "Provide staff with regular practical guidance on identifying and reporting phishing attempts."
        },
        {
            "id": "SA2",
            "question": "Are staff given guidance on securely sharing information through cloud services?",
            "why": "Incorrect sharing settings can expose organisational information.",
            "action": "Provide clear guidance on approved and secure methods for sharing cloud-based information."
        },
        {
            "id": "SA3",
            "question": "Are staff made aware of their responsibilities for protecting organisational cloud accounts and information?",
            "why": "Security controls are less effective when users do not understand their responsibilities.",
            "action": "Include cloud-security responsibilities in staff security awareness guidance."
        }
    ]
}

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def calculate_domain_score(questions, responses):
    obtained = 0
    maximum = 0

    for item in questions:
        response = responses.get(item["id"])

        if response in RESPONSE_SCORES:
            score = RESPONSE_SCORES[response]

            if score is not None:
                obtained += score
                maximum += 3

    if maximum == 0:
        return None

    return round((obtained / maximum) * 100, 1)


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


# =========================================================
# SESSION STATE
# =========================================================

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "context" not in st.session_state:
    st.session_state.context = {}

if "assessment_complete" not in st.session_state:
    st.session_state.assessment_complete = False


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🔐 Cloud Security Assessment")

page = st.sidebar.radio(
    "Navigation",
    [
        "Welcome",
        "Organisation Context",
        "Security Assessment",
        "Results"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Research prototype for SME cloud-security self-assessment."
)


# =========================================================
# WELCOME
# =========================================================

if page == "Welcome":

    st.title("🔐 SME Cloud Security Assessment Tool")

    st.subheader("About this prototype")

    st.write(
        """
        This research prototype is designed to help small and medium-sized
        enterprises (SMEs) identify areas of cloud-security practice that
        may require further attention.
        """
    )

    st.write(
        """
        The assessment covers eight areas of cloud security and provides
        prioritised, practical recommendations based on the answers provided.
        """
    )

    st.info(
        """
        **Important:** This tool is a questionnaire-based self-assessment aid.
        It does not certify that an organisation is secure and does not replace
        vulnerability scanning, penetration testing, formal security audits,
        or professional cybersecurity assessment.
        """
    )

    st.warning(
        """
        **Privacy:** Do not enter passwords, API keys, secret keys,
        access tokens, authentication credentials, or other sensitive
        security information.
        """
    )

    st.subheader("How the assessment works")

    st.markdown(
        """
        1. Complete the **Organisation Context** section.
        2. Complete the **Security Assessment**.
        3. Open **Results** to review your domain-level findings.
        4. Review the prioritised recommendations for areas requiring attention.
        """
    )

    st.subheader("Security areas covered")

    st.write(
        """
        Identity and Access Management • Data Protection • Backup and Recovery •
        Monitoring and Visibility • Incident Response • Governance and Cloud
        Responsibility • Third-Party and Cloud Services • Security Awareness
        """
    )


# =========================================================
# ORGANISATION CONTEXT
# =========================================================

elif page == "Organisation Context":

    st.title("Organisation Context")

    st.write(
        """
        These questions provide basic context for the assessment.
        They do **not** contribute to the assessment score.
        """
    )

    size_options = [
        "Select an option",
        "1–9 employees",
        "10–49 employees",
        "50–249 employees"
    ]

    cloud_use_options = [
        "Select an option",
        "SaaS applications",
        "Cloud-hosted infrastructure or applications",
        "Both",
        "Not sure"
    ]

    knowledge_options = [
        "Select an option",
        "Limited",
        "Moderate",
        "Advanced"
    ]

    organisation_size = st.selectbox(
        "C1. What is the approximate size of your organisation?",
        size_options,
        index=(
            size_options.index(st.session_state.context["organisation_size"])
            if st.session_state.context.get("organisation_size") in size_options
            else 0
        )
    )

    cloud_use = st.selectbox(
        "C2. How does your organisation mainly use cloud services?",
        cloud_use_options,
        index=(
            cloud_use_options.index(st.session_state.context["cloud_use"])
            if st.session_state.context.get("cloud_use") in cloud_use_options
            else 0
        )
    )

    platform_options = [
        "Microsoft 365 / Azure",
        "AWS",
        "Google Cloud / Google Workspace",
        "Other",
        "Not sure"
    ]

    cloud_platform = st.multiselect(
        "C3. Which cloud services or platforms does your organisation use?",
        platform_options,
        default=st.session_state.context.get("cloud_platform", [])
    )

    technical_knowledge = st.selectbox(
        "C4. How would you describe your level of technical knowledge?",
        knowledge_options,
        index=(
            knowledge_options.index(st.session_state.context["technical_knowledge"])
            if st.session_state.context.get("technical_knowledge") in knowledge_options
            else 0
        )
    )

    if st.button("Save organisation context", type="primary"):

        if (
            organisation_size == "Select an option"
            or cloud_use == "Select an option"
            or not cloud_platform
            or technical_knowledge == "Select an option"
        ):
            st.error("Please complete all four context questions.")

        else:
            st.session_state.context = {
                "organisation_size": organisation_size,
                "cloud_use": cloud_use,
                "cloud_platform": cloud_platform,
                "technical_knowledge": technical_knowledge
            }

            st.success(
                "Organisation context saved. You can now complete the Security Assessment."
            )


# =========================================================
# SECURITY ASSESSMENT
# =========================================================

elif page == "Security Assessment":

    st.title("Cloud Security Assessment")

    st.write(
        """
        Answer each question based on your organisation's **current practices**.
        Choose **Not sure** if you do not know the answer and
        **Not applicable** only where the control genuinely does not apply.
        """
    )

    if not st.session_state.context:
        st.warning(
            "Please complete and save the Organisation Context section before beginning the assessment."
        )

    total_questions = sum(len(qs) for qs in DOMAINS.values())

    st.caption(f"{total_questions} assessment questions across 8 security domains.")

    with st.form("assessment_form"):

        temporary_responses = {}

        for domain, questions in DOMAINS.items():

            st.header(domain)

            for item in questions:

                current_value = st.session_state.responses.get(
                    item["id"],
                    "Select an answer"
                )

                if current_value not in OPTIONS:
                    current_value = "Select an answer"

                temporary_responses[item["id"]] = st.selectbox(
                    f'{item["id"]}. {item["question"]}',
                    OPTIONS,
                    index=OPTIONS.index(current_value),
                    key=f'answer_{item["id"]}'
                )

            st.divider()

        submitted = st.form_submit_button(
            "Complete Assessment",
            type="primary"
        )

        if submitted:

            st.session_state.responses.update(temporary_responses)

            unanswered = [
                item["id"]
                for questions in DOMAINS.values()
                for item in questions
                if st.session_state.responses.get(item["id"])
                == "Select an answer"
            ]

            if unanswered:

                st.session_state.assessment_complete = False

                st.error(
                    "Please answer all assessment questions. "
                    "Unanswered: " + ", ".join(unanswered)
                )

            else:

                st.session_state.assessment_complete = True

                st.success(
                    "Assessment completed successfully. "
                    "Select Results from the sidebar to review your findings."
                )


# =========================================================
# RESULTS
# =========================================================

elif page == "Results":

    st.title("Assessment Results")

    if not st.session_state.assessment_complete:

        st.warning(
            "Please complete all questions in the Security Assessment before viewing results."
        )

    else:

        # -------------------------------------------------
        # CONTEXT SUMMARY
        # -------------------------------------------------

        if st.session_state.context:

            with st.expander("Organisation context"):

                st.write(
                    f"**Organisation size:** "
                    f"{st.session_state.context.get('organisation_size', 'Not provided')}"
                )

                st.write(
                    f"**Main cloud use:** "
                    f"{st.session_state.context.get('cloud_use', 'Not provided')}"
                )

                platforms = st.session_state.context.get(
                    "cloud_platform", []
                )

                st.write(
                    "**Cloud services/platforms:** "
                    + ", ".join(platforms)
                )

                st.write(
                    f"**Technical knowledge:** "
                    f"{st.session_state.context.get('technical_knowledge', 'Not provided')}"
                )

        # -------------------------------------------------
        # DOMAIN RESULTS
        # -------------------------------------------------

        st.header("Security Domain Summary")

        domain_results = []

        for domain, questions in DOMAINS.items():

            score = calculate_domain_score(
                questions,
                st.session_state.responses
            )

            level = concern_level(score)

            domain_results.append(
                {
                    "Security Domain": domain,
                    "Assessment Score (%)": score,
                    "Concern Classification": level
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
            Domain percentages are used to organise responses within this
            prototype. They are not validated measures of organisational
            cybersecurity.
            """
        )

        # -------------------------------------------------
        # FINDINGS
        # -------------------------------------------------

        st.header("Prioritised Findings and Recommendations")

        findings = []

        for domain, questions in DOMAINS.items():

            for item in questions:

                response = st.session_state.responses.get(item["id"])

                priority = recommendation_priority(response)

                if priority:

                    findings.append(
                        {
                            "domain": domain,
                            "id": item["id"],
                            "question": item["question"],
                            "response": response,
                            "priority": priority,
                            "why": item["why"],
                            "action": item["action"]
                        }
                    )

        priority_order = {
            "High": 0,
            "Medium": 1
        }

        findings.sort(
            key=lambda finding: priority_order.get(
                finding["priority"], 2
            )
        )

        if not findings:

            st.success(
                """
                No specific weaknesses were identified from the responses
                provided. This does not mean that the organisation is free
                from security vulnerabilities.
                """
            )

        else:

            high_count = sum(
                1 for finding in findings
                if finding["priority"] == "High"
            )

            medium_count = sum(
                1 for finding in findings
                if finding["priority"] == "Medium"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "High-priority findings",
                high_count
            )

            col2.metric(
                "Medium-priority findings",
                medium_count
            )

            for finding in findings:

                if finding["priority"] == "High":
                    st.error(
                        f'High Priority — {finding["id"]}: '
                        f'{finding["domain"]}'
                    )
                else:
                    st.warning(
                        f'Medium Priority — {finding["id"]}: '
                        f'{finding["domain"]}'
                    )

                st.write(
                    f'**Issue assessed:** {finding["question"]}'
                )

                st.write(
                    f'**Your response:** {finding["response"]}'
                )

                st.write(
                    f'**Why it matters:** {finding["why"]}'
                )

                st.write(
                    f'**Recommended action:** {finding["action"]}'
                )

                st.divider()

        # -------------------------------------------------
        # INTERPRETATION
        # -------------------------------------------------

        st.header("Understanding Your Results")

        st.info(
            """
            **Concern classifications**

            **Lower concern:** 75–100%  
            **Moderate concern:** 50–74%  
            **Higher concern:** 0–49%

            These thresholds are prototype classification rules used to
            organise and prioritise self-assessment responses. They have not
            been validated as measures of actual organisational security.
            """
        )

        st.warning(
            """
            This questionnaire does not perform technical scanning,
            vulnerability testing, penetration testing, or independent
            verification of the answers provided.

            A lower-concern result does not certify that an organisation,
            cloud service, or system is secure. Professional cybersecurity
            advice should be considered where significant risks or
            uncertainties are identified.
            """
        )

        st.subheader("Reassessment")

        st.write(
            """
            The assessment can be completed again after recommended
            improvements have been implemented. Reassessment can help users
            review their practices against the same assessment criteria.
            """
        )
