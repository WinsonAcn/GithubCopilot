"""
Tools that agents can use to perform various tasks.
"""
import json
import math
from typing import Any, Dict, List


# ============================================================================
# Math and Calculation Tools
# ============================================================================

def calculate_expression(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression as string
        
    Returns:
        Result of the calculation
    """
    try:
        # Only allow safe operations
        safe_dict = {"__builtins__": {}}
        result = eval(expression, safe_dict)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


def add_numbers(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate_average(numbers: List[float]) -> float:
    """Calculate average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


# ============================================================================
# Data Analysis Tools
# ============================================================================

def analyze_data(data: List[float]) -> Dict[str, Any]:
    """
    Analyze a list of numbers and return statistics.
    
    Args:
        data: List of numbers to analyze
        
    Returns:
        Dictionary with statistics
    """
    if not data:
        raise ValueError("Cannot analyze empty data")
    
    sorted_data = sorted(data)
    n = len(data)
    
    return {
        "count": n,
        "sum": sum(data),
        "mean": sum(data) / n,
        "median": (sorted_data[n//2] if n % 2 else (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2),
        "min": min(data),
        "max": max(data),
        "range": max(data) - min(data),
    }


def find_patterns(data: List[float]) -> Dict[str, Any]:
    """Find patterns in a list of numbers."""
    if len(data) < 2:
        raise ValueError("Need at least 2 data points")
    
    diffs = [data[i+1] - data[i] for i in range(len(data)-1)]
    
    return {
        "differences": diffs,
        "avg_difference": sum(diffs) / len(diffs),
        "is_increasing": all(d >= 0 for d in diffs),
        "is_decreasing": all(d <= 0 for d in diffs),
    }


# ============================================================================
# Task Management Tools
# ============================================================================

def break_down_task(task_description: str, num_subtasks: int = 3) -> Dict[str, Any]:
    """
    Break down a complex task into subtasks.
    
    Args:
        task_description: Description of the task
        num_subtasks: Number of subtasks to create
        
    Returns:
        Dictionary with task breakdown
    """
    # Simple task decomposition logic
    subtasks = []
    keywords = ["analyze", "prepare", "execute", "review", "finalize", "optimize"]
    
    for i in range(min(num_subtasks, len(keywords))):
        subtasks.append({
            "id": i + 1,
            "title": f"{keywords[i].capitalize()} - Part of {task_description[:30]}...",
            "priority": (num_subtasks - i) / num_subtasks,
            "estimated_time": f"{(i + 1) * 10} minutes",
        })
    
    return {
        "original_task": task_description,
        "subtasks": subtasks,
        "total_subtasks": len(subtasks),
    }


def prioritize_tasks(tasks: List[str]) -> Dict[str, Any]:
    """
    Prioritize a list of tasks.
    
    Args:
        tasks: List of task descriptions
        
    Returns:
        Prioritized list of tasks
    """
    # Simple priority assignment based on keyword urgency
    urgency_keywords = {
        "urgent": 5,
        "critical": 5,
        "important": 4,
        "high": 4,
        "medium": 3,
        "low": 2,
        "minor": 1,
    }
    
    scored_tasks = []
    for task in tasks:
        score = 2  # Default priority
        for keyword, urgency in urgency_keywords.items():
            if keyword.lower() in task.lower():
                score = max(score, urgency)
                break
        scored_tasks.append({"task": task, "priority": score})
    
    sorted_tasks = sorted(scored_tasks, key=lambda x: x["priority"], reverse=True)
    
    return {
        "total_tasks": len(tasks),
        "prioritized_tasks": sorted_tasks,
    }


# ============================================================================
# Simulation and Prediction Tools
# ============================================================================

def simulate_process(steps: int, initial_value: float = 1.0, growth_rate: float = 0.1) -> Dict[str, Any]:
    """
    Simulate a process over time.
    
    Args:
        steps: Number of simulation steps
        initial_value: Starting value
        growth_rate: Growth rate per step
        
    Returns:
        Simulation results
    """
    values = [initial_value]
    for i in range(steps - 1):
        next_value = values[-1] * (1 + growth_rate)
        values.append(next_value)
    
    return {
        "steps": steps,
        "initial_value": initial_value,
        "growth_rate": growth_rate,
        "final_value": values[-1],
        "values": values,
        "total_growth": ((values[-1] - initial_value) / initial_value) * 100,
    }


def predict_trend(historical_data: List[float]) -> Dict[str, Any]:
    """
    Predict future trend based on historical data.
    
    Args:
        historical_data: Historical data points
        
    Returns:
        Trend prediction
    """
    if len(historical_data) < 2:
        raise ValueError("Need at least 2 data points")
    
    # Simple linear trend calculation
    n = len(historical_data)
    x_sum = sum(range(n))
    y_sum = sum(historical_data)
    xy_sum = sum(i * historical_data[i] for i in range(n))
    x2_sum = sum(i * i for i in range(n))
    
    slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
    intercept = (y_sum - slope * x_sum) / n
    
    # Predict next values
    next_predictions = []
    for i in range(1, 4):
        pred = intercept + slope * (n + i - 1)
        next_predictions.append(pred)
    
    return {
        "trend": "upward" if slope > 0 else "downward",
        "slope": slope,
        "intercept": intercept,
        "next_3_predictions": next_predictions,
    }


# ============================================================================
# Information Retrieval Tools
# ============================================================================

def search_knowledge_base(query: str, knowledge_base: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Search a knowledge base for information.
    
    Args:
        query: Search query
        knowledge_base: Optional knowledge base dictionary
        
    Returns:
        Search results
    """
    if knowledge_base is None:
        knowledge_base = {
            "agent": "An autonomous system that can think, communicate, and act",
            "tool": "A function or capability that an agent can use",
            "graph": "A structure showing connections between agents and tasks",
            "workflow": "A sequence of steps to accomplish a goal",
        }
    
    results = []
    query_lower = query.lower()
    
    for key, value in knowledge_base.items():
        if query_lower in key.lower() or query_lower in value.lower():
            results.append({
                "key": key,
                "value": value,
                "relevance": 0.9 if query_lower in key.lower() else 0.7,
            })
    
    return {
        "query": query,
        "result_count": len(results),
        "results": results,
    }


def extract_information(text: str, keywords: List[str]) -> Dict[str, Any]:
    """
    Extract specific information from text.
    
    Args:
        text: Text to analyze
        keywords: Keywords to look for
        
    Returns:
        Extracted information
    """
    extracted = {}
    text_lower = text.lower()
    
    for keyword in keywords:
        count = text_lower.count(keyword.lower())
        extracted[keyword] = {
            "found": count > 0,
            "count": count,
        }
    
    return {
        "text_length": len(text),
        "keywords_found": sum(1 for info in extracted.values() if info["found"]),
        "extracted": extracted,
    }


# ============================================================================
# Tool Registry
# ============================================================================

def get_all_tools() -> List[Dict[str, Any]]:
    """Get information about all available tools."""
    tools_info = [
        {
            "name": "calculate_expression",
            "category": "math",
            "description": "Safely evaluate a mathematical expression",
            "parameters": {"expression": "str"},
        },
        {
            "name": "analyze_data",
            "category": "analysis",
            "description": "Analyze a list of numbers and return statistics",
            "parameters": {"data": "List[float]"},
        },
        {
            "name": "break_down_task",
            "category": "task_management",
            "description": "Break down a complex task into subtasks",
            "parameters": {"task_description": "str", "num_subtasks": "int"},
        },
        {
            "name": "prioritize_tasks",
            "category": "task_management",
            "description": "Prioritize a list of tasks",
            "parameters": {"tasks": "List[str]"},
        },
        {
            "name": "simulate_process",
            "category": "simulation",
            "description": "Simulate a process over time",
            "parameters": {"steps": "int", "initial_value": "float", "growth_rate": "float"},
        },
        {
            "name": "search_knowledge_base",
            "category": "information",
            "description": "Search a knowledge base for information",
            "parameters": {"query": "str"},
        },
    ]
    return tools_info
