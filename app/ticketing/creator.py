import requests
from config.settings import settings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class TicketCreator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.1
        )
    
    def extract_summary(self, conversation_history):
        template = """请总结以下客户对话，提取关键信息：
        
        对话内容：
        {conversation}
        
        请输出：
        1. 用户问题摘要（不超过50字）
        2. 问题分类（硬件问题/软件问题/账户问题/其他）
        3. 紧急程度（低/中/高）
        
        格式：
        摘要：xxx
        分类：xxx
        紧急程度：xxx
        """
        
        prompt = PromptTemplate(
            input_variables=["conversation"],
            template=template
        )
        
        result = self.llm.predict(prompt.format(conversation=conversation_history))
        return self._parse_summary(result)
    
    def _parse_summary(self, text):
        summary = ""
        category = "其他"
        priority = "低"
        
        lines = text.strip().split("\n")
        for line in lines:
            if line.startswith("摘要："):
                summary = line.replace("摘要：", "").strip()
            elif line.startswith("分类："):
                category = line.replace("分类：", "").strip()
            elif line.startswith("紧急程度："):
                priority = line.replace("紧急程度：", "").strip()
        
        return {
            "summary": summary,
            "category": category,
            "priority": priority
        }
    
    def create_ticket(self, user_id, conversation_history):
        info = self.extract_summary(conversation_history)
        
        payload = {
            "user_id": user_id,
            "summary": info["summary"],
            "category": info["category"],
            "priority": info["priority"],
            "conversation_history": conversation_history
        }
        
        if settings.TICKET_API_URL:
            headers = {"Authorization": f"Bearer {settings.TICKET_API_KEY}"}
            response = requests.post(
                settings.TICKET_API_URL,
                json=payload,
                headers=headers
            )
            if response.status_code == 200:
                return {"success": True, "ticket_id": response.json().get("ticket_id")}
            else:
                return {"success": False, "error": response.text}
        
        return {"success": True, "ticket_id": "mock-" + user_id[:8]}
