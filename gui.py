import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from quests import QUESTS
from skills import SKILLS
from utils.weights import calculate_weights
import random

def generate_plan():
    plan = []
    error_messages = []
    current_levels = {skill: 1 for skill in SKILLS}  # Start at level 1 for all skills

    # Get the tasks from the user's selections
    tasks = []
    for skill, var in skill_vars.items():
        target_level = var.get()
        if target_level:
            tasks.append({"type": "skill", "name": skill, "level": int(target_level)})

    for quest_key, var in quest_vars.items():
        if var.get():
            tasks.append({"type": "quest", "name": quest_key})

    # Sort tasks based on dependencies
    ordered_tasks = []
    while tasks:
        added = False
        for task in tasks:
            if task["type"] == "quest":
                quest_data = QUESTS[task["name"]]
                can_add = True
                for dep in quest_data.get("quests", []):
                    if {"type": "quest", "name": dep} not in ordered_tasks:
                        can_add = False
                        break
                if can_add:
                    ordered_tasks.append(task)
                    tasks.remove(task)
                    added = True
            elif task["type"] == "skill":
                skill_name = task["name"]
                
                # Use default method if specific method is not selected
                if not any(method_vars.get(skill_name, {}).get(m, {}).get("selected", False) for m in method_vars.get(skill_name, {})):
                    method = "default"
                else:
                    # Find the selected method
                    for m, data in method_vars.get(skill_name, {}).items():
                        if isinstance(data, dict) and data.get("selected", False):
                            method = m
                            break
                
                can_add = True
                
                # Check skill requirements for the chosen method
                for method_data in SKILLS[skill_name]["methods"].values():
                    if method == method_data.get("name", "").lower():
                        if "requirements" in method_data:
                            for req_skill, req_level in method_data["requirements"].items():
                                if req_skill in current_levels and current_levels[req_skill] < req_level:
                                    can_add = False
                                    error_messages.append(f"Error: '{method}' requires {req_skill.capitalize()} level {req_level} but current level is {current_levels[req_skill]}.")
                                    break
                        break
                
                if can_add:
                    ordered_tasks.append(task)
                    tasks.remove(task)
                    added = True
            
            if not added:
                # If a task couldn't be added due to unmet dependencies or missing method
                error_messages.append(f"Error: Unable to add task '{task['name']}' due to unmet dependencies or invalid method selection.")
                tasks.remove(task)
                added = True

    # Display errors if any
    if error_messages:
        error_text.delete("1.0", tk.END)
        for msg in error_messages:
            error_text.insert(tk.END, msg + "\n")
        return
    
    # Generate plan steps based on ordered tasks
    for task in ordered_tasks:
        if task["type"] == "skill":
            skill = task["name"]
            target_level = task["level"]

            # Check if a specific method is selected for the skill
            if skill.lower() in method_vars:
                for method_name, method_data in method_vars[skill.lower()].items():
                    if method_name == "selected":
                        continue

                    if isinstance(method_data, dict) and method_data.get("selected", False):
                        chosen_method = method_name
                        break
                else:
                    # If no specific method is selected, use the default method
                    chosen_method = SKILLS[skill.lower()]["default_method"]
            else:
                # If the skill is not in method_vars, use the default method
                chosen_method = SKILLS[skill.lower()]["default_method"]

            # Determine valid methods and their weights
            valid_methods = []
            weights = {}
            
            if chosen_method == "agility" and method_vars["Agility"]["selected"].get():
                valid_methods = [
                    method
                    for method in method_vars["Agility"]
                    if method != "selected" and method_vars["Agility"][method].get()
                ]
                weights = {method: int(method_vars["Agility"][method].get() or 0) for method in valid_methods}
            elif chosen_method in combat_methods and method_vars[chosen_method]["selected"].get():
                valid_methods = [
                    skill for skill, settings in method_vars[chosen_method].items() if isinstance(settings, dict) and settings["selected"].get()
                ]
                weights = {
                    skill: int(settings["weight"].get() or 0)
                    for skill in valid_methods
                    if isinstance(settings, dict) and "weight" in settings and settings["selected"].get()
                }
            else:
                # Use the default method
                valid_methods = [chosen_method]
                weights = {chosen_method: 1}

            # Calculate weights, apply bonuses, and consider milestones
            weights = calculate_weights(current_levels, method_vars, skill, chosen_method)

            # Select a method based on weights
            total_weight = sum(weights.values())
            random_choice = random.uniform(0, total_weight)
            cumulative_weight = 0
            chosen_method = None
            
            for method, weight in weights.items():
                cumulative_weight += weight
                if random_choice <= cumulative_weight:
                    chosen_method = method
                    break

            # Update plan
            plan.append(f"Train {skill} to level {current_levels[skill] + 1} using {chosen_method}")

            # Increment the current level
            current_levels[skill] += 1

        # ... (Handle quest tasks)

    # Display the plan
    output_text.delete("1.0", tk.END)
    for step in plan:
        output_text.insert(tk.END, step + "\n")
    error_text.delete("1.0", tk.END)

