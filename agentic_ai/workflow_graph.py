"""
Graph-based workflow visualization and management.
"""
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
from .agent import Message, Agent


class NodeType(Enum):
    """Types of nodes in the workflow graph."""
    AGENT = "agent"
    TASK = "task"
    TOOL = "tool"
    DATA = "data"


@dataclass
class GraphNode:
    """Represents a node in the workflow graph."""
    id: str
    name: str
    type: NodeType
    data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class GraphEdge:
    """Represents an edge in the workflow graph."""
    source: str
    target: str
    edge_type: str
    weight: float = 1.0
    data: Dict[str, Any] = None


class WorkflowGraph:
    """Graph-based representation of multi-agent workflows."""

    def __init__(self, name: str = "Workflow"):
        """Initialize the workflow graph."""
        self.name = name
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.message_flows: List[Tuple[str, str, Message]] = []

    def add_node(self, node_id: str, name: str, node_type: NodeType, 
                 data: Dict[str, Any] = None, metadata: Dict[str, Any] = None) -> GraphNode:
        """Add a node to the graph."""
        node = GraphNode(
            id=node_id,
            name=name,
            type=node_type,
            data=data or {},
            metadata=metadata or {},
        )
        self.nodes[node_id] = node
        
        # Add to networkx graph
        self.graph.add_node(
            node_id,
            label=name,
            type=node_type.value,
            **node.data
        )
        
        return node

    def add_edge(self, source: str, target: str, edge_type: str, 
                 weight: float = 1.0, data: Dict[str, Any] = None) -> GraphEdge:
        """Add an edge to the graph."""
        edge = GraphEdge(
            source=source,
            target=target,
            edge_type=edge_type,
            weight=weight,
            data=data or {},
        )
        self.edges.append(edge)
        
        # Add to networkx graph
        self.graph.add_edge(source, target, weight=weight, edge_type=edge_type)
        
        return edge

    def add_agent_node(self, agent: Agent) -> GraphNode:
        """Add an agent as a node."""
        return self.add_node(
            node_id=agent.state.id,
            name=agent.state.name,
            node_type=NodeType.AGENT,
            data={
                "role": agent.state.role,
                "tool_count": len(agent.state.tools),
                "message_count": len(agent.state.memory),
            },
            metadata={
                "state_id": agent.state.id,
                "role": agent.state.role,
            }
        )

    def add_agent_communication(self, sender_id: str, receiver_id: str, message: Message) -> GraphEdge:
        """Record agent-to-agent communication."""
        edge = self.add_edge(
            source=sender_id,
            target=receiver_id,
            edge_type="communication",
            data={
                "message_type": message.type.value,
                "message_id": message.id,
                "content_preview": message.content[:50] if message.content else "",
            }
        )
        self.message_flows.append((sender_id, receiver_id, message))
        return edge

    def add_tool_usage(self, agent_id: str, tool_name: str) -> GraphEdge:
        """Record tool usage by an agent."""
        tool_node_id = f"tool_{tool_name}"
        
        # Add tool node if not exists
        if tool_node_id not in self.nodes:
            self.add_node(
                node_id=tool_node_id,
                name=tool_name,
                node_type=NodeType.TOOL,
            )
        
        return self.add_edge(
            source=agent_id,
            target=tool_node_id,
            edge_type="uses_tool",
            data={"tool": tool_name}
        )

    def add_task_node(self, task_id: str, task_name: str, task_data: Dict[str, Any] = None) -> GraphNode:
        """Add a task node."""
        return self.add_node(
            node_id=task_id,
            name=task_name,
            node_type=NodeType.TASK,
            data=task_data or {},
        )

    def add_agent_task_assignment(self, agent_id: str, task_id: str) -> GraphEdge:
        """Record agent-task assignment."""
        return self.add_edge(
            source=agent_id,
            target=task_id,
            edge_type="assigned_to",
        )

    def get_agent_connections(self, agent_id: str) -> Dict[str, List[str]]:
        """Get all connections for an agent."""
        successors = list(self.graph.successors(agent_id))
        predecessors = list(self.graph.predecessors(agent_id))
        
        return {
            "outgoing": successors,
            "incoming": predecessors,
        }

    def get_communication_path(self, source_agent_id: str, target_agent_id: str) -> Optional[List[str]]:
        """Find communication path between two agents."""
        try:
            path = nx.shortest_path(self.graph, source_agent_id, target_agent_id)
            return path
        except nx.NetworkXNoPath:
            return None

    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get statistics about the graph."""
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "agents": len([n for n in self.nodes.values() if n.type == NodeType.AGENT]),
            "tasks": len([n for n in self.nodes.values() if n.type == NodeType.TASK]),
            "tools": len([n for n in self.nodes.values() if n.type == NodeType.TOOL]),
            "density": nx.density(self.graph),
            "message_flows": len(self.message_flows),
        }

    def visualize(self, output_file: str = None, title: str = None) -> Optional[plt.Figure]:
        """
        Visualize the workflow graph.
        
        Args:
            output_file: Optional file path to save the visualization
            title: Optional title for the graph
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=42)
        
        # Separate nodes by type for different colors
        agent_nodes = [n for n in self.nodes.values() if n.type == NodeType.AGENT]
        task_nodes = [n for n in self.nodes.values() if n.type == NodeType.TASK]
        tool_nodes = [n for n in self.nodes.values() if n.type == NodeType.TOOL]
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph, pos,
            edge_color='gray',
            arrows=True,
            arrowsize=20,
            arrowstyle='->',
            width=1.5,
            ax=ax,
            connectionstyle="arc3,rad=0.1"
        )
        
        # Draw agent nodes
        agent_ids = [n.id for n in agent_nodes]
        nx.draw_networkx_nodes(
            self.graph, pos,
            nodelist=agent_ids,
            node_color='#FF6B6B',
            node_size=2000,
            node_shape='o',
            label='Agents',
            ax=ax
        )
        
        # Draw task nodes
        task_ids = [n.id for n in task_nodes]
        if task_ids:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=task_ids,
                node_color='#4ECDC4',
                node_size=1500,
                node_shape='s',
                label='Tasks',
                ax=ax
            )
        
        # Draw tool nodes
        tool_ids = [n.id for n in tool_nodes]
        if tool_ids:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=tool_ids,
                node_color='#95E1D3',
                node_size=1200,
                node_shape='^',
                label='Tools',
                ax=ax
            )
        
        # Draw labels
        labels = {n.id: n.name for n in self.nodes.values()}
        nx.draw_networkx_labels(
            self.graph, pos,
            labels,
            font_size=8,
            font_weight='bold',
            ax=ax
        )
        
        # Add title and legend
        if title is None:
            title = self.name
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.legend(scatterpoints=1, loc='upper left', fontsize=10)
        ax.axis('off')
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Graph saved to {output_file}")
        
        return fig

    def export_to_dict(self) -> Dict[str, Any]:
        """Export graph structure to dictionary."""
        return {
            "name": self.name,
            "nodes": [
                {
                    "id": node.id,
                    "name": node.name,
                    "type": node.type.value,
                    "data": node.data,
                    "metadata": node.metadata,
                }
                for node in self.nodes.values()
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "type": edge.edge_type,
                    "weight": edge.weight,
                    "data": edge.data,
                }
                for edge in self.edges
            ],
            "statistics": self.get_graph_statistics(),
        }

    def print_summary(self):
        """Print a summary of the graph."""
        stats = self.get_graph_statistics()
        
        print("\n" + "="*60)
        print(f"Workflow Graph: {self.name}")
        print("="*60)
        print(f"Total Nodes: {stats['total_nodes']}")
        print(f"  - Agents: {stats['agents']}")
        print(f"  - Tasks: {stats['tasks']}")
        print(f"  - Tools: {stats['tools']}")
        print(f"Total Edges: {stats['total_edges']}")
        print(f"Graph Density: {stats['density']:.4f}")
        print(f"Message Flows: {stats['message_flows']}")
        print("="*60)
        
        print("\nAgents:")
        for agent in [n for n in self.nodes.values() if n.type == NodeType.AGENT]:
            print(f"  - {agent.name} ({agent.data.get('tool_count', 0)} tools)")
        
        if any(n.type == NodeType.TASK for n in self.nodes.values()):
            print("\nTasks:")
            for task in [n for n in self.nodes.values() if n.type == NodeType.TASK]:
                print(f"  - {task.name}")
