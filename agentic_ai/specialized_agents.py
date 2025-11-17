"""
Specialized agent implementations with tool usage and inter-agent communication.
"""
from typing import Any, Dict, Optional
from .agent import Agent, Message, MessageType, Tool
from . import tools


class AnalyzerAgent(Agent):
    """Agent specialized in data analysis and pattern recognition."""

    def __init__(self, agent_manager=None):
        super().__init__(name="Analyzer", role="Data Analysis and Pattern Detection", agent_manager=agent_manager)
        self._register_tools()
        self.response_handlers["query"] = self._handle_analysis_query

    def _register_tools(self):
        """Register analysis tools."""
        self.register_tool(Tool(
            name="analyze_data",
            description="Analyze numerical data for statistics",
            func=tools.analyze_data,
            parameters={"data": "List[float]"}
        ))
        self.register_tool(Tool(
            name="find_patterns",
            description="Find patterns in data",
            func=tools.find_patterns,
            parameters={"data": "List[float]"}
        ))
        self.register_tool(Tool(
            name="predict_trend",
            description="Predict future trend from historical data",
            func=tools.predict_trend,
            parameters={"historical_data": "List[float]"}
        ))

    def _handle_analysis_query(self, message: Message) -> Optional[Message]:
        """Handle analysis queries from other agents."""
        data = message.data.get("data", [])
        analysis_type = message.data.get("type", "full")

        response_data = {}
        
        try:
            if analysis_type == "full" or analysis_type == "statistics":
                response_data["statistics"] = self.use_tool("analyze_data", data=data)
            
            if analysis_type == "full" or analysis_type == "patterns":
                response_data["patterns"] = self.use_tool("find_patterns", data=data)
            
            if analysis_type == "full" or analysis_type == "trend":
                response_data["trend"] = self.use_tool("predict_trend", historical_data=data)
        except Exception as e:
            return Message(
                sender=self.state.name,
                receiver=message.sender,
                type=MessageType.ERROR,
                content=f"Analysis error: {str(e)}",
                data={"error": str(e)},
                parent_message_id=message.id,
            )

        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content="Analysis complete",
            data=response_data,
            parent_message_id=message.id,
        )


class PlannerAgent(Agent):
    """Agent specialized in task planning and prioritization."""

    def __init__(self, agent_manager=None):
        super().__init__(name="Planner", role="Task Planning and Prioritization", agent_manager=agent_manager)
        self._register_tools()
        self.response_handlers["query"] = self._handle_planning_query

    def _register_tools(self):
        """Register planning tools."""
        self.register_tool(Tool(
            name="break_down_task",
            description="Break down complex tasks into subtasks",
            func=tools.break_down_task,
            parameters={"task_description": "str", "num_subtasks": "int"}
        ))
        self.register_tool(Tool(
            name="prioritize_tasks",
            description="Prioritize tasks by importance",
            func=tools.prioritize_tasks,
            parameters={"tasks": "List[str]"}
        ))

    def _handle_planning_query(self, message: Message) -> Optional[Message]:
        """Handle planning queries from other agents."""
        planning_type = message.data.get("type", "breakdown")
        
        try:
            if planning_type == "breakdown":
                task = message.data.get("task")
                num_subtasks = message.data.get("num_subtasks", 3)
                result = self.use_tool("break_down_task", task_description=task, num_subtasks=num_subtasks)
            elif planning_type == "prioritize":
                tasks = message.data.get("tasks", [])
                result = self.use_tool("prioritize_tasks", tasks=tasks)
            else:
                return Message(
                    sender=self.state.name,
                    receiver=message.sender,
                    type=MessageType.ERROR,
                    content=f"Unknown planning type: {planning_type}",
                    parent_message_id=message.id,
                )
        except Exception as e:
            return Message(
                sender=self.state.name,
                receiver=message.sender,
                type=MessageType.ERROR,
                content=f"Planning error: {str(e)}",
                parent_message_id=message.id,
            )

        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content="Planning complete",
            data=result,
            parent_message_id=message.id,
        )