def copy_to_clipboard():
    """Placeholder for the copy to clipboard logic."""
    output_text.insert(tk.END, "Plan copied to clipboard!\n")

def validate_input(P):
    """Validation function for skill entry boxes."""
    if str.isdigit(P) or P == "":
        if P == "" or 1 <= int(P) <= 99:
            return True

    return False

def open_agility_methods():
    """Opens a new window for selecting specific Agility courses."""
    agility_methods_window = tk.Toplevel(root)
    agility_methods_window.title("Agility Training Methods")

    # Center the agility methods window
    agility_methods_window.update_idletasks()
    screen_width = agility_methods_window.winfo_screenwidth()
    screen_height = agility_methods_window.winfo_screenheight()
    window_width = agility_methods_window.winfo_width()
    window_height = agility_methods_window.winfo_height()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    agility_methods_window.geometry(f"+{x}+{y}")

    # Set transient property to keep window on top
    agility_methods_window.transient(root)

    for method in SKILLS["agility"]["methods"]:
        if method != "default":
            method_var = tk.BooleanVar(value=False)
            method_vars["Agility"][method] = method_var
            tk.Checkbutton(agility_methods_window, text=method.capitalize(), variable=method_var).pack(anchor="w")

def open_combat_methods(method_name):
    """Opens a new window for selecting skills and setting min/max levels for a combat method."""
    if method_name in open_combat_windows and open_combat_windows[method_name].winfo_exists():
        open_combat_windows[method_name].lift()
        return

    combat_methods_window = tk.Toplevel(root)
    combat_methods_window.title(f"{method_name} Training Methods")

    # Set transient property to keep window on top
    combat_methods_window.transient(root)

    # Center the combat methods window
    combat_methods_window.update_idletasks()
    screen_width = combat_methods_window.winfo_screenwidth()
    screen_height = combat_methods_window.winfo_screenheight()
    window_width = combat_methods_window.winfo_width()
    window_height = combat_methods_window.winfo_height()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    combat_methods_window.geometry(f"+{x}+{y}")

    skills = {
        "Crab": ["Attack", "Strength", "Defence", "Ranged", "Longranged"],
        "Nmz": ["Attack", "Strength", "Defence", "Ranged"],
        "Rat": ["Attack", "Strength", "Defence", "Ranged", "Longranged"],
        "Slay": ["Attack", "Strength", "Defence", "Ranged", "Longranged"],
        "Cannon": ["Ranged"]
    }

    # Create labels for "Min", "Max", and "Weight" columns
    tk.Label(combat_methods_window, text="Min").grid(row=0, column=1, padx=2, pady=2)
    tk.Label(combat_methods_window, text="Max").grid(row=0, column=2, padx=2, pady=2)
    tk.Label(combat_methods_window, text="Weight").grid(row=0, column=3, padx=2, pady=2)

    row = 1
    for skill in skills.get(method_name, []):
        # Ensure the skill dictionary exists
        if skill not in method_vars[method_name]:
            method_vars[method_name][skill] = {}

        # Use existing variable if it exists
        if "selected" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["selected"] = tk.BooleanVar(value=False)
        
        method_checkbutton = tk.Checkbutton(combat_methods_window, text=skill, variable=method_vars[method_name][skill]["selected"])
        method_checkbutton.grid(row=row, column=0, sticky="w", padx=2, pady=2)

        # Create and store StringVar variables for min, max, and weight levels
        if "min" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["min"] = tk.StringVar()
        if "max" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["max"] = tk.StringVar()
        if "weight" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["weight"] = tk.StringVar()

        # Add entry boxes for min, max, and weight levels
        tk.Entry(combat_methods_window, textvariable=method_vars[method_name][skill]["min"], width=3, validate="key", validatecommand=vcmd).grid(row=row, column=1, padx=2, pady=2)
        tk.Entry(combat_methods_window, textvariable=method_vars[method_name][skill]["max"], width=3, validate="key", validatecommand=vcmd).grid(row=row, column=2, padx=2, pady=2)
        tk.Entry(combat_methods_window, textvariable=method_vars[method_name][skill]["weight"], width=3, validate="key", validatecommand=vcmd).grid(row=row, column=3, padx=2, pady=2)

        row += 1

    # Add a save button
    save_button = tk.Button(combat_methods_window, text="Save", command=lambda: save_combat_methods(method_name, combat_methods_window))
    save_button.grid(row=row, column=0, columnspan=4, pady=5)

    # Keep track of open windows
    open_combat_windows[method_name] = combat_methods_window

