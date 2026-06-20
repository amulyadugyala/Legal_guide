from crewai import Task

from agents.explainability_agent import explainability_agent
from tasks.case_intake_task import case_intake_task
from tasks.ipc_section_task import ipc_section_task
from tasks.legal_precedent_task import legal_precedent_task
from tasks.legal_reasoning_task import legal_reasoning_task


explainability_task = Task(
    agent=explainability_agent,

    description=(
        "Provide a clear explanation of how the legal reasoning system "
        "analyzed this case.\n\n"

        "Explain the reasoning step-by-step including:\n"
        "- What the legal issue is\n"
        "- Which IPC sections were identified and why\n"
        "- Which precedent cases were considered\n"
        "- What arguments were made by the opponent\n"
        "- What counterarguments were made by the defence\n"
        "- How the judge evaluated both sides\n"
        "- Why the final reasoning was reached\n\n"

        "Write the explanation in simple, easy-to-understand language."
    ),

    expected_output=(
        "A step-by-step explanation of the reasoning process used by the "
        "multi-agent legal system to analyze the case."
    ),

    context=[
        case_intake_task,
        ipc_section_task,
        legal_precedent_task,
        legal_reasoning_task
    ]
)