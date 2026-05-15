# Smart After-Sales Agent

基于大模型的智能售后 Agent，致力于解决传统客服系统在处理复杂、非标准化客户咨询时效率低、人工成本高的痛点。

## ✨ 核心功能

### 1. RAG 检索增强生成
- 实时接入企业内部产品 FAQ 和维修手册知识库
- 确保回答的准确性和时效性
- 支持多文档格式的知识检索

### 2. 长链推理引擎
- 解析客户多轮、复杂的意图
- 自动匹配最佳解决方案
- 支持上下文理解和记忆

### 3. 工单自动创建
- 自动提取咨询摘要
- 智能路由至对应人工坐席
- 无缝衔接人机协作流程

## 📊 效果数据

| 指标 | 改善前 | 改善后 | 提升幅度 |
|------|--------|--------|----------|
| 日均处理量 | - | ~200次 | - |
| 平均等待时间 | - | 缩短50% | 50% |
| 人工介入率 | - | 降低35% | 35% |

## 🛠️ 技术栈

- **大模型**: 支持主流大模型接口
- **RAG**: 检索增强生成技术
- **向量数据库**: 用于知识库存储与检索
- **LangChain**: 长链推理框架
- **API Gateway**: RESTful API 服务

## 🚀 快速开始

### 环境要求
- Python 3.10+
- 依赖见 `requirements.txt`

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置
配置文件位于 `config/settings.py`，需设置：
- 大模型 API Key
- 知识库路径
- 向量数据库连接信息

### 启动服务
```bash
python app/main.py
```

## 📁 项目结构

```
.
├── app/                    # 应用主目录
│   ├── main.py             # 入口文件
│   ├── api/                # API 接口
│   ├── rag/                # RAG 模块
│   ├── reasoning/          # 推理引擎
│   └── ticketing/          # 工单模块
├── config/                 # 配置文件
├── docs/                   # 文档
├── tests/                  # 测试用例
└── requirements.txt        # 依赖列表
```

## 🔌 API 接口

### 咨询接口
```
POST /api/chat
Content-Type: application/json

{
  "user_id": "string",
  "message": "string",
  "context": []
}
```

### 工单创建
```
POST /api/ticket/create
Content-Type: application/json

{
  "user_id": "string",
  "summary": "string",
  "category": "string",
  "priority": "low|medium|high"
}
```

## 📝 使用说明

1. **知识库准备**: 将产品 FAQ 和维修手册放入 `data/knowledge/` 目录
2. **向量索引构建**: 运行 `python scripts/build_index.py`
3. **启动服务**: 运行 `python app/main.py`
4. **接入客服系统**: 通过 API 接口接入现有客服平台

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

*Built with ❤️ for smarter customer support*
