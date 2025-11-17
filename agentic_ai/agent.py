"""
Core agent framework for agentic AI system.
"""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid
from datetime import datetime
import json


class MessageType(Enum):
    """Types of messages between agents."""
    REQUEST = "request"
    RESPONSE = "response"
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    QUERY = "query"


@dataclass
class Message:
    """Message passed between agents."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    receiver: str = ""
    type: MessageType = MessageType.REQUEST
    content: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    parent_message_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type.value,
            "content": self.content,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "parent_message_id": self.parent_message_id,
        }


@dataclass
class Tool:
    """Represents a tool/function that an agent can use."""
    name: str
    description: str
    func: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)

    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        return self.func(**kwargs)


@dataclass
class AgentState:
    """State of an agent."""
    id: str
    name: str
    role: str
    memory: List[Message] = field(default_factory=list)
    tools: Dict[str, Tool] = field(default_factory=dict)
    active: bool = True
    execution_count: int = 0


class Agent:
    """Base agent class with tool usage and communication capabilities."""

    def __init__(self, name: str, role: str, agent_manager=None):
        """
        Initialize an agent.
        
        Args:
            name: Name of the agent
            role: Role/purpose of the agent
            agent_manager: Reference to the agent manager for inter-agent communication
        """
        self.state = AgentState(
            id=str(uuid.uuid4()),
            name=name,
            role=role,
        )
        self.agent_manager = agent_manager
        self.message_queue: List[Message] = []
        self.response_handlers: Dict[str, Callable] = {}

    def register_tool(self, tool: Tool) -> None:
        """Register a tool that the agent can use."""
        self.state.tools[tool.name] = tool

    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Use a registered tool."""
        if tool_name not in self.state.tools:
            raise ValueError(f"Tool '{tool_name}' not found in {self.state.name}'s toolkit")
        
        tool = self.state.tools[tool_name]
        try:
            result = tool.execute(**kwargs)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def send_message(self, receiver: str, content: str, msg_type: MessageType = MessageType.REQUEST, 
                    data: Dict[str, Any] = None) -> Optional[str]:
        """
        Send a message to another agent.
        
        Args:
            receiver: Name of the receiving agent
            content: Message content
            msg_type: Type of message
            data: Optional data payload
            
        Returns:
            Message ID if sent successfully, None otherwise
        """
        if not self.agent_manager:
            return None

        message = Message(
            sender=self.state.name,
            receiver=receiver,
            type=msg_type,
            content=content,
            data=data or {},
        )
        
        self.state.memory.append(message)
        self.agent_manager.route_message(message)
        return message.id

    def receive_message(self, message: Message) -> None:
        """Receive a message from another agent."""
        self.message_queue.append(message)
        self.state.memory.append(message)

    def process_messages(self) -> List[Message]:
        """Process all queued messages and return responses."""
        responses = []
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self._handle_message(message)
            if response:
                responses.append(response)
        return responses

    def _handle_message(self, message: Message) -> Optional[Message]:
        """Handle a single message and generate response if needed."""
        # Check for custom handlers first
        if message.type.value in self.response_handlers:
            handler = self.response_handlers[message.type.value]
            return handler(message)
        
        # Default handling
        if message.type == MessageType.TASK:
            return self._process_task(message)
        elif message.type == MessageType.QUERY:
            return self._process_query(message)
        
        return None

    def _process_task(self, message: Message) -> Optional[Message]:
        """Process a task message."""
        # Override in subclasses
        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESULT,
            content="Task processed",
            parent_message_id=message.id,
        )

    def _process_query(self, message: Message) -> Optional[Message]:
        """Process a query message."""
        # Override in subclasses
        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content="Query processed",
            parent_message_id=message.id,
        )

    def get_memory(self) -> List[Dict[str, Any]]:
        """Get agent's memory as list of message dictionaries."""
        return [msg.to_dict() for msg in self.state.memory]

    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "id": self.state.id,
            "name": self.state.name,
            "role": self.state.role,
            "tools": list(self.state.tools.keys()),
            "message_count": len(self.state.memory),
            "execution_count": self.state.execution_count,
        }


class AgentManager:
    """Manages multiple agents and their communication."""

    def __init__(self):
        """Initialize the agent manager."""
        self.agents: Dict[str, Agent] = {}
        self.message_history: List[Message] = []
        self.execution_graph = None

    def register_agent(self, agent: Agent) -> None:
        """Register an agent with the manager."""
        self.agents[agent.state.name] = agent
        agent.agent_manager = self

    def route_message(self, message: Message) -> None:
        """Route a message to the appropriate agent."""
        self.message_history.append(message)
        
        if message.receiver in self.agents:
            receiver_agent = self.agents[message.receiver]
            receiver_agent.receive_message(message)

    def execute_agents(self, max_iterations: int = 10) -> Dict[str, Any]:
        """
        Execute all agents with message passing.
        
        Args:
            max_iterations: Maximum number of execution iterations
            
        Returns:
            Execution report
        """
        iteration = 0
        active_agents = True
        
        while active_agents and iteration < max_iterations:
            active_agents = False
            iteration += 1
            
            for agent in self.agents.values():
                if agent.message_queue:
                    active_agents = True
                    responses = agent.process_messages()
                    
                    for response in responses:
                        self.route_message(response)
                    
                    agent.state.execution_count += 1
        
        return {
            "iterations": iteration,
            "total_messages": len(self.message_history),
            "agent_stats": {name: agent.get_info() for name, agent in self.agents.items()},
        }

    def get_all_agents_info(self) -> List[Dict[str, Any]]:
        """Get information about all registered agents."""
        return [agent.get_info() for agent in self.agents.values()]

    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get all message history."""
        return [msg.to_dict() for msg in self.message_history]
