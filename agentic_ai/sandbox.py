"""
Main demonstration of the agentic AI system with multiple scenarios.
"""
import json
from agentic_ai.agent import AgentManager, MessageType
from agentic_ai.specialized_agents import (
    AnalyzerAgent,
    PlannerAgent,
    ExecutorAgent,
    CoordinatorAgent,
    KnowledgeAgent,
)
from agentic_ai.workflow_graph import WorkflowGraph


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def scenario_1_data_analysis():
    """Scenario 1: Multi-agent data analysis workflow."""
    print_header("SCENARIO 1: Data Analysis Workflow")
    
    # Create agent manager and agents
    manager = AgentManager()
    analyzer = AnalyzerAgent(manager)
    coordinator = CoordinatorAgent(manager)
    
    manager.register_agent(analyzer)
    manager.register_agent(coordinator)
    
    # Create workflow graph
    workflow = WorkflowGraph("Data Analysis Workflow")
    workflow.add_agent_node(analyzer)
    workflow.add_agent_node(coordinator)
    
    # Coordinator initiates analysis task
    print("\n1. Coordinator requesting data analysis...")
    coordinator.send_message(
        receiver="Analyzer",
        content="Analyze the following dataset",
        msg_type=MessageType.QUERY,
        data={
            "type": "full",
            "data": [10, 20, 15, 25, 30, 22, 28, 35, 32, 40]
        }
    )
    
    # Execute agents
    print("2. Executing agents...")
    execution_report = manager.execute_agents(max_iterations=5)
    
    print(f"\nExecution completed in {execution_report['iterations']} iterations")
    print(f"Total messages exchanged: {execution_report['total_messages']}")
    
    # Print agent statistics
    print("\nAgent Statistics:")
    for name, stats in execution_report['agent_stats'].items():
        print(f"\n  {name}:")
        print(f"    - Tools: {stats['tools']}")
        print(f"    - Messages: {stats['message_count']}")
        print(f"    - Executions: {stats['execution_count']}")
    
    # Record communications in graph
    for msg in manager.message_history:
        if msg.sender in [a.state.name for a in manager.agents.values()]:
            sender_agent = manager.agents.get(msg.sender)
            if sender_agent:
                workflow.add_agent_communication(
                    sender_agent.state.id,
                    manager.agents.get(msg.receiver).state.id if msg.receiver in manager.agents else "unknown",
                    msg
                )
    
    workflow.print_summary()
    return workflow

def main():
    """Run main demonstration scenarios."""
    scenario_1_data_analysis()
    # Additional scenarios can be added here