
import json
from fastapi import APIRouter,  Request
from fastapi.responses import StreamingResponse
from services.agent.graph import graph
from langchain_core.messages import HumanMessage, AIMessageChunk

router = APIRouter(prefix="/api/agent", tags=["agent"])


def sse(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.get("/stream")
async def get_stream(
    req: str,
    request: Request,
):
    async def event_generator():
        try:
            yield sse({"type": "start"})
            async for chunk, meta in graph.astream(
                    {"messages": [HumanMessage(content=req)]},
                    config={"recursion_limit": 12},  # 替代你原来 MAX_STEPS=6
                    stream_mode="messages",
            ):
                if meta.get("langgraph_node") != "agent":
                    continue  # 过滤掉 tools 节点的输出
                if not isinstance(chunk, AIMessageChunk):
                    continue
                if chunk.content:
                    yield sse({"type": "delta", "text": chunk.content})
                if chunk.tool_call_chunks:  # 前端可显示"正在检索…"
                    yield sse({"type": "tool", "name": chunk.tool_call_chunks[0].get("name")})
            yield sse({"type": "done"})
        except Exception as e:
            yield sse({"type": "error", "message": f"{type(e).__name__}: {e}"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

