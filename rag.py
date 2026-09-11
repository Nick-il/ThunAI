from pathlib import Path
from typing import Literal

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langgraph.graph import (
    StateGraph,
    START,
    END,
    MessagesState,
)

from langgraph.prebuilt import ToolNode, tools_condition

from tools import tools


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# MODELS
# ============================================================

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0
)


# LLM with access to our Python tools
llm_with_tools = llm.bind_tools(tools)


# ============================================================
# VECTOR DATABASE
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_db = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings
)


# ============================================================
# STATE
# ============================================================

class AgentState(MessagesState):

    route: str

    question: str

    context: str

    answer: str

    sources: list


# ============================================================
# ROUTER
# ============================================================

def router(state: AgentState):

    question = state["messages"][-1].content

    routing_prompt = f"""
You are the routing system for ThunAI,
a confidential industrial AI assistant.

Classify the user's request into exactly ONE
of these categories:

GENERAL
DOCUMENT
TOOL

--------------------------------------------

GENERAL:

Use GENERAL for:

- Greetings
- Casual conversation
- General knowledge
- Conceptual questions
- Questions that do not require company documents
- Questions that do not require calculations or data analysis

Examples:

"Hello"

"What is machine learning?"

"Explain entropy."

--------------------------------------------

DOCUMENT:

Use DOCUMENT when the user needs information
from company or organization documents.

Examples:

"According to the inspection report, what was
the pressure recorded?"

"What does the company safety manual say?"

"What is the maximum temperature mentioned
in the uploaded report?"

"What did the maintenance report say about
Pump P-101?"

If the question refers to a report, manual,
drawing, inspection document, internal policy,
contract, or other company document, use DOCUMENT.

--------------------------------------------

TOOL:

Use TOOL when the user explicitly needs:

- Mathematical calculations
- Scientific calculations
- Engineering calculations
- Unit conversions
- Fluid mechanics calculations
- Heat-transfer calculations
- Thermodynamics calculations
- Process calculations
- Equipment calculations
- Statistical analysis
- Correlation
- Regression
- CSV analysis
- Excel analysis
- Data analysis
- Bar charts
- Line charts
- Pie charts
- Scatter plots
- Histograms

Examples:

"Calculate Reynolds number."

"Convert 50 psi to bar."

"Calculate pressure drop."

"Find the mean and standard deviation."

"Create a bar chart."

"Calculate heat exchanger duty."

"Analyze this dataset."

--------------------------------------------

IMPORTANT:

If the user asks for a calculation or data
analysis that does NOT require company documents,
choose TOOL.

Return ONLY:

GENERAL

or

DOCUMENT

or

TOOL

User question:

{question}
"""

    response = llm.invoke(routing_prompt)

    decision = response.content.strip().upper()

    if "DOCUMENT" in decision:
        route = "document"

    elif "TOOL" in decision:
        route = "tool"

    else:
        route = "general"

    return {
        "route": route,
        "question": question
    }


# ============================================================
# ROUTING DECISION
# ============================================================

def route_question(state: AgentState) -> Literal[
    "general_answer",
    "retrieve",
    "tool_agent"
]:

    if state["route"] == "document":
        return "retrieve"

    if state["route"] == "tool":
        return "tool_agent"

    return "general_answer"


# ============================================================
# GENERAL ANSWER
# ============================================================

def generate_general_answer(state: AgentState):

    question = state["question"]

    prompt = f"""
You are ThunAI.

Answer the user's question clearly and accurately.

This question does not require the company's
internal documents or engineering tools.

User question:

{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# ============================================================
# DOCUMENT RETRIEVAL
# ============================================================

def retrieve_documents(state: AgentState):

    question = state["question"]

    results = vector_db.similarity_search(
        question,
        k=3
    )

    context_parts = []

    sources = []

    for doc in results:

        source = doc.metadata.get(
            "source",
            "Unknown document"
        )

        page = doc.metadata.get(
            "page",
            "Unknown page"
        )

        context_parts.append(
            f"""
SOURCE: {source}
PAGE: {page}

