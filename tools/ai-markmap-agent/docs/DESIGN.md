# AI Markmap Agent - Technical Design Document

> This document details the system's technical design decisions, LangGraph implementation details, and how modules interact.

## Table of Contents

1. [Design Principles](#design-principles)
2. [LangGraph Core Concepts](#langgraph-core-concepts)
3. [State Design](#state-design)
4. [Graph Structure](#graph-structure)
5. [Agent Design Patterns](#agent-design-patterns)
6. [Memory System Architecture](#memory-system-architecture)
7. [Error Handling Strategies](#error-handling-strategies)
8. [Performance Optimization](#performance-optimization)

---

## Design Principles

### 1. Configurability
- All parameters configurable via YAML
- Support for environment variable interpolation (`${VAR_NAME}`)
- Hot-reload configuration (development mode)

### 2. Extensibility
- Adding new Agents only requires defining configuration and Prompt
- Support for custom Vector Store implementations
- Modular design for easy component replacement

### 3. Observability
- Complete logging
- LangGraph Studio visualization
- Checkpoint support for interruption recovery

### 4. Testability
- Mock LLM support for unit testing
- Independent modules can be tested separately
- Integration tests cover complete workflows

---

## LangGraph Core Concepts

### State + Graph Paradigm

```
┌─────────────────────────────────────────────────────────────────┐
│                        LangGraph Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   State (TypedDict)          Graph (StateGraph)                 │
│   ┌─────────────────┐        ┌─────────────────────────────┐   │
│   │ • metadata      │        │ Nodes:                      │   │
│   │ • markmaps      │ ────── │ • generate_generalist_en    │   │
│   │ • discussions   │        │ • generate_generalist_zh    │   │
│   │ • round_info    │        │ • optimize                  │   │
│   │ • memory        │        │ • summarize                 │   │
│   │ • final_output  │        │ • evaluate                  │   │
│   └─────────────────┘        │                             │   │
│                              │ Edges:                      │   │
│                              │ • START → generators        │   │
│                              │ • generators → collect      │   │
│                              │ • collect → optimize (loop) │   │
│                              │ • optimize → evaluate       │   │
│                              │ • evaluate → END            │   │
│                              └─────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key APIs

| API | Purpose | Example |
|-----|---------|---------|
| `StateGraph(State)` | Create a stateful Graph | `graph = StateGraph(MarkmapState)` |
| `add_node(name, func)` | Add a node | `graph.add_node("optimize", optimize_fn)` |
| `add_edge(from, to)` | Add an edge | `graph.add_edge("a", "b")` |
| `add_conditional_edges()` | Conditional routing | Decide next step based on state |
| `compile(checkpointer)` | Compile and enable persistence | `graph.compile(checkpointer=MemorySaver())` |

---

## State Design

### MarkmapState Definition

```python
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages

class MarkmapState(TypedDict):
    """
    Shared state - passed between all nodes
    
    Design principles:
    1. Immutability: Each update returns a new dictionary
    2. Traceability: Preserve complete history
    3. Minimalism: Only include necessary information
    """
    
    # ===== Input Data =====
    metadata: Optional[dict]           # Full metadata (first time only)
    ontology: Optional[dict]           # Ontology data
    
    # ===== Phase 1 Outputs =====
    markmap_general_en: Optional[str]
    markmap_general_zh: Optional[str]
    markmap_specialist_en: Optional[str]
    markmap_specialist_zh: Optional[str]
    
    # ===== Process State =====
    current_round: int
    current_markmaps: List[str]
    
    # ===== Discussion Records =====
    # Uses add_messages reducer to automatically accumulate
    discussion_history: Annotated[List[dict], add_messages]
    round_summaries: List[str]
    
    # ===== Compressed Content =====
    compressed_discussion: Optional[str]
    compressed_metadata: Optional[str]
    
    # ===== Evaluation Results =====
    candidate_markmaps: List[dict]
    judge_evaluations: List[dict]
    final_selection: Optional[str]
    
    # ===== Output =====
    final_html: Optional[str]
    
    # ===== Memory =====
    stm: dict
    ltm_context: Optional[str]
```

### Reducer Mechanism

LangGraph uses Reducers to handle state updates:

```python
# add_messages reducer example
# Automatically accumulates new messages into history

# Node returns:
return {"discussion_history": [new_message]}

# After state update:
# discussion_history = [old_msg1, old_msg2, new_message]
```

---

## Graph Structure

### Complete Graph Definition

```python
from langgraph.graph import StateGraph, START, END

def build_graph():
    graph = StateGraph(MarkmapState)
    
    # ===== Phase 1: Baseline Generation =====
    graph.add_node("gen_general_en", generate_generalist_en)
    graph.add_node("gen_general_zh", generate_generalist_zh)
    graph.add_node("gen_specialist_en", generate_specialist_en)
    graph.add_node("gen_specialist_zh", generate_specialist_zh)
    graph.add_node("collect", collect_baselines)
    
    # Parallel edges from START
    graph.add_edge(START, "gen_general_en")
    graph.add_edge(START, "gen_general_zh")
    graph.add_edge(START, "gen_specialist_en")
    graph.add_edge(START, "gen_specialist_zh")
    
    # All generators → collect
    graph.add_edge("gen_general_en", "collect")
    graph.add_edge("gen_general_zh", "collect")
    graph.add_edge("gen_specialist_en", "collect")
    graph.add_edge("gen_specialist_zh", "collect")
    
    # ===== Phase 2: Optimization Loop =====
    graph.add_node("compress", compress_if_needed)
    graph.add_node("optimize", run_optimization)
    graph.add_node("summarize", summarize_round)
    
    graph.add_edge("collect", "compress")
    graph.add_edge("compress", "optimize")
    graph.add_edge("optimize", "summarize")
    
    # Conditional: continue or evaluate
    graph.add_conditional_edges(
        "summarize",
        should_continue,
        {"continue": "compress", "evaluate": "evaluate"}
    )
    
    # ===== Phase 3: Final Evaluation =====
    graph.add_node("evaluate", run_evaluation)
    graph.add_node("convert", convert_to_html)
    
    graph.add_edge("evaluate", "convert")
    graph.add_edge("convert", END)
    
    return graph.compile(checkpointer=MemorySaver())
```

### Conditional Routing Logic

```python
def should_continue(state: MarkmapState) -> Literal["continue", "evaluate"]:
    """
    Decide whether to continue optimization
    
    Conditions:
    1. Maximum rounds not reached
    2. Significant improvement in previous round (optional)
    """
    config = load_config()
    max_rounds = config["workflow"]["optimization_rounds"]
    
    if state["current_round"] < max_rounds:
        return "continue"
    return "evaluate"
```

---

## Agent Design Patterns

### Base Agent Abstract

```python
from abc import ABC, abstractmethod
from langchain_core.messages import HumanMessage

class BaseAgent(ABC):
    """Base class for all Agents"""
    
    def __init__(self, config: dict):
        self.config = config
        self.model = self._init_model()
        self.prompt = self._load_prompt()
    
    @abstractmethod
    def _init_model(self):
        """Initialize LLM"""
        pass
    
    def _load_prompt(self) -> str:
        """Load Prompt template"""
        with open(self.config["prompt_path"], "r") as f:
            return f.read()
    
    @abstractmethod
    def execute(self, state: MarkmapState) -> dict:
        """Execute Agent logic"""
        pass
```

### Optimizer Agent Cognitive Modules

```python
class OptimizerAgent(BaseAgent):
    """
    Optimizer Agent - Full cognitive capabilities
    
    Cognitive modules:
    1. Planning: Plan optimization objectives
    2. Decomposition: Task decomposition
    3. Reflection: Reflect and improve
    4. Memory: Memory management
    """
    
    def plan(self, state: MarkmapState) -> dict:
        """
        🧠 Planning Module
        
        Input: Current Markmap, LTM context
        Output: Optimization plan
        """
        prompt = self._build_planning_prompt(state)
        response = self.model.invoke([HumanMessage(content=prompt)])
        return {"plan": response.content}
    
    def decompose(self, plan: str) -> List[dict]:
        """
        🧩 Task Decomposition Module
        
        Decompose optimization plan into:
        - Node structure adjustments
        - Classification hierarchy optimization
        - Semantic consistency checks
        - Engineering readability improvements
        """
        prompt = self._build_decomposition_prompt(plan)
        response = self.model.invoke([HumanMessage(content=prompt)])
        return self._parse_subtasks(response.content)
    
    def reflect(self, previous_results: List[dict], state: MarkmapState) -> dict:
        """
        🔁 Reflection Module
        
        Evaluate previous round results and adjust strategy
        """
        prompt = self._build_reflection_prompt(previous_results, state)
        response = self.model.invoke([HumanMessage(content=prompt)])
        return {"reflection": response.content}
    
    def execute(self, state: MarkmapState, other_opinions: List[str]) -> dict:
        """
        Execute complete optimization workflow
        
        1. Retrieve relevant decisions from LTM
        2. Plan
        3. Decompose tasks
        4. Reflect (if not first round)
        5. Execute optimization
        6. Update memory
        """
        # 1. LTM retrieval
        ltm_context = query_ltm(state["current_markmaps"][0][:500])
        
        # 2. Plan
        plan = self.plan(state)
        
        # 3. Decompose
        subtasks = self.decompose(plan["plan"])
        
        # 4. Reflect (if not first round)
        if state["current_round"] > 0:
            reflection = self.reflect(state["round_summaries"], state)
        
        # 5. Execute optimization
        optimized = self._optimize(state, other_opinions, subtasks)
        
        # 6. Update memory
        update_stm(state["stm"], optimized)
        store_to_ltm(optimized)
        
        return optimized
```

---

## Memory System Architecture

### Short-Term Memory (STM)

```python
class ShortTermMemory:
    """
    Short-Term Memory - Maintains current session context
    
    Features:
    - In-memory implementation
    - FIFO eviction strategy
    - Fast access
    """
    
    def __init__(self, max_items: int = 50):
        self.max_items = max_items
        self.memory: List[dict] = []
    
    def add(self, item: dict) -> None:
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "content": item
        })
        if len(self.memory) > self.max_items:
            self.memory.pop(0)  # FIFO
    
    def get_recent(self, n: int = 10) -> List[dict]:
        return self.memory[-n:]
    
    def search(self, keyword: str) -> List[dict]:
        return [m for m in self.memory if keyword in str(m["content"])]
```

### Long-Term Memory (LTM)

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class LongTermMemory:
    """
    Long-Term Memory - Cross-session persistence
    
    Features:
    - Vector Store implementation
    - Semantic search
    - Persistent storage
    """
    
    def __init__(self, config: dict):
        self.embeddings = OpenAIEmbeddings(
            model=config["embedding_model"]
        )
        self.vectorstore = Chroma(
            collection_name=config["collection_name"],
            embedding_function=self.embeddings,
            persist_directory=config["chromadb"]["persist_directory"]
        )
    
    def store(self, content: str, metadata: dict = None) -> None:
        """Store decision to LTM"""
        self.vectorstore.add_texts(
            texts=[content],
            metadatas=[metadata or {}]
        )
    
    def query(self, query: str, k: int = 5) -> List[str]:
        """Semantic search for relevant decisions"""
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
```

### Memory Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Memory System Flow                        │
│                                                                 │
│   ┌─────────────┐                         ┌─────────────┐       │
│   │   Agent     │ ─── Query relevant ───► │    LTM      │       │
│   │             │     decisions            │  (Vector)   │       │
│   │             │ ◄── Return context ────── │             │       │
│   └──────┬──────┘                         └─────────────┘       │
│          │                                                      │
│          │ Execute decision                                     │
│          ▼                                                      │
│   ┌─────────────┐                         ┌─────────────┐       │
│   │   Result    │ ─── Store to ─────────► │    STM      │       │
│   │             │     short-term            │  (Memory)   │       │
│   └──────┬──────┘                         └──────┬──────┘       │
│          │                                       │              │
│          │ Important decision                    │ Session end  │
│          ▼                                       ▼              │
│   ┌─────────────┐                         ┌─────────────┐       │
│   │   Store to  │ ◄── Persist ──────────── │   Persist   │       │
│   │    LTM      │                         │    STM      │       │
│   └─────────────┘                         └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Error Handling Strategies

### Retry Mechanism

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustLLMCall:
    """LLM call with retry"""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def invoke(self, messages: List[dict]) -> str:
        try:
            return self.model.invoke(messages)
        except RateLimitError:
            logger.warning("Rate limit hit, retrying...")
            raise
        except APIError as e:
            logger.error(f"API error: {e}")
            raise
```

### Checkpoint Recovery

```python
def resume_from_checkpoint(thread_id: str):
    """Resume execution from checkpoint"""
    graph = build_graph()
    
    # Get latest checkpoint
    state = graph.get_state({"configurable": {"thread_id": thread_id}})
    
    if state.values:
        logger.info(f"Resuming from round {state.values['current_round']}")
        return graph.invoke(None, {"configurable": {"thread_id": thread_id}})
    else:
        logger.warning("No checkpoint found, starting fresh")
        return None
```

---

## Performance Optimization

### 1. Parallel Execution

```python
# Phase 1: 4 generators in parallel
graph.add_edge(START, "gen_general_en")
graph.add_edge(START, "gen_general_zh")
graph.add_edge(START, "gen_specialist_en")
graph.add_edge(START, "gen_specialist_zh")

# LangGraph automatically executes independent nodes in parallel
```

### 2. Content Compression

```python
def compress_if_needed(state: MarkmapState) -> dict:
    """Smart compression - only compress when necessary"""
    
    estimated_tokens = estimate_tokens(state["discussion_history"])
    threshold = config["workflow"]["max_tokens_before_compress"]
    
    if estimated_tokens > threshold:
        compressed = compress_content(state["discussion_history"])
        return {"compressed_discussion": compressed}
    
    return {}  # No compression
```

### 3. Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embedding(text: str) -> List[float]:
    """Cache embedding results"""
    return embeddings.embed_query(text)
```

### 4. Streaming Output

```python
async def stream_optimization(state: MarkmapState):
    """Stream optimization process"""
    async for event in graph.astream(state):
        yield event
```

---

## Appendix: Design Decision Records

| Decision | Options | Choice | Reason |
|----------|---------|--------|--------|
| State Management | Redux / Zustand / LangGraph State | LangGraph State | Tight integration with Graph |
| Vector Store | Chroma / Pinecone / FAISS | Chroma | Free, local, easy to deploy |
| Config Format | JSON / YAML / TOML | YAML | Good readability, supports comments |
| Logging Framework | logging / loguru | loguru | Better formatting |

---

*Last updated: 2025-12-17

