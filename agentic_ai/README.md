# Agentic AI System - Multi-Agent Orchestration Framework

A comprehensive Python framework for building intelligent multi-agent systems with agent-to-agent communication, tool usage, and graph-based workflow visualization.

## Overview

This system enables you to:
- **Create autonomous agents** with specific roles and capabilities
- **Enable agent-to-agent communication** through message passing
- **Register and use tools** for task execution
- **Visualize workflows** as interactive directed graphs
- **Coordinate complex multi-agent workflows** with a central coordinator
- **Track execution history** and message flows

## Architecture

### Core Components

#### 1. **Agent Framework** (`agent.py`)
The foundation of the system with:
- `Agent` - Base class for all agents
- `Message` - Message protocol for agent communication
- `Tool` - Tool/function wrapper for agent capabilities
- `AgentManager` - Centralized agent registry and message router
- `AgentState` - State management for agents

#### 2. **Tools System** (`tools.py`)
Pre-built reusable tools including:
- **Math Tools**: `calculate_expression`, `add_numbers`, `multiply_numbers`, `divide_numbers`
- **Analysis Tools**: `analyze_data`, `find_patterns`, `predict_trend`
- **Task Management**: `break_down_task`, `prioritize_tasks`
- **Simulation**: `simulate_process`
- **Information Retrieval**: `search_knowledge_base`, `extract_information`

#### 3. **Specialized Agents** (`specialized_agents.py`)
Domain-specific agents:
- **AnalyzerAgent** - Data analysis and pattern detection
- **PlannerAgent** - Task planning and prioritization
- **ExecutorAgent** - Task execution and calculations
- **CoordinatorAgent** - Inter-agent coordination
- **KnowledgeAgent** - Information management

#### 4. **Workflow Graph** (`workflow_graph.py`)
Graph-based workflow management:
- `WorkflowGraph` - Graph representation of multi-agent workflows
- `GraphNode` - Nodes representing agents, tasks, tools, or data
- `GraphEdge` - Edges representing relationships
- Visualization with matplotlib and NetworkX

## Installation

### Prerequisites
- Python 3.8+

### Setup

1. **Clone or navigate to the project**:
```bash
cd /workspaces/GithubCopilot
```

