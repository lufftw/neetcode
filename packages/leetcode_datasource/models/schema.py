"""
Schema versioning for Question data model.

This module defines the schema version and provides migration utilities
for handling data format changes over time.
"""

from typing import Dict, Callable

# Current schema version
SCHEMA_VERSION = "1.0"

# Changelog for documentation
SCHEMA_CHANGELOG: Dict[str, str] = {
    "1.0": "Initial schema with LeetScrape-compatible fields",
    # "1.1": "Added new_field",  # Future example
}

# Migration functions: "from_version -> to_version" -> migration_func
SCHEMA_MIGRATIONS: Dict[str, Callable[[dict], dict]] = {
    # "1.0 -> 1.1": lambda data: {**data, "new_field": "default_value"},
}


def get_migration_path(from_version: str, to_version: str) -> list:
    """
    Get the list of migrations needed to upgrade from one version to another.
    
    Args:
        from_version: Starting schema version
        to_version: Target schema version
        
    Returns:
        List of migration keys in order
    """
    # For now, simple implementation - extend when needed
    if from_version == to_version:
        return []
    
    # TODO: Implement proper version comparison and migration path finding
    return []


def migrate_question_data(data: dict, from_version: str) -> dict:
    """
    Apply migrations to upgrade data to current schema.
    
    Args:
        data: Question data dictionary
        from_version: Version of the data
        
    Returns:
        Migrated data dictionary
    """
    if from_version == SCHEMA_VERSION:
        return data
    
    migration_path = get_migration_path(from_version, SCHEMA_VERSION)
    
    result = data.copy()
    for migration_key in migration_path:
        if migration_key in SCHEMA_MIGRATIONS:
            result = SCHEMA_MIGRATIONS[migration_key](result)
    
    result["_schema_version"] = SCHEMA_VERSION
    return result

