import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ticketing.creator import TicketCreator

def test_extract_summary():
    creator = TicketCreator()
    conversation = "用户：我的产品无法启动了\n助手：请检查电源连接\n用户：已经检查过了，还是不行"
    result = creator.extract_summary(conversation)
    assert "summary" in result
    assert "category" in result
    assert "priority" in result
    print("工单摘要提取测试通过")

def test_create_ticket():
    creator = TicketCreator()
    result = creator.create_ticket("user123", "测试对话内容")
    assert result["success"]
    print("工单创建测试通过")

if __name__ == "__main__":
    test_extract_summary()
    test_create_ticket()
