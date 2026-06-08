"""
REST API服务
3级模块：单词数=1（Main）
"""
import os
import sys
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Rag.impl.BuilderImpl import BuilderImpl
from src.utils.logger import get_logger


class QueryRequest(BaseModel):
    """查询请求"""
    question: str
    top_k: Optional[int] = 4


class QueryResponse(BaseModel):
    """查询响应"""
    answer: str
    sources: List[Dict[str, Any]]
    model_used: str


class StatusResponse(BaseModel):
    """状态响应"""
    document_count: int
    vector_count: int
    bm25_index_size: int
    embedding_available: bool
    offline_mode: bool


app = FastAPI(
    title="RAG Agent API",
    description="检索增强生成智能体API",
    version="2.1.0"
)

# 全局Agent实例
_agent = None
_logger = get_logger()


def get_agent():
    """获取Agent实例"""
    global _agent
    if _agent is None:
        _logger.info("API", "初始化Agent")
        builder = BuilderImpl()
        _agent = builder.build_agent()
    return _agent


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """查询接口"""
    _logger.enter_method("API", "query", question=request.question)
    try:
        agent = get_agent()
        answer = agent.query(request.question)
        status = agent.get_status()
        
        response = QueryResponse(
            answer=answer,
            sources=[],
            model_used="mock-llm"
        )
        _logger.exit_method("API", "query")
        return response
    except Exception as e:
        _logger.error("API", "查询失败", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents")
async def add_documents(documents: List[str]):
    """添加文档接口"""
    _logger.enter_method("API", "add_documents", doc_count=len(documents))
    try:
        agent = get_agent()
        agent.add_documents(documents)
        status = agent.get_status()
        _logger.exit_method("API", "add_documents")
        return {"status": "success", "document_count": status["document_count"]}
    except Exception as e:
        _logger.error("API", "添加文档失败", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """获取系统状态"""
    _logger.enter_method("API", "get_status")
    try:
        agent = get_agent()
        status = agent.get_status()
        _logger.exit_method("API", "get_status")
        return StatusResponse(**status)
    except Exception as e:
        _logger.error("API", "获取状态失败", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset():
    """重置系统"""
    _logger.enter_method("API", "reset")
    try:
        agent = get_agent()
        agent.reset()
        _logger.exit_method("API", "reset")
        return {"status": "reset_complete"}
    except Exception as e:
        _logger.error("API", "重置失败", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "version": "2.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
