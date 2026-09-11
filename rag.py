from pathlib import Path
from typing import Literal
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from tools import tools

BASE_DIR = Path(__file__).parent
CHROMA_DIR = BASE_DIR / "chroma_db"

# Keeping qwen3:8b as you requested
llm = ChatOllama(model="qwen3:8b", temperature=0)
llm_with_tools = llm.bind_tools(tools)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)

class AgentState(MessagesState):
    route: str
    question: str
    context: str
    answer: str
    sources: list

def router(state: AgentState):
    question = state["messages"][-1].content
    routing_prompt = f"""
You are the routing system for ThunAI. Classify into ONE category: GENERAL, DOCUMENT, or TOOL.

GENERAL: Greetings, general knowledge.
DOCUMENT: Information extraction from company SOPs, manuals, inspection reports.
TOOL: Math, calculations, generating Word documents (.docx), creating approval notes, creating charts, or analyzing CSVs.

User question: {question}
Return ONLY: GENERAL, DOCUMENT, or TOOL.
"""
    response = llm.invoke(routing_prompt)
    decision = response.content.strip().upper()
    if "DOCUMENT" in decision: route = "document"
    elif "TOOL" in decision: route = "tool"
    else: route = "general"
    return {"route": route, "question": question}

def route_question(state: AgentState) -> Literal["general_answer", "retrieve", "tool_agent"]:
    if state["route"] == "document": return "retrieve"
    if state["route"] == "tool": return "tool_agent"
    return "general_answer"

def generate_general_answer(state: AgentState):
    response = llm.invoke(f"Answer clearly. Question: {state['question']}")
    return {"answer": response.content}

def retrieve_documents(state: AgentState):
    results = vector_db.similarity_search(state["question"], k=3)
    context_parts = []
    sources = []
    for doc in results:
        source = doc.metadata.get("source", "Unknown")
        context_parts.append(f"SOURCE: {source}\nCONTENT:\n{doc.page_content}")
        sources.append({"document": source})
    return {"context": "\n\n".join(context_parts), "sources": sources}

def generate_document_answer(state: AgentState):
    prompt = f"Answer using ONLY context. CONTEXT: {state['context']} QUESTION: {state['question']}"
    response = llm.invoke(prompt)
    return {"answer": response.content}

def tool_agent(state: AgentState):
    system_message = "You are the engineering/document agent. Use tools to calculate or generate Word documents."
    messages = [{"role": "system", "content": system_message}] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def finalize_tool_answer(state: AgentState):
    for message in reversed(state["messages"]):
        if getattr(message, "type", None) == "ai" and message.content:
            return {"answer": message.content}
    return {"answer": "The task was completed successfully."}

graph = StateGraph(AgentState)
graph.add_node("router", router)
graph.add_node("general_answer", generate_general_answer)
graph.add_node("retrieve", retrieve_documents)
graph.add_node("document_answer", generate_document_answer)
graph.add_node("tool_agent", tool_agent)
graph.add_node("tools", ToolNode(tools))
graph.add_node("tool_final", finalize_tool_answer)

graph.add_edge(START, "router")
graph.add_conditional_edges("router", route_question, {"general_answer": "general_answer", "retrieve": "retrieve", "tool_agent": "tool_agent"})
graph.add_edge("general_answer", END)
graph.add_edge("retrieve", "document_answer")
graph.add_edge("document_answer", END)
graph.add_conditional_edges("tool_agent", tools_condition, {"tools": "tools", END: "tool_final"})
graph.add_edge("tools", "tool_agent")
graph.add_edge("tool_final", END)

agent = graph.compile()