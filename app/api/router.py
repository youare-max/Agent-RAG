from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag.retriever import RAGRetriever
from app.reasoning.engine import ReasoningEngine
from app.ticketing.creator import TicketCreator

router = APIRouter()

retriever = RAGRetriever()
reasoning_engine = ReasoningEngine()
ticket_creator = TicketCreator()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: list = []

class TicketCreateRequest(BaseModel):
    user_id: str
    summary: str
    category: str
    priority: str = "low"

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        knowledge = retriever.retrieve(request.message)
        knowledge_text = "\n\n".join(knowledge)
        
        response = reasoning_engine.infer(request.message, knowledge_text)
        
        needs_human = reasoning_engine.needs_human_intervention(response)
        
        if needs_human:
            conversation = "\n".join([f"{ctx['role']}: {ctx['content']}" for ctx in request.context])
            conversation += f"\n用户: {request.message}\n助手: {response}"
            
            ticket_result = ticket_creator.create_ticket(request.user_id, conversation)
            
            return {
                "response": response,
                "needs_human_intervention": True,
                "ticket_created": ticket_result["success"],
                "ticket_id": ticket_result.get("ticket_id")
            }
        
        return {
            "response": response,
            "needs_human_intervention": False,
            "ticket_created": False
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ticket/create")
async def create_ticket(request: TicketCreateRequest):
    try:
        result = ticket_creator.create_ticket(
            request.user_id,
            request.summary
        )
        
        if result["success"]:
            return {"ticket_id": result["ticket_id"]}
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/knowledge/update")
async def update_knowledge():
    try:
        retriever.update_knowledge_base()
        return {"message": "知识库更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