2. **Create virtual environment** (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from agentic_ai import (
    Agent, AgentManager, Tool, Message, MessageType,
    AnalyzerAgent, PlannerAgent
)

# Create manager
manager = AgentManager()

# Create agents
analyzer = AnalyzerAgent(manager)
planner = PlannerAgent(manager)

# Register agents
manager.register_agent(analyzer)
manager.register_agent(planner)

# Send message between agents
analyzer.send_message(
    receiver="Planner",
    content="Analyze and plan this task",
    msg_type=MessageType.QUERY,
    data={"tasks": ["Task 1", "Task 2", "Task 3"]}
)

# Execute
manager.execute_agents(max_iterations=5)
```

### Creating Custom Agents

```python
from agentic_ai import Agent, Tool, Message, MessageType

class CustomAgent(Agent):
    def __init__(self, agent_manager=None):
        super().__init__(
            name="CustomAgent",
            role="Custom Processing",
            agent_manager=agent_manager
        )
        self._register_tools()
    
    def _register_tools(self):
        def my_function(x, y):
            return x + y
        
        self.register_tool(Tool(
            name="my_tool",
            description="My custom tool",
            func=my_function,
            parameters={"x": "int", "y": "int"}
        ))
    
    def _handle_message(self, message):
        # Custom message handling
        result = self.use_tool("my_tool", x=5, y=3)
        return Message(
            sender=self.state.name,
            receiver=message.sender,
            type=MessageType.RESPONSE,
            content=f"Result: {result}",
            data=result,
            parent_message_id=message.id
        )
```

## Running Examples

### Run All Scenarios
```bash
python -m agentic_ai.main
```

This executes four comprehensive scenarios:
1. **Data Analysis Workflow** - Agents analyzing datasets
2. **Task Planning** - Breaking down and executing tasks
3. **Knowledge Coordination** - Sharing and coordinating knowledge
4. **Full Ecosystem** - All agents working together

### Output
- Console logs of agent interactions
- Message history
- PNG visualizations of workflow graphs
- JSON exports of workflow data

## Message Protocol

### Message Types
- `REQUEST` - Request for action
- `RESPONSE` - Response to a request
- `TASK` - Task assignment
- `RESULT` - Task result
- `ERROR` - Error notification
- `QUERY` - Information query

### Example Message
```python
Message(
    id="unique-id",
    sender="Agent1",
    receiver="Agent2",
    type=MessageType.QUERY,
    content="Analyze this data",
    data={
        "type": "full",
        "data": [1, 2, 3, 4, 5]
    },
    parent_message_id="parent-message-id"
)
```

## Workflow Graphs

### Creating and Visualizing Graphs

```python
from agentic_ai import WorkflowGraph, NodeType

# Create graph
workflow = WorkflowGraph("My Workflow")

# Add agent nodes
workflow.add_agent_node(agent1)
workflow.add_agent_node(agent2)

# Add task nodes
workflow.add_task_node("task_1", "Data Processing")

# Add edges
workflow.add_agent_task_assignment(agent1.state.id, "task_1")
workflow.add_agent_communication(agent1.state.id, agent2.state.id, message)

# Visualize
workflow.visualize(output_file="workflow.png", title="My Workflow")

# Print summary
workflow.print_summary()

# Export to JSON
data = workflow.export_to_dict()
```

### Graph Statistics
```python
stats = workflow.get_graph_statistics()
# Returns: {
#     "total_nodes": 5,
#     "total_edges": 8,
#     "agents": 2,
#     "tasks": 2,
#     "tools": 1,
#     "density": 0.4,
#     "message_flows": 3
# }
```

## File Structure

```
agentic_ai/
├── __init__.py              # Package initialization
├── agent.py                 # Core agent framework
├── tools.py                 # Reusable tools
├── specialized_agents.py    # Domain-specific agents
├── workflow_graph.py        # Graph visualization
├── main.py                  # Example scenarios
└── [outputs]
    ├── scenario_1_graph.png
    ├── scenario_2_graph.png
    ├── scenario_3_graph.png
    ├── scenario_4_graph.png
    ├── scenario_1_data.json
    ├── scenario_2_data.json
    ├── scenario_3_data.json
    └── scenario_4_data.json
```

## Features

### Agent Communication
- Message passing between agents
- Parent-child message tracking
- Message history and memory
- Custom response handlers

### Tool System
- Register tools with agents
- Tool execution with error handling
- Parameter validation
- Result tracking

### Graph Visualization
- NetworkX-based graph representation
- Different node types (agents, tasks, tools, data)
- Color-coded visualization
- Interactive layout
- Export to JSON

### Execution Management
- Centralized agent manager
- Message routing
- Iterative execution
- Execution statistics

## Advanced Features

### Custom Message Handlers
```python
agent.response_handlers["custom_type"] = custom_handler_function
```

### Finding Communication Paths
```python
path = workflow.get_communication_path("Agent1", "Agent2")
```

### Agent Connections
```python
connections = workflow.get_agent_connections(agent_id)
# Returns: {"outgoing": [...], "incoming": [...]}
```

## Best Practices

1. **Agent Design**
   - Keep agents focused on specific roles
   - Register relevant tools during initialization
   - Implement custom `_handle_message` methods

2. **Message Handling**
   - Always include parent_message_id for traceability
   - Use appropriate message types
   - Include structured data in message.data

3. **Tool Usage**
   - Create reusable, single-purpose tools
   - Provide clear descriptions
   - Handle exceptions gracefully

4. **Workflow Management**
   - Use WorkflowGraph for visualization
   - Export workflows for documentation
   - Track execution statistics

## Troubleshooting

### Agents Not Communicating
- Verify agents are registered with the same manager
- Check receiver agent name is correct
- Ensure agents are executed with `manager.execute_agents()`

### Tools Not Working
- Verify tool is registered with agent
- Check parameter types match
- Look for exceptions in use_tool() result

### Graph Visualization Issues
- Ensure matplotlib and networkx are installed
- Verify nodes and edges are properly added
- Check file permissions for output directory

## Examples

See `main.py` for four complete example scenarios:
1. **Data Analysis** - Statistical analysis of datasets
2. **Task Planning** - Decomposition and prioritization
3. **Knowledge Coordination** - Information sharing
4. **Full Ecosystem** - Comprehensive multi-agent workflow

## Performance Considerations

- Agent execution is iterative with configurable max iterations
- Message routing is O(1) with agent name lookup
- Graph operations depend on NetworkX implementation
- Visualization scales to ~100 agents efficiently

## Future Extensions

- LLM integration for natural language processing
- Persistent agent memory/database
- Distributed agent execution
- Real-time monitoring dashboard
- Advanced scheduling algorithms
- Multi-tier agent hierarchies

## Contributing

Contributions welcome! Areas for enhancement:
- Additional specialized agents
- More tool implementations
- Advanced workflow patterns
- Performance optimizations
- Testing suite

## License

MIT License - Feel free to use in your projects

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example scenarios
3. Check agent and tool docstrings
4. Examine message history for debugging

---

**Built with Python | Multi-Agent Architecture | NetworkX Graph Visualization**
