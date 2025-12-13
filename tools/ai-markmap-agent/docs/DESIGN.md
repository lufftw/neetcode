# AI Markmap Agent - Technical Design Document

> 本文件詳細說明系統的技術設計決策、LangGraph 實作細節、以及各模組的互動方式。

## 目錄

1. [設計原則](#設計原則)
2. [LangGraph 核心概念](#langgraph-核心概念)
3. [State 設計](#state-設計)
4. [Graph 結構](#graph-結構)
5. [Agent 設計模式](#agent-設計模式)
6. [記憶系統架構](#記憶系統架構)
7. [錯誤處理策略](#錯誤處理策略)
8. [效能優化](#效能優化)

---

## 設計原則

### 1. 可配置性 (Configurability)
- 所有參數皆可透過 YAML 配置
- 支援環境變數插值 (`${VAR_NAME}`)
- 熱重載配置（開發模式）

### 2. 可擴展性 (Extensibility)
- 新增 Agent 只需定義配置與 Prompt
- 支援自訂 Vector Store 實作
- 模組化設計便於替換元件

### 3. 可觀測性 (Observability)
- 完整的日誌記錄
- LangGraph Studio 可視化
- Checkpoint 支援中斷恢復

### 4. 可測試性 (Testability)
- Mock LLM 支援單元測試
- 獨立模組可單獨測試
- 整合測試覆蓋完整流程

---

## LangGraph 核心概念

### State + Graph 範式

```
┌─────────────────────────────────────────────────────────────────┐
│                        LangGraph 架構                           │
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

### 關鍵 API

| API | 用途 | 範例 |
|-----|------|------|
| `StateGraph(State)` | 建立有狀態的 Graph | `graph = StateGraph(MarkmapState)` |
| `add_node(name, func)` | 新增節點 | `graph.add_node("optimize", optimize_fn)` |
| `add_edge(from, to)` | 新增邊 | `graph.add_edge("a", "b")` |
| `add_conditional_edges()` | 條件路由 | 根據狀態決定下一步 |
| `compile(checkpointer)` | 編譯並啟用持久化 | `graph.compile(checkpointer=MemorySaver())` |

---

## State 設計

### MarkmapState 定義

```python
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages

class MarkmapState(TypedDict):
    """
    共享狀態 - 在所有節點間傳遞
    
    設計原則：
    1. 不可變性：每次更新返回新字典
    2. 可追蹤性：保留完整歷史
    3. 最小化：僅包含必要資訊
    """
    
    # ===== 輸入數據 =====
    metadata: Optional[dict]           # 全量 metadata（僅首次）
    ontology: Optional[dict]           # ontology 數據
    
    # ===== 第一階段產物 =====
    markmap_general_en: Optional[str]
    markmap_general_zh: Optional[str]
    markmap_specialist_en: Optional[str]
    markmap_specialist_zh: Optional[str]
    
    # ===== 流程狀態 =====
    current_round: int
    current_markmaps: List[str]
    
    # ===== 討論紀錄 =====
    # 使用 add_messages reducer 自動累積
    discussion_history: Annotated[List[dict], add_messages]
    round_summaries: List[str]
    
    # ===== 壓縮內容 =====
    compressed_discussion: Optional[str]
    compressed_metadata: Optional[str]
    
    # ===== 評斷結果 =====
    candidate_markmaps: List[dict]
    judge_evaluations: List[dict]
    final_selection: Optional[str]
    
    # ===== 輸出 =====
    final_html: Optional[str]
    
    # ===== 記憶 =====
    stm: dict
    ltm_context: Optional[str]
```

### Reducer 機制

LangGraph 使用 Reducer 處理狀態更新：

```python
# add_messages reducer 範例
# 自動將新訊息累積到歷史中

# 節點返回：
return {"discussion_history": [new_message]}

# State 更新後：
# discussion_history = [old_msg1, old_msg2, new_message]
```

---

## Graph 結構

### 完整 Graph 定義

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

### 條件路由邏輯

```python
def should_continue(state: MarkmapState) -> Literal["continue", "evaluate"]:
    """
    決定是否繼續優化
    
    條件：
    1. 未達最大輪數
    2. 上輪有顯著改進（可選）
    """
    config = load_config()
    max_rounds = config["workflow"]["optimization_rounds"]
    
    if state["current_round"] < max_rounds:
        return "continue"
    return "evaluate"
```

---

## Agent 設計模式

### Base Agent 抽象

```python
from abc import ABC, abstractmethod
from langchain_core.messages import HumanMessage

class BaseAgent(ABC):
    """所有 Agent 的基類"""
    
    def __init__(self, config: dict):
        self.config = config
        self.model = self._init_model()
        self.prompt = self._load_prompt()
    
    @abstractmethod
    def _init_model(self):
        """初始化 LLM"""
        pass
    
    def _load_prompt(self) -> str:
        """載入 Prompt 模板"""
        with open(self.config["prompt_path"], "r") as f:
            return f.read()
    
    @abstractmethod
    def execute(self, state: MarkmapState) -> dict:
        """執行 Agent 邏輯"""
        pass
```

### Optimizer Agent 認知模組

```python
class OptimizerAgent(BaseAgent):
    """
    優化者 Agent - 具備完整認知能力
    
    認知模組：
    1. Planning: 規劃優化目標
    2. Decomposition: 任務分解
    3. Reflection: 反思改進
    4. Memory: 記憶管理
    """
    
    def plan(self, state: MarkmapState) -> dict:
        """
        🧠 規劃模組
        
        輸入：當前 Markmap, LTM 上下文
        輸出：優化計劃
        """
        prompt = self._build_planning_prompt(state)
        response = self.model.invoke([HumanMessage(content=prompt)])
        return {"plan": response.content}
    
    def decompose(self, plan: str) -> List[dict]:
        """
        🧩 任務分解模組
        
        將優化計劃分解為：
        - 節點結構調整
        - 分類層次優化
        - 語義一致性檢查
        - 工程可讀性提升
        """
        prompt = self._build_decomposition_prompt(plan)
        response = self.model.invoke([HumanMessage(content=prompt)])
        return self._parse_subtasks(response.content)
    
    def reflect(self, previous_results: List[dict], state: MarkmapState) -> dict:
        """
        🔁 反思模組
        
        評估前一輪結果，調整策略
        """
        prompt = self._build_reflection_prompt(previous_results, state)
        response = self.model.invoke([HumanMessage(content=prompt)])
        return {"reflection": response.content}
    
    def execute(self, state: MarkmapState, other_opinions: List[str]) -> dict:
        """
        執行完整優化流程
        
        1. 從 LTM 檢索相關決策
        2. 規劃
        3. 分解任務
        4. 反思（非首輪）
        5. 執行優化
        6. 更新記憶
        """
        # 1. LTM 檢索
        ltm_context = query_ltm(state["current_markmaps"][0][:500])
        
        # 2. 規劃
        plan = self.plan(state)
        
        # 3. 分解
        subtasks = self.decompose(plan["plan"])
        
        # 4. 反思（非首輪）
        if state["current_round"] > 0:
            reflection = self.reflect(state["round_summaries"], state)
        
        # 5. 執行優化
        optimized = self._optimize(state, other_opinions, subtasks)
        
        # 6. 更新記憶
        update_stm(state["stm"], optimized)
        store_to_ltm(optimized)
        
        return optimized
```

---

## 記憶系統架構

### 短期記憶 (STM)

```python
class ShortTermMemory:
    """
    短期記憶 - 維護當前會話上下文
    
    特點：
    - In-memory 實作
    - FIFO 淘汰策略
    - 快速存取
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

### 長期記憶 (LTM)

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class LongTermMemory:
    """
    長期記憶 - 跨會話持久化
    
    特點：
    - Vector Store 實作
    - 語義搜尋
    - 持久化存儲
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
        """存儲決策到 LTM"""
        self.vectorstore.add_texts(
            texts=[content],
            metadatas=[metadata or {}]
        )
    
    def query(self, query: str, k: int = 5) -> List[str]:
        """語義搜尋相關決策"""
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
```

### 記憶整合流程

```
┌─────────────────────────────────────────────────────────────────┐
│                       記憶系統流程                               │
│                                                                 │
│   ┌─────────────┐                         ┌─────────────┐       │
│   │   Agent     │ ─── 查詢相關決策 ────► │    LTM      │       │
│   │             │ ◄── 返回上下文 ─────── │  (Vector)   │       │
│   └──────┬──────┘                         └─────────────┘       │
│          │                                                      │
│          │ 執行決策                                              │
│          ▼                                                      │
│   ┌─────────────┐                         ┌─────────────┐       │
│   │   Result    │ ─── 存入短期 ─────────► │    STM      │       │
│   │             │                         │  (Memory)   │       │
│   └──────┬──────┘                         └──────┬──────┘       │
│          │                                       │              │
│          │ 重要決策                               │ 會話結束    │
│          ▼                                       ▼              │
│   ┌─────────────┐                         ┌─────────────┐       │
│   │   Store to  │ ◄── 持久化 ──────────── │   Persist   │       │
│   │    LTM      │                         │    STM      │       │
│   └─────────────┘                         └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 錯誤處理策略

### 重試機制

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustLLMCall:
    """帶重試的 LLM 呼叫"""
    
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

### Checkpoint 恢復

```python
def resume_from_checkpoint(thread_id: str):
    """從 Checkpoint 恢復執行"""
    graph = build_graph()
    
    # 取得最新 checkpoint
    state = graph.get_state({"configurable": {"thread_id": thread_id}})
    
    if state.values:
        logger.info(f"Resuming from round {state.values['current_round']}")
        return graph.invoke(None, {"configurable": {"thread_id": thread_id}})
    else:
        logger.warning("No checkpoint found, starting fresh")
        return None
```

---

## 效能優化

### 1. 並行執行

```python
# 第一階段：4 個生成器並行
graph.add_edge(START, "gen_general_en")
graph.add_edge(START, "gen_general_zh")
graph.add_edge(START, "gen_specialist_en")
graph.add_edge(START, "gen_specialist_zh")

# LangGraph 自動並行執行無依賴的節點
```

### 2. 內容壓縮

```python
def compress_if_needed(state: MarkmapState) -> dict:
    """智慧壓縮 - 僅在必要時壓縮"""
    
    estimated_tokens = estimate_tokens(state["discussion_history"])
    threshold = config["workflow"]["max_tokens_before_compress"]
    
    if estimated_tokens > threshold:
        compressed = compress_content(state["discussion_history"])
        return {"compressed_discussion": compressed}
    
    return {}  # 不壓縮
```

### 3. 快取策略

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embedding(text: str) -> List[float]:
    """快取 embedding 結果"""
    return embeddings.embed_query(text)
```

### 4. 串流輸出

```python
async def stream_optimization(state: MarkmapState):
    """串流輸出優化過程"""
    async for event in graph.astream(state):
        yield event
```

---

## 附錄：設計決策記錄

| 決策 | 選項 | 選擇 | 原因 |
|------|------|------|------|
| 狀態管理 | Redux / Zustand / LangGraph State | LangGraph State | 與 Graph 緊密整合 |
| Vector Store | Chroma / Pinecone / FAISS | Chroma | 免費、本地、易部署 |
| 配置格式 | JSON / YAML / TOML | YAML | 可讀性好、支援註解 |
| 日誌框架 | logging / loguru | loguru | 更好的格式化 |

---

*Last updated: 2024-12*

