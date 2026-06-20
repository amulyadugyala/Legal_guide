# Legal_guide

The increasing complexity of legal systems and the lack of accessible legal guidance for the general 
public create a significant barrier to justice. Individuals often struggle to interpret legal provisions, 
understand applicable laws, and analyze their situations from a legal perspective without 
professional assistance. To address this challenge, this project presents “LEGAL GUIDE –A 
PLATFORM FOR LEGAL ASSISTANCE,” an AI-driven framework that simulates structured 
legal reasoning using a collaborative multi-agent architecture. 

The system leverages a modular design built on the CrewAI framework, where multiple specialized 
agents perform distinct legal tasks in a coordinated pipeline.The process begins with a Case Intake 
Agent,which interprets user-provided legal queries and converts them into structured representations 
including case type, legal domain, and relevant entities. 

This structured input is then utilized by the IPC Section Agent,which retrieves the most relevant 
provisions of the Indian Penal Code using a vector database powered by semantic similarity 
search.Simultaneously,a Legal Precedent Agent identifies relevant case laws from trusted legal 
sources, ensuring that the reasoning process is grounded in real judicial decisions. 

A key contribution of the system is the Legal Reasoning Agent, which performs courtroom-style 
analysis by generating arguments from both the prosecution (opponent) and defense perspectives, 
followed by an objective judicial evaluation.To enhance transparency, an Explainability Agent 
provides a step-by-step breakdown of how the system arrived at its conclusions, making the 
reasoning process understandable even to non-legal users. 

Finally, a Legal Drafter Agent synthesizes all intermediate outputs into a comprehensive, structured 
legal report covering key issues, applicable laws, precedents, and final interpretations. 
The system integrates multiple technologies, including large language models (LLaMA-based via 
Groq API), vector databases (Chroma), semantic embeddings (HuggingFace), and real-time web
based interfaces using Streamlit. The orchestration of agents and tasks is managed through a 
centralized crew pipeline, ensuring sequential and context-aware execution of all legal reasoning 
stages. 

The proposed system demonstrates how multi-agent AI architectures can be effectively applied to 
legal informatics, offering scalable, explainable, and user-friendly legal assistance. While not a 
substitute for professional legal advice, it serves as a powerful decision-support tool for preliminary 
legal understanding, education, and analysis. 
