"""
Main demonstration of the agentic AI system with multiple scenarios.
"""
import json
from .agent import AgentManager, MessageType
from .specialized_agents import (
    AnalyzerAgent,
    PlannerAgent,
    ExecutorAgent,
    CoordinatorAgent,
    KnowledgeAgent,
)
from .workflow_graph import WorkflowGraph


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


def scenario_2_task_planning():
    """Scenario 2: Multi-agent task planning and execution."""
    print_header("SCENARIO 2: Task Planning and Execution")
    
    manager = AgentManager()
    planner = PlannerAgent(manager)
    executor = ExecutorAgent(manager)
    coordinator = CoordinatorAgent(manager)
    
    manager.register_agent(planner)
    manager.register_agent(executor)
    manager.register_agent(coordinator)
    
    workflow = WorkflowGraph("Task Planning Workflow")
    workflow.add_agent_node(planner)
    workflow.add_agent_node(executor)
    workflow.add_agent_node(coordinator)
    
    # Step 1: Request task breakdown
    print("\n1. Requesting task breakdown...")
    coordinator.send_message(
        receiver="Planner",
        content="Break down the data processing project",
        msg_type=MessageType.QUERY,
        data={
            "type": "breakdown",
            "task": "Build a machine learning model for customer churn prediction",
            "num_subtasks": 5
        }
    )
    
    # Step 2: Request task execution
    print("2. Requesting calculation task...")
    coordinator.send_message(
        receiver="Executor",
        content="Calculate financial metrics",
        msg_type=MessageType.QUERY,
        data={
            "type": "calculate",
            "expression": "100 * 0.15 + 50 * 0.25"
        }
    )
    
    print("3. Executing agents...")
    execution_report = manager.execute_agents(max_iterations=5)
    
    print(f"\nExecution completed in {execution_report['iterations']} iterations")
    print(f"Total messages exchanged: {execution_report['total_messages']}")
    
    # Record in graph
    for msg in manager.message_history:
        if msg.sender in [a.state.name for a in manager.agents.values()]:
            sender_agent = manager.agents.get(msg.sender)
            receiver_agent = manager.agents.get(msg.receiver)
            if sender_agent and receiver_agent:
                workflow.add_agent_communication(sender_agent.state.id, receiver_agent.state.id, msg)
    
    workflow.print_summary()
    return workflow


def scenario_3_knowledge_coordination():
    """Scenario 3: Knowledge sharing and complex coordination."""
    print_header("SCENARIO 3: Knowledge Coordination Workflow")
    
    manager = AgentManager()
    knowledge_agent = KnowledgeAgent(manager)
    analyzer = AnalyzerAgent(manager)
    planner = PlannerAgent(manager)
    
    manager.register_agent(knowledge_agent)
    manager.register_agent(analyzer)
    manager.register_agent(planner)
    
    workflow = WorkflowGraph("Knowledge Coordination Workflow")
    workflow.add_agent_node(knowledge_agent)
    workflow.add_agent_node(analyzer)
    workflow.add_agent_node(planner)
    
    # Knowledge queries
    print("\n1. Querying knowledge base...")
    analyzer.send_message(
        receiver="Knowledge",
        content="Search for multiagent information",
        msg_type=MessageType.QUERY,
        data={
            "type": "search",
            "query": "multiagent coordination"
        }
    )
    
    print("2. Requesting task planning with knowledge...")
    planner.send_message(
        receiver="Analyzer",
        content="Analyze workflow patterns",
        msg_type=MessageType.QUERY,
        data={
            "type": "patterns",
            "data": [1.0, 1.1, 1.21, 1.33, 1.46, 1.61, 1.77, 1.95, 2.14]
        }
    )
    
    print("3. Executing coordination...")
    execution_report = manager.execute_agents(max_iterations=5)
    
    print(f"\nExecution completed in {execution_report['iterations']} iterations")
    print(f"Total messages exchanged: {execution_report['total_messages']}")
    
    # Record in graph
    for msg in manager.message_history:
        if msg.sender in [a.state.name for a in manager.agents.values()]:
            sender_agent = manager.agents.get(msg.sender)
            receiver_agent = manager.agents.get(msg.receiver)
            if sender_agent and receiver_agent:
                workflow.add_agent_communication(sender_agent.state.id, receiver_agent.state.id, msg)
    
    workflow.print_summary()
    return workflow


