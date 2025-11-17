#!/usr/bin/env python3
"""
Quick Start Guide and Interactive Demo for Agentic AI System

This script provides an interactive walkthrough of the system's capabilities.
"""

from agentic_ai import (
    Agent, AgentManager, Tool, Message, MessageType,
    AnalyzerAgent, PlannerAgent, ExecutorAgent,
    CoordinatorAgent, KnowledgeAgent
)
from agentic_ai.workflow_graph import WorkflowGraph
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_1_basic_agent_communication():
    """Demo 1: Basic agent-to-agent communication."""
    print_section("DEMO 1: Basic Agent Communication")
    
    print("\nCreating agents...")
    manager = AgentManager()
    agent1 = AnalyzerAgent(manager)
    agent2 = PlannerAgent(manager)
    
    manager.register_agent(agent1)
    manager.register_agent(agent2)
    
    print(f"✓ Created Analyzer Agent: {agent1.state.name}")
    print(f"✓ Created Planner Agent: {agent2.state.name}")
    
    print("\nAgent 1 sending message to Agent 2...")
    msg_id = agent1.send_message(
        receiver="Planner",
        content="Please analyze this task breakdown",
        msg_type=MessageType.QUERY,
        data={"type": "breakdown", "task": "Develop new feature"}
    )
    print(f"✓ Message sent (ID: {msg_id})")
    
    print("\nExecuting agents (2 iterations)...")
    report = manager.execute_agents(max_iterations=2)
    
    print(f"✓ Execution complete:")
    print(f"  - Iterations: {report['iterations']}")
    print(f"  - Messages: {report['total_messages']}")


def demo_2_tool_usage():
    """Demo 2: Agents using tools."""
    print_section("DEMO 2: Tool Usage by Agents")
    
    manager = AgentManager()
    executor = ExecutorAgent(manager)
    manager.register_agent(executor)
    
    print(f"\n{executor.state.name} registered tools:")
    for tool_name in executor.state.tools:
        print(f"  • {tool_name}")
    
    print("\nExecuting a calculation tool...")
    result = executor.use_tool("calculate_expression", expression="2**10 + 3*5")
    print(f"✓ Result: {result}")
    
    print("\nExecuting a simulation tool...")
    result = executor.use_tool(
        "simulate_process",
        steps=5,
        initial_value=100,
        growth_rate=0.1
    )
    print(f"✓ Simulation completed:")
    print(f"  - Initial: {result['result']['initial_value']}")
    print(f"  - Final: {result['result']['final_value']:.2f}")
    print(f"  - Growth: {result['result']['total_growth']:.2f}%")


def demo_3_agent_info():
    """Demo 3: Accessing agent information."""
    print_section("DEMO 3: Agent Information and State")
    
    manager = AgentManager()
    analyzer = AnalyzerAgent(manager)
    manager.register_agent(analyzer)
    
    info = analyzer.get_info()
    
    print(f"\nAnalyzer Agent Information:")
    print(f"  - ID: {info['id']}")
    print(f"  - Name: {info['name']}")
    print(f"  - Role: {info['role']}")
    print(f"  - Tools: {len(info['tools'])}")
    print(f"    {info['tools']}")
    print(f"  - Messages: {info['message_count']}")
    print(f"  - Executions: {info['execution_count']}")


def demo_4_complex_workflow():
    """Demo 4: Complex multi-agent workflow."""
    print_section("DEMO 4: Complex Workflow")
    
    manager = AgentManager()
    
    # Create diverse agents
    analyzer = AnalyzerAgent(manager)
    planner = PlannerAgent(manager)
    executor = ExecutorAgent(manager)
    knowledge = KnowledgeAgent(manager)
    
    manager.register_agent(analyzer)
    manager.register_agent(planner)
    manager.register_agent(executor)
    manager.register_agent(knowledge)
    
    print(f"\nRegistered {len(manager.agents)} agents:")
    for name in manager.agents:
        print(f"  • {name}")
    
    # Analyzer requests knowledge
    print("\n1. Analyzer queries Knowledge agent...")
    analyzer.send_message(
        receiver="Knowledge",
        content="What is multiagent?",
        msg_type=MessageType.QUERY,
        data={"type": "search", "query": "multiagent"}
    )
    
    # Planner requests analysis
    print("2. Planner requests data analysis...")
    planner.send_message(
        receiver="Analyzer",
        content="Analyze performance data",
        msg_type=MessageType.QUERY,
        data={
            "type": "full",
            "data": [10, 15, 12, 20, 25, 22, 28, 30]
        }
    )
    
    # Executor runs simulation
    print("3. Executor runs simulation...")
    executor.send_message(
        receiver="Executor",
        content="Run growth simulation",
        msg_type=MessageType.QUERY,
        data={
            "type": "simulate",
            "steps": 6,
            "initial_value": 1000,
            "growth_rate": 0.15
        }
    )
    
    print("\nExecuting workflow (5 iterations)...")
    report = manager.execute_agents(max_iterations=5)
    
    print(f"\n✓ Workflow complete:")
    print(f"  - Iterations: {report['iterations']}")
    print(f"  - Total messages: {report['total_messages']}")
    
    print(f"\nAgent execution summary:")
    for name, stats in report['agent_stats'].items():
        print(f"  {name}:")
        print(f"    - Executions: {stats['execution_count']}")
        print(f"    - Messages: {stats['message_count']}")


