"""REST API Routes."""
from fastapi import APIRouter
from pydantic import BaseModel
from src.core.engine import Engine, AgentConfig

router = APIRouter()

class TaskReq(BaseModel):
    task: str
    model: str = "gpt-4o"
    temperature: float = 0.7

class TaskResp(BaseModel):
    task: str
    output: str
    steps_count: int
    duration_ms: float

@router.post("/run", response_model=TaskResp)
async def run_task(req: TaskReq):
    engine = Engine(AgentConfig(model=req.model, temperature=req.temperature, verbose=False))
    r = await engine.run(req.task)
    return TaskResp(task=req.task, output=r.output, steps_count=len(r.steps), duration_ms=r.total_duration_ms)

@router.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
