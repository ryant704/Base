import tkinter as tk
from gui import OSRSAccountPlannerGUI
import networkx as nx
from skills import SKILLS
from quests import QUESTS
from utils.account_goals import QUEST_MILESTONES
from utils.chunking import calculate_time_based_chunks

# --- Function to Build Quest Dependency Graph ---
def build_quest_dependency_graph(quest_data):
    graph = nx.DiGraph()
    for quest_name, quest_info in quest_data.items():
        graph.add_node(quest_name)
        for prereq_quest in quest_info.get("quests", []):
            graph.add_edge(prereq_quest, quest_name)
    return graph

# --- Function to Get Doable Quests (Implementation Needed) ---
def get_doable_quests(quest_milestone, current_levels, quest_dependency_graph, completed_quests):
    """
    Determines which quests in a milestone are doable based on prerequisites and skill levels.
    """
    doable_quests = []
    for quest in quest_milestone:
        # Check if the quest is already completed
        if quest in completed_quests:
            continue

        # Check if all quest dependencies are met
        dependencies_met = all(
            prereq in completed_quests for prereq in quest_dependency_graph.predecessors(quest)
        )

        # Check if skill requirements are met
        skill_requirements_met = True
        if dependencies_met:
            for skill, level in QUESTS[quest].get("skills", {}).items():
                if current_levels.get(skill, 0) < level:
                    skill_requirements_met = False
                    break

        # Add the quest to the doable list if all conditions are met
        if dependencies_met and skill_requirements_met:
            doable_quests.append(quest)

    return doable_quests

# --- Function to Update Levels with Quest Rewards (Implementation Needed) ---
def update_levels_with_quest_rewards(current_levels, quest_name):
    """
    Updates the current levels based on the XP rewards from a completed quest.
    """
    quest_rewards = QUESTS.get(quest_name, {}).get("xp_rewards", {})
    for skill, xp_reward in quest_rewards.items():
        if skill in current_levels:
            current_levels[skill] = get_level_from_xp(XP_TABLE[current_levels[skill]] + xp_reward)

def all_skills_at_desired_level(current_levels, desired_levels):
    """Checks if all skills are at or above their desired levels."""
    for skill, desired_level in desired_levels.items():
        if current_levels.get(skill, 0) < desired_level:
            return False
    return True

if __name__ == "__main__":
    # Build Quest Dependency Graph
    quest_dependency_graph = build_quest_dependency_graph(QUESTS)

    # Initialize completed quests (you might load this from a save file later)
    completed_quests = []

    root = tk.Tk()
    gui = OSRSAccountPlannerGUI(root)

    # --- Plan Generation Logic (Illustrative) ---
    def generate_plan():
        # 1. Get user input (desired levels, selected methods, etc.) - from GUI
        desired_levels = {}  # Replace with logic to get from GUI
        method_vars = {}  # Replace with logic to get from GUI
        # ... (Get desired levels and method selections from the GUI)

        # 2. Initialize current levels (all to 1 at the start)
        current_levels = {skill: 1 for skill in SKILLS}

        plan = []  # Your plan data structure

        # 3. Main loop (iterate until all skills are at desired levels or other goals are met)
        quest_prioritization_factor = 0.7  # You can adjust this value
        while not all_skills_at_desired_level(current_levels, desired_levels):
            # --- Prioritize Quests ---
            milestone_key, next_quest_milestone = get_next_quest_milestone(completed_quests)
            if next_quest_milestone:
                doable_quests = get_doable_quests(
                    next_quest_milestone, current_levels, quest_dependency_graph, completed_quests
                )
                if doable_quests:
                    if random.random() < quest_prioritization_factor:  # Prioritize with some randomness
                        chosen_quest = random.choice(doable_quests)

                        # Add quest to plan
                        plan.append(f"Complete quest: {chosen_quest}")

                        # Update completed quests and current levels
                        completed_quests.append(chosen_quest)
                        update_levels_with_quest_rewards(current_levels, chosen_quest)
                        continue  # Move to the next iteration of the loop

            # --- Skill Training Chunk Selection ---
            # (Simplified logic - you'll need to refine this)
            available_skills = [skill for skill in current_levels if skill not in ["Attack", "Strength", "Defence"]]
            if available_skills:
                chosen_skill = random.choice(available_skills)  # Add more sophisticated selection logic here
            else:
                chosen_skill = random.choice(["Attack", "Strength", "Defence"])

            chunks = calculate_time_based_chunks(
                current_levels,
                desired_levels,
                chosen_skill,
                method_vars,
                completed_quests,
                quest_dependency_graph,
                quest_prioritization_factor
            )

            if chunks:
                chunk = chunks[0]  # Take the first chunk
                plan.append(f"Train {chunk['skill']} from level {chunk['start_level']} to {chunk['target_level']} using {chunk['method']} ({chunk['time']} minutes)")
                current_levels[chunk["skill"]] = chunk["target_level"]

        # --- Output the Plan ---
        # (Replace this with your logic to display the plan in the GUI)
        print(plan)

    # --- Add a Button to Trigger Plan Generation ---
    generate_button = tk.Button(root, text="Generate Plan", command=generate_plan)
    generate_button.pack()

    root.mainloop()