CONTENT:

{doc.page_content}
"""
        )

        sources.append(
            {
                "document": source,
                "page": page
            }
        )

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources
    }


# ============================================================
# DOCUMENT ANSWER
# ============================================================

def generate_document_answer(state: AgentState):

    question = state["question"]

    context = state["context"]

    prompt = f"""
You are ThunAI, a confidential document assistant.

Answer the user's question using ONLY the
provided document context.

Do not invent information.

If the answer is not present in the context,
say:

"I do not have enough information in the
available documents."

Always be precise.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# ============================================================
# TOOL AGENT
# ============================================================

def tool_agent(state: AgentState):

    """
    Ask Qwen to determine whether it needs
    one of the available Python tools.

    Qwen can generate a tool call such as:

    calculator(...)
    reynolds_number(...)
    statistical_analysis(...)
    create_bar_chart(...)
    etc.
    """

    system_message = """
You are the engineering analysis agent
inside ThunAI.

You have access to local Python engineering,
scientific, statistical, data-analysis and
visualization tools.

Use the tools whenever the user's request
requires an actual calculation, numerical
analysis, data analysis or chart.

Do NOT manually calculate when an appropriate
tool exists.

Choose the appropriate tool and provide the
required arguments.

After receiving the tool result, explain the
result clearly to the user.

For engineering calculations:

- State the result clearly.
- Include units when available.
- Do not invent missing input values.
- If required information is missing, ask
  the user for it.
- Do not claim that a calculation is
  plant-certified or safety-approved.

All tools execute locally.
"""

    messages = [
        {
            "role": "system",
            "content": system_message
        }
    ]

    messages.extend(state["messages"])

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ============================================================
# TOOL RESULT → FINAL ANSWER
# ============================================================

def finalize_tool_answer(state: AgentState):

    messages = state["messages"]

    # Last AI response should contain the
    # final answer after tool execution.
    for message in reversed(messages):

        if getattr(message, "type", None) == "ai":

            if message.content:

                return {
                    "answer": message.content
                }

    return {
        "answer": "The calculation was completed."
    }


# ============================================================
# LANGGRAPH
# ============================================================

graph = StateGraph(AgentState)


# ------------------------------------------------------------
# Nodes
# ------------------------------------------------------------

graph.add_node(
    "router",
    router
)

graph.add_node(
    "general_answer",
    generate_general_answer
)

graph.add_node(
    "retrieve",
    retrieve_documents
)

graph.add_node(
    "document_answer",
    generate_document_answer
)

graph.add_node(
    "tool_agent",
    tool_agent
)

graph.add_node(
    "tools",
    ToolNode(tools)
)

graph.add_node(
    "tool_final",
    finalize_tool_answer
)


# ------------------------------------------------------------
# START
# ------------------------------------------------------------

graph.add_edge(
    START,
    "router"
)


# ------------------------------------------------------------
# Router
# ------------------------------------------------------------

graph.add_conditional_edges(
    "router",
    route_question,
    {
        "general_answer": "general_answer",
        "retrieve": "retrieve",
        "tool_agent": "tool_agent"
    }
)


# ------------------------------------------------------------
# General
# ------------------------------------------------------------

graph.add_edge(
    "general_answer",
    END
)


# ------------------------------------------------------------
# RAG
# ------------------------------------------------------------

graph.add_edge(
    "retrieve",
    "document_answer"
)

graph.add_edge(
    "document_answer",
    END
)


# ------------------------------------------------------------
# TOOL AGENT
# ------------------------------------------------------------

graph.add_conditional_edges(
    "tool_agent",
    tools_condition,
    {
        "tools": "tools",
        END: "tool_final"
    }
)


# ------------------------------------------------------------
# Tool execution → Tool Agent
# ------------------------------------------------------------

graph.add_edge(
    "tools",
    "tool_agent"
)


# ------------------------------------------------------------
# Final tool answer
# ------------------------------------------------------------

graph.add_edge(
    "tool_final",
    END
)


# ============================================================
# COMPILE
# ============================================================

agent = graph.compile()