class ExecutorAgent(Agent):
    """Agent specialized in executing tasks and calculations."""

    def __init__(self, agent_manager=None):
        super().__init__(name="Executor", role="Task Execution and Calculation", agent_manager=agent_manager)
        self._register_tools()
        self.response_handlers["query"] = self._handle_execution_query

    def _register_tools(self):
        """Register execution tools."""
        self.register_tool(Tool(
            name="calculate_expression",
            description="Evaluate mathematical expressions",
            func=tools.calculate_expression,
            parameters={"expression": "str"}
        ))
        self.register_tool(Tool(
            name="simulate_process",
            description="Simulate processes over time",
            func=tools.simulate_process,
            parameters={"steps": "int", "initial_value": "float", "growth_rate": "float"}
        ))

    def _handle_execution_query(self, message: Message) -> Optional[Message]:
        """Handle execution queries from other agents."""
        execution_type = message.data.get("type", "calculate")
        
        try:
            if execution_type == "calculate":
                expression = message.data.get("expression")
                result = self.use_tool("calculate_expression", expression=expression)
            elif execution_type == "simulate":
                steps = message.data.get("steps", 10)
                initial_value = message.data.get("initial_value", 1.0)
                growth_rate = message.data.get("growth_rate", 0.1)
                result = self.use_tool("simulate_process", steps=steps, initial_value=initial_value, growth_rate=growth_rate)
            else:
                return Message(
                    sender=self.state.name,
                    receiver=message.sender,
                    type=MessageType.ERROR,
                    content=f"Unknown execution type: {execution_type}",
                    parent_message_id=message.id,
                )
        except Exception as e:
            return Message(
                sender=self.state.name,
                receiver=message.sender,
                type=MessageType.ERROR,
                content=f"Execution error: {str(e)}",
                parent_message_id=message.id,
            )

        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content="Execution complete",
            data=result,
            parent_message_id=message.id,
        )


class CoordinatorAgent(Agent):
    """Agent that coordinates between other agents."""

    def __init__(self, agent_manager=None):
        super().__init__(name="Coordinator", role="Inter-Agent Coordination", agent_manager=agent_manager)
        self.response_handlers["query"] = self._handle_coordination_query
        self.active_workflows = {}

    def _handle_coordination_query(self, message: Message) -> Optional[Message]:
        """Handle coordination queries."""
        workflow_id = message.data.get("workflow_id", "workflow_1")
        tasks = message.data.get("tasks", [])
        
        # Store workflow
        self.active_workflows[workflow_id] = {
            "tasks": tasks,
            "status": "coordinating",
            "completed_tasks": [],
        }
        
        # Delegate to appropriate agents
        for task in tasks:
            self._delegate_task(task, workflow_id)
        
        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content=f"Workflow {workflow_id} initialized",
            data={"workflow_id": workflow_id, "task_count": len(tasks)},
            parent_message_id=message.id,
        )

    def _delegate_task(self, task: Dict[str, Any], workflow_id: str):
        """Delegate a task to the appropriate agent."""
        task_type = task.get("type", "analyze")
        target_agent = "Analyzer"
        
        if task_type == "analyze":
            target_agent = "Analyzer"
        elif task_type == "plan":
            target_agent = "Planner"
        elif task_type == "execute":
            target_agent = "Executor"
        
        self.send_message(
            receiver=target_agent,
            content=f"Task for workflow {workflow_id}",
            msg_type=MessageType.QUERY,
            data={"task": task, "workflow_id": workflow_id},
        )

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow."""
        return self.active_workflows.get(workflow_id, {"status": "not found"})


class KnowledgeAgent(Agent):
    """Agent that manages knowledge and information retrieval."""

    def __init__(self, agent_manager=None):
        super().__init__(name="Knowledge", role="Information Management", agent_manager=agent_manager)
        self._register_tools()
        self.knowledge_base = self._initialize_knowledge_base()
        self.response_handlers["query"] = self._handle_knowledge_query

    def _register_tools(self):
        """Register knowledge tools."""
        self.register_tool(Tool(
            name="search_knowledge_base",
            description="Search for information in knowledge base",
            func=lambda query: tools.search_knowledge_base(query, self.knowledge_base),
            parameters={"query": "str"}
        ))
        self.register_tool(Tool(
            name="extract_information",
            description="Extract specific information from text",
            func=tools.extract_information,
            parameters={"text": "str", "keywords": "List[str]"}
        ))

    def _initialize_knowledge_base(self) -> Dict[str, str]:
        """Initialize the knowledge base."""
        return {
            "agent": "An autonomous system that perceives, thinks, communicates, and acts",
            "tool": "A capability or function that enables agents to perform tasks",
            "graph": "A structure representing relationships between agents and tasks",
            "workflow": "A coordinated sequence of steps to accomplish goals",
            "multiagent": "Multiple agents working together to solve complex problems",
            "communication": "Message passing between agents for coordination",
            "coordination": "Mechanism to synchronize actions between multiple agents",
        }

    def _handle_knowledge_query(self, message: Message) -> Optional[Message]:
        """Handle knowledge queries from other agents."""
        query_type = message.data.get("type", "search")
        
        try:
            if query_type == "search":
                query = message.data.get("query")
                result = self.use_tool("search_knowledge_base", query=query)
            elif query_type == "extract":
                text = message.data.get("text")
                keywords = message.data.get("keywords", [])
                result = self.use_tool("extract_information", text=text, keywords=keywords)
            else:
                result = {"error": f"Unknown query type: {query_type}"}
        except Exception as e:
            return Message(
                sender=self.state.name,
                receiver=message.sender,
                type=MessageType.ERROR,
                content=f"Knowledge error: {str(e)}",
                parent_message_id=message.id,
            )

        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content="Query processed",
            data=result,
            parent_message_id=message.id,
        )