def save_combat_methods(method_name, window):
    """Saves the combat method settings, performs validation, and checks requirements."""
    error_messages = []  # Store error messages for display in a single message box

    # Mapping from method name to required skills
    method_requirements = {
        "Rat": {"Attack": 50, "Strength": 50, "Ranged": 50, "Defence": 40, "Longranged": 40},
        "Nmz": {"Attack": 60, "Strength": 60, "Ranged": 50, "Defence": 40},
        "Crab": {},
        "Slay": {},
        "Cannon": {}
    }

    for skill, settings in method_vars[method_name].items():
        if isinstance(settings, dict) and settings["selected"].get():
            min_level_str = settings["min"].get()
            max_level_str = settings["max"].get()
            weight_str = settings["weight"].get()  # Get the weight value

            # Check if min, max, and weight are provided
            if not min_level_str or not max_level_str or not weight_str:
                error_messages.append(f"Min, Max, and Weight values must be set for {method_name} - {skill}.\n")
                continue

            try:
                min_level = int(min_level_str)
                max_level = int(max_level_str)
                weight = int(weight_str)  # Convert weight to integer
            except ValueError:
                error_messages.append(f"Min, Max, and Weight values must be integers for {method_name} - {skill}.\n")
                continue

            if min_level < 1 or max_level > 99:
                error_messages.append(f"Min and Max levels must be between 1 and 99 for {method_name} - {skill}.\n")
                continue

            if min_level > max_level:
                error_messages.append(f"Min level cannot be greater than Max level for {method_name} - {skill}.\n")
                continue

            # Check against requirements
            if method_name in method_requirements:
                for req_skill, req_level in method_requirements[method_name].items():
                    if skill.lower() == req_skill.lower() and min_level < req_level:
                        error_messages.append(f"{method_name} requires {req_skill} level {req_level} (You set Min: {min_level}).\n")
                        break

            # Store weight in method_vars
            settings["weight"] = weight_str

    if error_messages:
        # Display a single error message box with all errors
        messagebox.showerror("Error", "\n".join(error_messages))
    else:
        window.destroy()  # Close the window only if there are no errors

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, wraplength=300, justify="left")
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = None

root = tk.Tk()
root.title("OSRS Account Planner")

# --- Skills Frame ---
skills_frame = tk.LabelFrame(root, text="Skills")
skills_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

skill_vars = {}
method_vars = {}
row = 0
col = 0
vcmd = (root.register(validate_input), '%P')

skills_order = [
    "Agility", "Hunter", "Mining", "Smithing", "Herblore", "Thieving",
    "Construction", "Farming", "Runecrafting", "Woodcutting", "Fishing", "Fletching",
    "Cooking", "Firemaking", "Crafting", "Prayer", "Magic", "Attack", "Strength", "Defence", "Ranged"
]

for skill in skills_order:
    if skill.lower() in SKILLS:
        skill_vars[skill] = tk.StringVar()
        method_vars[skill] = {}

        skill_label = tk.Label(skills_frame, text=skill)
        skill_label.grid(row=row, column=col, sticky="w", padx=2)

        skill_entry = tk.Entry(skills_frame, textvariable=skill_vars[skill], width=3, validate="key", validatecommand=vcmd)
        skill_entry.grid(row=row, column=col + 1, padx=2, pady=2)

        row += 1
        if row > (len(skills_order) - 1) / 2:
            row = 0
            col += 2

# --- Training Methods Frame ---
methods_frame = tk.LabelFrame(root, text="Training Methods")
methods_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Initialize method_vars
for method in ["Agility", "Crab", "Nmz", "Rat", "Slay", "Cannon", "Fruit"]:
    method_vars[method] = {}

method_row = 0

# Special handling for Agility
method_vars["Agility"]["selected"] = tk.BooleanVar(value=False)
agility_checkbox = tk.Checkbutton(methods_frame, variable=method_vars["Agility"]["selected"], command=open_agility_methods)
agility_checkbox.grid(row=method_row, column=0, sticky="w", padx=2, pady=2)

agility_button = tk.Button(methods_frame, text="Agility Methods", command=open_agility_methods)
agility_button.grid(row=method_row, column=1, sticky="w", padx=2, pady=2)
method_row += 1