def scenario_4_full_ecosystem():
    """Scenario 4: Complete multi-agent ecosystem."""
    print_header("SCENARIO 4: Full Multi-Agent Ecosystem")
    
    manager = AgentManager()
    
    # Create all types of agents
    analyzer = AnalyzerAgent(manager)
    planner = PlannerAgent(manager)
    executor = ExecutorAgent(manager)
    coordinator = CoordinatorAgent(manager)
    knowledge = KnowledgeAgent(manager)
    
    manager.register_agent(analyzer)
    manager.register_agent(planner)
    manager.register_agent(executor)
    manager.register_agent(coordinator)
    manager.register_agent(knowledge)
    
    workflow = WorkflowGraph("Full Ecosystem Workflow")
    
    # Add all agents to workflow
    for agent in [analyzer, planner, executor, coordinator, knowledge]:
        workflow.add_agent_node(agent)
        workflow.add_agent_node(agent)
    
    # Complex workflow: Coordinator orchestrates multiple agents
    print("\n1. Coordinator initiating complex workflow...")
    
    # Get knowledge first
    coordinator.send_message(
        receiver="Knowledge",
        content="Get workflow information",
        msg_type=MessageType.QUERY,
        data={
            "type": "search",
            "query": "workflow coordination"
        }
    )
    
    # Request analysis
    coordinator.send_message(
        receiver="Analyzer",
        content="Analyze quarterly performance data",
        msg_type=MessageType.QUERY,
        data={
            "type": "full",
            "data": [100, 120, 115, 140, 160, 155, 180, 200, 190, 210]
        }
    )
    
    # Request planning
    coordinator.send_message(
        receiver="Planner",
        content="Plan Q4 initiatives",
        msg_type=MessageType.QUERY,
        data={
            "type": "breakdown",
            "task": "Improve customer retention by 20%",
            "num_subtasks": 4
        }
    )
    
    # Request execution
    coordinator.send_message(
        receiver="Executor",
        content="Calculate growth projections",
        msg_type=MessageType.QUERY,
        data={
            "type": "simulate",
            "steps": 12,
            "initial_value": 1000,
            "growth_rate": 0.05
        }
    )
    
    print("2. Executing full ecosystem...")
    execution_report = manager.execute_agents(max_iterations=10)
    
    print(f"\nExecution completed in {execution_report['iterations']} iterations")
    print(f"Total messages exchanged: {execution_report['total_messages']}")
    
    # Record communications in graph
    for msg in manager.message_history:
        if msg.sender in [a.state.name for a in manager.agents.values()]:
            sender_agent = manager.agents.get(msg.sender)
            receiver_agent = manager.agents.get(msg.receiver)
            if sender_agent and receiver_agent:
                workflow.add_agent_communication(sender_agent.state.id, receiver_agent.state.id, msg)
    
    # Print detailed message history
    print("\nMessage History Summary:")
    for i, msg in enumerate(manager.message_history[:10], 1):
        print(f"  {i}. {msg.sender} → {msg.receiver}: {msg.content[:50]}")
    
    workflow.print_summary()
    return workflow


def main():
    """Run all scenarios and generate visualizations."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  AGENTIC AI SYSTEM - MULTI-AGENT ORCHESTRATION DEMO".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    workflows = []
    
    # Run scenarios
    workflows.append(("Scenario 1", scenario_1_data_analysis()))
    workflows.append(("Scenario 2", scenario_2_task_planning()))
    workflows.append(("Scenario 3", scenario_3_knowledge_coordination()))
    workflows.append(("Scenario 4", scenario_4_full_ecosystem()))
    
    # Generate visualizations
    print_header("Generating Visualizations")
    
    for scenario_name, workflow in workflows:
        output_file = f"/workspaces/GithubCopilot/agentic_ai/{scenario_name.lower().replace(' ', '_')}_graph.png"
        print(f"\nGenerating visualization for {scenario_name}...")
        try:
            workflow.visualize(
                output_file=output_file,
                title=f"{scenario_name}: {workflow.name}"
            )
            print(f"✓ Saved to {output_file}")
        except Exception as e:
            print(f"✗ Error generating visualization: {e}")
    
    # Export workflow data
    print_header("Exporting Workflow Data")
    
    for scenario_name, workflow in workflows:
        output_file = f"/workspaces/GithubCopilot/agentic_ai/{scenario_name.lower().replace(' ', '_')}_data.json"
        try:
            with open(output_file, 'w') as f:
                json.dump(workflow.export_to_dict(), f, indent=2, default=str)
            print(f"✓ {scenario_name} data exported to {output_file}")
        except Exception as e:
            print(f"✗ Error exporting {scenario_name}: {e}")
    
    # Summary
    print_header("Execution Summary")
    print("\n✓ All scenarios completed successfully!")
    print(f"✓ Generated {len(workflows)} workflow visualizations")
    print(f"✓ Generated {len(workflows)} workflow data files")
    print("\nKey Features Demonstrated:")
    print("  • Agent-to-agent communication with message passing")
    print("  • Tool registration and execution by agents")
    print("  • Graph-based workflow visualization")
    print("  • Message history and state tracking")
    print("  • Multi-agent coordination and orchestration")
    print("  • Complex task decomposition and planning")
    
    print("\nGenerated Files:")
    print("  • agent.py - Core agent framework")
    print("  • tools.py - Reusable tools and functions")
    print("  • specialized_agents.py - Domain-specific agents")
    print("  • workflow_graph.py - Graph visualization")
    print("  • main.py - Scenarios and demonstrations")
    print("\n")


if __name__ == "__main__":
    main()
