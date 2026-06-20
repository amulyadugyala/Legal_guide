from crewai import Task

from agents.legal_reasoning_agent import legal_reasoning_agent
from tasks.case_intake_task import case_intake_task
from tasks.ipc_section_task import ipc_section_task
from tasks.legal_precedent_task import legal_precedent_task


legal_reasoning_task = Task(
    agent=legal_reasoning_agent,

    description=(
        "Analyze the case using a courtroom-style reasoning process.\n\n"

        "Your analysis must contain three sections:\n\n"

        "1. Opponent Perspective\n"
        "- Explain the complainant/prosecution argument\n"
        "- Apply relevant IPC sections\n"
        "- Use precedent cases that support the claim\n\n"

        "2. Defence Perspective\n"
        "- Identify weaknesses in the prosecution case\n"
        "- Provide legal defenses\n"
        "- Interpret IPC sections favorably for the accused\n"
        "- Cite supporting precedents\n\n"

        "3. Judicial Evaluation\n"
        "- Objectively analyze both arguments\n"
        "- Interpret IPC provisions\n"
        "- Evaluate precedent relevance\n"
        "- Provide a balanced legal reasoning overview\n"
    ),

    expected_output=(
        "A structured legal reasoning analysis containing three sections:\n"
        "1. Opponent Argument\n"
        "2. Defence Argument\n"
        "3. Judicial Evaluation"
    ),

    context=[
        case_intake_task,
        ipc_section_task,
        legal_precedent_task
    ]
)