from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from config.settings import settings

class ReasoningEngine:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.3
        )
        self.memory = ConversationBufferMemory()
        self.chain = self._build_chain()
    
    def _build_chain(self):
        template = """你是一个专业的智能售后客服助手。
        根据以下知识库内容和对话历史，回答用户的问题：
        
        知识库：
        {knowledge}
        
        对话历史：
        {history}
        
        用户问题：
        {input}
        
        请遵循以下规则：
        1. 优先使用知识库中的信息回答
        2. 如果知识库中没有相关信息，使用你的知识回答
        3. 如果无法回答，明确说明并建议转人工
        4. 保持回答简洁、专业、友好
        """
        
        prompt = PromptTemplate(
            input_variables=["knowledge", "history", "input"],
            template=template
        )
        
        return ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt
        )
    
    def infer(self, user_input, knowledge=""):
        response = self.chain.run(
            knowledge=knowledge,
            history=self.memory.buffer,
            input=user_input
        )
        return response
    
    def clear_memory(self):
        self.memory.clear()
    
    def needs_human_intervention(self, response):
        keywords = ["转人工", "无法回答", "需要帮助", "联系客服"]
        return any(keyword in response for keyword in keywords)
