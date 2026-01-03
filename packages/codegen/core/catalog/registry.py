"""
Catalog registry - metadata only.

Maps names to template locations and provides metadata about each helper.
Does NOT contain the actual template content (that lives in templates/).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class HelperCategory(Enum):
    """Category of helper."""
    CLASS = "class"
    STRUCT_FUNC = "struct"      # Tier-1: structure conversion
    SEMANTIC_FUNC = "semantic"  # Tier-1.5: semantic conversion


class Tier(Enum):
    """Tier level for helpers."""
    TIER_1 = "1"
    TIER_1_5 = "1.5"


@dataclass
class HelperMeta:
    """Metadata for a helper class or function."""
    name: str
    category: HelperCategory
    tier: Tier
    module_path: str  # Relative path within templates/
    depends_on: List[str] = None  # Other helpers this depends on
    description: str = ""
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []


# =============================================================================
# Class Registry
# =============================================================================

CLASS_REGISTRY: Dict[str, HelperMeta] = {
    "ListNode": HelperMeta(
        name="ListNode",
        category=HelperCategory.CLASS,
        tier=Tier.TIER_1,
        module_path="classes/ListNode.py",
        description="Singly linked list node",
    ),
    "TreeNode": HelperMeta(
        name="TreeNode",
        category=HelperCategory.CLASS,
        tier=Tier.TIER_1,
        module_path="classes/TreeNode.py",
        description="Binary tree node",
    ),
    "Node": HelperMeta(
        name="Node",
        category=HelperCategory.CLASS,
        tier=Tier.TIER_1_5,
        module_path="classes/Node.py",
        description="Linked list node with random pointer",
    ),
    "NodeGraph": HelperMeta(
        name="NodeGraph",
        category=HelperCategory.CLASS,
        tier=Tier.TIER_1_5,
        module_path="classes/NodeGraph.py",
        description="Graph node with neighbors",
    ),
    "NodeNary": HelperMeta(
        name="NodeNary",
        category=HelperCategory.CLASS,
        tier=Tier.TIER_1_5,
        module_path="classes/NodeNary.py",
        description="N-ary tree node",
    ),
    "DoublyListNode": HelperMeta(
        name="DoublyListNode",
        category=HelperCategory.CLASS,
        tier=Tier.TIER_1_5,
        module_path="classes/DoublyListNode.py",
        description="Doubly linked list node",
    ),
}


# =============================================================================
# Struct Function Registry (Tier-1)
# =============================================================================

STRUCT_FUNC_REGISTRY: Dict[str, HelperMeta] = {
    "list_to_linkedlist": HelperMeta(
        name="list_to_linkedlist",
        category=HelperCategory.STRUCT_FUNC,
        tier=Tier.TIER_1,
        module_path="functions/struct/list_to_linkedlist.py",
        depends_on=["ListNode"],
        description="Convert list to LinkedList",
    ),
    "linkedlist_to_list": HelperMeta(
        name="linkedlist_to_list",
        category=HelperCategory.STRUCT_FUNC,
        tier=Tier.TIER_1,
        module_path="functions/struct/linkedlist_to_list.py",
        description="Convert LinkedList to list",
    ),
    "list_to_tree": HelperMeta(
        name="list_to_tree",
        category=HelperCategory.STRUCT_FUNC,
        tier=Tier.TIER_1,
        module_path="functions/struct/list_to_tree.py",
        depends_on=["TreeNode"],
        description="Convert list to Binary Tree",
    ),
    "tree_to_list": HelperMeta(
        name="tree_to_list",
        category=HelperCategory.STRUCT_FUNC,
        tier=Tier.TIER_1,
        module_path="functions/struct/tree_to_list.py",
        description="Convert Binary Tree to list",
    ),
}


# =============================================================================
# Semantic Function Registry (Tier-1.5)
# =============================================================================

SEMANTIC_FUNC_REGISTRY: Dict[str, HelperMeta] = {
    "build_list_with_cycle": HelperMeta(
        name="build_list_with_cycle",
        category=HelperCategory.SEMANTIC_FUNC,
        tier=Tier.TIER_1_5,
        module_path="functions/semantic/build_list_with_cycle.py",
        depends_on=["ListNode"],
        description="Build linked list with cycle",
    ),
    "node_to_index": HelperMeta(
        name="node_to_index",
        category=HelperCategory.SEMANTIC_FUNC,
        tier=Tier.TIER_1_5,
        module_path="functions/semantic/node_to_index.py",
        description="Find node index in array",
    ),
    "build_intersecting_lists": HelperMeta(
        name="build_intersecting_lists",
        category=HelperCategory.SEMANTIC_FUNC,
        tier=Tier.TIER_1_5,
        module_path="functions/semantic/build_intersecting_lists.py",
        depends_on=["ListNode"],
        description="Build two intersecting lists",
    ),
    "build_random_pointer_list": HelperMeta(
        name="build_random_pointer_list",
        category=HelperCategory.SEMANTIC_FUNC,
        tier=Tier.TIER_1_5,
        module_path="functions/semantic/build_random_pointer_list.py",
        depends_on=["Node"],
        description="Build list with random pointers",
    ),
    "encode_random_pointer_list": HelperMeta(
        name="encode_random_pointer_list",
        category=HelperCategory.SEMANTIC_FUNC,
        tier=Tier.TIER_1_5,
        module_path="functions/semantic/encode_random_pointer_list.py",
        description="Encode random pointer list to pairs",
    ),
}


# =============================================================================
# Combined Registry
# =============================================================================

def get_all_registries() -> Dict[str, HelperMeta]:
    """Get combined registry of all helpers."""
    combined = {}
    combined.update(CLASS_REGISTRY)
    combined.update(STRUCT_FUNC_REGISTRY)
    combined.update(SEMANTIC_FUNC_REGISTRY)
    return combined


def get_helper_meta(name: str) -> Optional[HelperMeta]:
    """Get metadata for a helper by name."""
    all_reg = get_all_registries()
    return all_reg.get(name)


def list_by_category(category: HelperCategory) -> List[str]:
    """List all helper names in a category."""
    all_reg = get_all_registries()
    return [name for name, meta in all_reg.items() if meta.category == category]


def list_by_tier(tier: Tier) -> List[str]:
    """List all helper names in a tier."""
    all_reg = get_all_registries()
    return [name for name, meta in all_reg.items() if meta.tier == tier]


def get_dependencies(name: str) -> List[str]:
    """Get transitive dependencies for a helper."""
    meta = get_helper_meta(name)
    if not meta:
        return []
    
    deps = set()
    to_process = list(meta.depends_on)
    
    while to_process:
        dep = to_process.pop()
        if dep not in deps:
            deps.add(dep)
            dep_meta = get_helper_meta(dep)
            if dep_meta:
                to_process.extend(dep_meta.depends_on)
    
    return list(deps)