def demo_5_workflow_visualization():
    """Demo 5: Workflow graph visualization."""
    print_section("DEMO 5: Workflow Visualization")
    
    manager = AgentManager()
    agent1 = AnalyzerAgent(manager)
    agent2 = ExecutorAgent(manager)
    
    manager.register_agent(agent1)
    manager.register_agent(agent2)
    
    # Create workflow graph
    workflow = WorkflowGraph("Demo Workflow")
    workflow.add_agent_node(agent1)
    workflow.add_agent_node(agent2)
    
    # Add communication
    msg = Message(
        sender=agent1.state.name,
        receiver=agent2.state.name,
        type=MessageType.QUERY
    )
    workflow.add_agent_communication(agent1.state.id, agent2.state.id, msg)
    
    # Get statistics
    stats = workflow.get_graph_statistics()
    
    print(f"\nWorkflow Graph Statistics:")
    print(f"  - Nodes: {stats['total_nodes']}")
    print(f"  - Edges: {stats['total_edges']}")
    print(f"  - Agents: {stats['agents']}")
    print(f"  - Density: {stats['density']:.4f}")
    
    print(f"\nExporting workflow data...")
    data = workflow.export_to_dict()
    print(f"✓ Exported:")
    print(f"  - Nodes: {len(data['nodes'])}")
    print(f"  - Edges: {len(data['edges'])}")
    
    print(f"\nGenerating visualization...")
    try:
        workflow.visualize(
            output_file="/tmp/demo_workflow.png",
            title="Demo Workflow Graph"
        )
        print(f"✓ Visualization saved to /tmp/demo_workflow.png")
    except Exception as e:
        print(f"✗ Could not save visualization: {e}")


def demo_6_message_history():
    """Demo 6: Message history and tracing."""
    print_section("DEMO 6: Message History & Tracing")
    
    manager = AgentManager()
    agent1 = AnalyzerAgent(manager)
    agent2 = PlannerAgent(manager)
    
    manager.register_agent(agent1)
    manager.register_agent(agent2)
    
    # Exchange messages
    agent1.send_message(
        receiver="Planner",
        content="Please break down this project",
        msg_type=MessageType.QUERY,
        data={"type": "breakdown", "task": "Build ML model"}
    )
    
    manager.execute_agents(max_iterations=2)
    
    # Get message history
    history = manager.get_message_history()
    
    print(f"\nMessage History ({len(history)} messages):")
    for i, msg in enumerate(history, 1):
        print(f"\n  {i}. {msg['sender']} → {msg['receiver']}")
        print(f"     Type: {msg['type']}")
        print(f"     Content: {msg['content'][:50]}...")
        if msg['parent_message_id']:
            print(f"     Parent: {msg['parent_message_id'][:8]}...")


def main():
    """Run all demos."""
    print("\n" + "█"*70)
    print("█  AGENTIC AI SYSTEM - QUICK START & INTERACTIVE DEMO".center(70) + "█")
    print("█"*70)
    
    demos = [
        ("Basic Agent Communication", demo_1_basic_agent_communication),
        ("Tool Usage", demo_2_tool_usage),
        ("Agent Information", demo_3_agent_info),
        ("Complex Workflow", demo_4_complex_workflow),
        ("Workflow Visualization", demo_5_workflow_visualization),
        ("Message History", demo_6_message_history),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print_section("All Demos Completed!")
    print("\nKey Takeaways:")
    print("  ✓ Agents can communicate with each other")
    print("  ✓ Agents can use registered tools")
    print("  ✓ Workflows can be visualized as graphs")
    print("  ✓ Message history is tracked automatically")
    print("  ✓ Complex multi-agent systems can be orchestrated")
    
    print("\nNext Steps:")
    print("  1. Review agentic_ai/README.md for detailed documentation")
    print("  2. Check agentic_ai/main.py for full scenarios")
    print("  3. Create custom agents by extending Agent class")
    print("  4. Register tools specific to your use case")
    print("  5. Use WorkflowGraph to visualize your workflows")
    print("\n")


if __name__ == "__main__":
    main()
