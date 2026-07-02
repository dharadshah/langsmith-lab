# app/services/agent_service.py
import ast
import operator

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.config import settings, export_langsmith_env
from app.constants.app_constants import MODEL_NAME, MODEL_TEMPERATURE
from app.constants.prompts import QA_AGENT_SYSTEM_PROMPT

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}


def _evaluate_node(node: ast.expr) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](
            _evaluate_node(node.left), _evaluate_node(node.right)
        )
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_evaluate_node(node.operand)
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '12 * (3 + 4)'."""
    parsed = ast.parse(expression, mode="eval")
    return str(_evaluate_node(parsed.body))


class AgentService:
    """Owns the LLM and the ReAct agent graph for question answering."""

    def __init__(self) -> None:
        export_langsmith_env()
        self._llm = ChatGroq(
            model=MODEL_NAME,
            temperature=MODEL_TEMPERATURE,
            api_key=settings.groq_api_key,
        )
        self._agent = create_react_agent(
            self._llm,
            tools=[calculator],
            prompt=QA_AGENT_SYSTEM_PROMPT,
        )

    def ask(self, question: str) -> str:
        result = self._agent.invoke({"messages": [("user", question)]})
        return result["messages"][-1].content