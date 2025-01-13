# chunking.py
import random
from xp_table import XP_TABLE
from skills import SKILLS
from account_goals import COMBAT_MILESTONES, TOTAL_LEVEL_MILESTONES, LEVEL_TIME_RANGES, SKILL_MILESTONES, QUEST_MILESTONES

def calculate_xp_needed(current_level, target_level):
    """Calculates the XP needed to reach a target level from a current level."""
    current_xp = XP_TABLE[current_level]
    target_xp = XP_TABLE[target_level]
    return target_xp - current_xp

def get_level_from_xp(xp):
    """Finds the level corresponding to a given XP amount."""
    for level, level_xp in XP_TABLE.items():
        if level_xp > xp:
            return level - 1
    return 99  # If XP is higher than the max in the table, return 99

def get_time_range(level):
    """Returns the appropriate time range based on the given level."""
    for level_range, time_range in LEVEL_TIME_RANGES.items():
        if level_range[0] <= level <= level_range[1]:
            return time_range
    return (240, 480)  # Default to 4-8 hours if level is outside defined ranges

def get_next_combat_milestone(current_levels):
    """Gets the next combat milestone that hasn't been reached yet."""
    for milestone, levels in COMBAT_MILESTONES.items():
        if any(current_levels[skill] < level for skill, level in levels.items()):
            return levels
    return None

def get_next_total_level_milestone(current_total_level):
    """Gets the next total level milestone that hasn't been reached yet."""
    for milestone, level in TOTAL_LEVEL_MILESTONES.items():
        if current_total_level < level:
            return level
    return None

def get_next_skill_milestone(skill, current_level):
    """
    Gets the next milestone for a given skill that hasn't been reached yet.
    """
    if skill in SKILL_MILESTONES:
        for milestone_level, description in SKILL_MILESTONES[skill].items():
            if current_level < milestone_level:
                return milestone_level, description
    return None, None

def get_next_quest_milestone(completed_quests):
    """Gets the next quest milestone that hasn't been fully completed."""
    for milestone_key, milestone_quests in QUEST_MILESTONES.items():
        if any(quest not in completed_quests for quest in milestone_quests):
            return milestone_key, milestone_quests
    return None, None

def calculate_time_based_chunks(current_levels, desired_levels, skill, method_vars, completed_quests, quest_dependency_graph, quest_prioritization_factor=0.7):
    """
    Calculates time-based chunks for a given skill, considering combat, 
    total level, and skill-specific milestones, with a preference for quests.
    """
    chunks = []
    current_level = current_levels[skill]
    total_level = sum(current_levels.values())

    # --- Prioritize Milestones ---
    # 1. Combat Milestones (if applicable)
    if skill in ["Attack", "Strength", "Defence"]:
        milestone_target = get_next_combat_milestone(current_levels)
        if milestone_target and current_level < milestone_target[skill]:
            desired_level = milestone_target[skill]
        else:
            desired_level = desired_levels[skill]
    else:
        desired_level = desired_levels[skill]

    # 2. Total Level Milestones (ONLY if specific skill goals are NOT set)
    if all(desired_levels.get(s, 1) == 1 for s in SKILLS) and desired_levels.get(skill, 1) == 1:
        next_total_level_milestone = get_next_total_level_milestone(total_level)
        if next_total_level_milestone:
            desired_level = min(99, current_level + 5)

    # --- Main Chunk Calculation Loop ---
    while current_level < desired_level:
        time_range = get_time_range(current_level)
        chunk_time = random.randint(*time_range)

        # --- Method Selection (Basic Framework) ---
        available_methods = []
        for method_name, method_data in SKILLS[skill]["methods"].items():
            if method_name == "default":
                for level_range, details in method_data.items():
                    min_level, max_level = map(int, level_range.split('-'))
                    if min_level <= current_level <= max_level:
                        if all(current_levels.get(req_skill, 0) >= req_level for req_skill, req_level in details.get("requirements", {}).items()):
                            available_methods.append((method_name, details["xp_per_hour"]))
            elif method_name in method_vars:
                if method_vars[method_name]["selected"].get() and current_level >= int(method_vars[method_name]["min"].get()) and current_level <= int(method_vars[method_name]["max"].get()):
                    if all(current_levels.get(req_skill, 0) >= req_level for req_skill, req_level in method_data.get("requirements", {}).items()):
                        available_methods.append((method_name, method_data["xp_per_hour"]))
        
        # Prioritize skill-specific milestone methods if applicable
        next_skill_milestone, _ = get_next_skill_milestone(skill, current_level)
        if next_skill_milestone:
            for method_name, xp_per_hour in available_methods:
                if method_name == SKILL_MILESTONES[skill].get(next_skill_milestone):
                    available_methods.insert(0, (method_name, xp_per_hour))  # Move to the front

        if not available_methods:
            print(f"No methods available for {skill} at level {current_level}")
            break

        # Choose a method (for now, pick the first available one after prioritization)
        chosen_method, xp_per_hour = available_methods[0]

        # --- Calculate XP and Target Level ---
        xp_gain = int((xp_per_hour / 60) * chunk_time)
        target_xp = min(XP_TABLE[current_level] + xp_gain, XP_TABLE.get(desired_level, XP_TABLE[99]))
        target_level = get_level_from_xp(target_xp)

        # --- Create Chunk Data ---
        chunks.append({
            "skill": skill,
            "start_level": current_level,
            "target_level": target_level,
            "start_xp": XP_TABLE[current_level],
            "target_xp": target_xp,
            "time": chunk_time,
            "method": chosen_method,
        })

        current_level = target_level

    return chunks