# Combat methods
combat_methods = ["Crab", "Nmz", "Rat", "Slay", "Cannon"]
for method in combat_methods:
    method_vars[method]["selected"] = tk.BooleanVar(value=False)
    method_checkbox = tk.Checkbutton(methods_frame, variable=method_vars[method]["selected"], command=lambda m=method: open_combat_methods(m))
    method_checkbox.grid(row=method_row, column=0, sticky="w", padx=2, pady=2)

    method_button = tk.Button(methods_frame, text=method, command=lambda m=method: open_combat_methods(m))
    method_button.grid(row=method_row, column=1, sticky="w", padx=2, pady=2)
    method_row += 1

# Fruit method (Thieving)
method_vars["Fruit"]["selected"] = tk.BooleanVar(value=False)
fruit_checkbox = tk.Checkbutton(methods_frame, variable=method_vars["Fruit"]["selected"])
fruit_checkbox.grid(row=method_row, column=0, sticky="w", padx=2, pady=2)

fruit_label = tk.Label(methods_frame, text="Fruit (Thieving)")
fruit_label.grid(row=method_row, column=1, sticky="w", padx=2, pady=2)
method_row += 1

# Dictionary to track open combat method windows
open_combat_windows = {}

# --- Quests Frame ---
quests_frame = tk.LabelFrame(root, text="Quests")
quests_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

quest_vars = {}
row = 0
col = 0
for quest_key, quest_data in QUESTS.items():
    quest_vars[quest_key] = tk.BooleanVar(value=False)
    quest_checkbutton = tk.Checkbutton(quests_frame, text=quest_data["name"], variable=quest_vars[quest_key])
    quest_checkbutton.grid(row=row, column=col, sticky="w", padx=2)
    row += 1
    if row >= 20:
        row = 0
        col += 1

# --- Buttons Frame ---
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

generate_button = tk.Button(buttons_frame, text="Generate Plan", command=generate_plan)
generate_button.pack(side="left", padx=5)

copy_button = tk.Button(buttons_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side="left", padx=5)

# --- Output Frame ---
output_frame = tk.LabelFrame(root, text="Output")
output_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

output_text = tk.Text(output_frame, wrap="word", state="normal")
output_text.pack(expand=True, fill="both")

# --- Error/Warning Frame ---
error_frame = tk.LabelFrame(root, text="Errors/Warnings")
error_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

error_text = tk.Text(error_frame, wrap="word", state="normal", height=5)
error_text.pack(expand=True, fill="both")

# --- Tooltips ---
for skill_key, skill_data in SKILLS.items():
    if skill_key in skill_vars:
        tooltip_text = f"{skill_key.capitalize()}:\n"
        for method_key, method_data in skill_data["methods"].items():
            if method_key == "default":
                continue
            tooltip_text += f"\n  {method_data['name']}:\n"
            if "requirements" in method_data:
                requirements = method_data["requirements"]
                if requirements:
                    tooltip_text += "    Requirements:\n"
                    for req_key, req_value in requirements.items():
                        tooltip_text += f"      {req_key.capitalize()}: {req_value}\n"
                else:
                    tooltip_text += "    Requirements: None\n"

        # Find the corresponding label and entry widgets
        for widget in skills_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text").lower() == skill_key:
                ToolTip(widget, tooltip_text)
            elif isinstance(widget, tk.Entry) and widget == skill_entry:
                ToolTip(widget, tooltip_text)

for quest_key, quest_data in QUESTS.items():
    tooltip_text = f"{quest_data['name']}:\n"
    if "quests" in quest_data:
        prerequisites = quest_data["quests"]
        if prerequisites:
            tooltip_text += "\n  Prerequisite Quests:\n"
            for prereq_key in prerequisites:
                prereq_name = QUESTS.get(prereq_key, {}).get("name", "Unknown")
                tooltip_text += f"    - {prereq_name}\n"
    if "skills" in quest_data:
        requirements = quest_data["skills"]
        if requirements:
            tooltip_text += "\n  Required Skills:\n"
            for req_key, req_value in requirements.items():
                tooltip_text += f"    {req_key.capitalize()}: {req_value}\n"
    if "skills_recommended" in quest_data:
        recommendations = quest_data["skills_recommended"]
        if recommendations:
            tooltip_text += "\n  Recommended Skills:\n"
            for rec_key, rec_value in recommendations.items():
                tooltip_text += f"    {rec_key.capitalize()}: {rec_value}\n"
    if "xp_rewards" in quest_data:
        xp_rewards = quest_data["xp_rewards"]
        if xp_rewards:
            tooltip_text += "\n  XP Rewards:\n"
            for xp_key, xp_value in xp_rewards.items():
                tooltip_text += f"    {xp_key.capitalize()}: {xp_value}\n"

    # Find the corresponding checkbutton widget
    for widget in quests_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton) and widget.cget("text") == quest_data["name"]:
            ToolTip(widget, tooltip_text)
            break

root.mainloop()