from datetime import date
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from services.llm import build_llm
from services.agent.tools import ALL_TOOLS
from services.agent.prompt import SYSTEM_PROMPT

model = build_llm().bind_tools(ALL_TOOLS)

def build_graph():
    async def agent_node(state: MessagesState):
        msgs = state["messages"]
        if not msgs or not isinstance(msgs[0], SystemMessage):
            msgs = [SystemMessage(SYSTEM_PROMPT.format(today=date.today())), *msgs]
        return {"messages": [await model.ainvoke(msgs)]}

    g = StateGraph(MessagesState)
    g.add_node("agent", agent_node)
    g.add_node("tools", ToolNode(ALL_TOOLS, handle_tool_errors=True))
    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    return g.compile()

graph = build_graph()      # 模块级单例，避免每请求重建
