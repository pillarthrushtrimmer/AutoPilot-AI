"""WebSocket endpoint."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.core.engine import Engine, AgentConfig

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    engine = Engine(AgentConfig(verbose=False))
    try:
        while True:
            data = await ws.receive_json()
            task = data.get("task", "")
            if not task: await ws.send_json({"error": "No task"}); continue
            await ws.send_json({"status": "planning", "task": task})
            r = await engine.run(task)
            await ws.send_json({"status": "complete", "output": r.output, "steps": len(r.steps), "duration_ms": r.total_duration_ms})
    except WebSocketDisconnect: pass
