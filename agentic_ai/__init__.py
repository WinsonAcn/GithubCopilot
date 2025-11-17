"""
Agentic AI System - Multi-Agent Orchestration Framework

This package provides a complete framework for building and orchestrating
multiple AI agents that can communicate with each other, use tools, and
manage complex workflows.
"""

from .agent import Agent, AgentManager, Message, MessageType, Tool, AgentState
from .specialized_agents import (
    AnalyzerAgent,
    PlannerAgent,
    ExecutorAgent,
    CoordinatorAgent,
    KnowledgeAgent,
)
from .workflow_graph import WorkflowGraph, GraphNode, GraphEdge, NodeType

__version__ = "1.0.0"
__author__ = "Agentic AI Team"

__all__ = [
    # Core classes
    "Agent",
    "AgentManager",
    "Message",
    "MessageType",
    "Tool",
    "AgentState",
    # Specialized agents
    "AnalyzerAgent",
    "PlannerAgent",
    "ExecutorAgent",
    "CoordinatorAgent",
    "KnowledgeAgent",
    # Graph components
    "WorkflowGraph",
    "GraphNode",
    "GraphEdge",
    "NodeType",
]
