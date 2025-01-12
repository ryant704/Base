import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from quests import QUESTS
from skills import SKILLS
from utils.weights import calculate_weights
import random
import os

CONFIG_FILE = "config.txt"

def generate_plan():
    """
    Placeholder function for generating the plan.
    """
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Plan generation logic will be added here.\n")
    error_text.delete("1.0", tk.END)
    error_text.insert(tk.END, "No errors.\n")

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

    # Loop through agility methods
    for method_name, method_data in SKILLS["agility"]["methods"].items():
        if method_name != "default":  # Skip the default method
            method_var = tk.BooleanVar(value=False)
            method_vars["Agility"][method_name] = method_var
            check_button = ttk.Checkbutton(
                agility_methods_window, text=method_name.capitalize(), variable=method_var
            )
            check_button.pack(anchor="w")

            # Build a tooltip text without including "name"
            tooltip_text = f"{method_name.capitalize()}:\n"
            if isinstance(method_data, dict):  # Handle nested structure
                for level_range, details in method_data.items():
                    if isinstance(details, dict):
                        xp_per_hour = details.get("xp_per_hour", "N/A")
                        requirements = details.get("requirements", {})
                        tooltip_text += (
                            f"  • Level {level_range}\n"
                            f"      XP/hr: {xp_per_hour}\n"
                            f"      Requirements: {', '.join(f'{k.capitalize()}: {v}' for k, v in requirements.items()) or 'None'}\n"
                        )
            else:  # Handle flat structure (if any)
                xp_per_hour = method_data.get("xp_per_hour", "N/A")
                requirements = method_data.get("requirements", {})
                tooltip_text += (
                    f"  • XP/hr: {xp_per_hour}\n"
                    f"      Requirements: {', '.join(f'{k.capitalize()}: {v}' for k, v in requirements.items()) or 'None'}"
                )

            # Add tooltip to the checkbox
            ToolTip(check_button, tooltip_text)

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

    ttk.Label(combat_methods_window, text="Min").grid(row=0, column=1, padx=2, pady=2)
    ttk.Label(combat_methods_window, text="Max").grid(row=0, column=2, padx=2, pady=2)
    ttk.Label(combat_methods_window, text="Weight").grid(row=0, column=3, padx=2, pady=2)

    row = 1
    for skill in skills.get(method_name, []):
        if skill not in method_vars[method_name]:
            method_vars[method_name][skill] = {}

        if "selected" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["selected"] = tk.BooleanVar(value=False)

        method_checkbutton = ttk.Checkbutton(combat_methods_window, text=skill, variable=method_vars[method_name][skill]["selected"])
        method_checkbutton.grid(row=row, column=0, sticky="w", padx=2, pady=2)

        # Add tooltip with XP per hour and requirements
        tooltip_text = f"Train {skill} using {method_name} method.\n"
        if skill.lower() in SKILLS and "methods" in SKILLS[skill.lower()]:
            method_data = SKILLS[skill.lower()]["methods"].get(method_name.lower(), {})
            for level_range, details in method_data.items():
                if isinstance(details, dict):
                    name = details.get("name", "Unknown")
                    xp_per_hour = details.get("xp_per_hour", "N/A")
                    requirements = details.get("requirements", {})
                    req_text = "\n".join(f"      - {k.capitalize()}: {v}" for k, v in requirements.items()) or "      - None"
                    tooltip_text += (
                        f"  • Level {level_range}: {name}\n"
                        f"      XP/hr: {xp_per_hour}\n"
                        f"      Requirements:\n{req_text}\n"
                    )
        ToolTip(method_checkbutton, tooltip_text)

        if "min" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["min"] = tk.StringVar()
        if "max" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["max"] = tk.StringVar()
        if "weight" not in method_vars[method_name][skill]:
            method_vars[method_name][skill]["weight"] = tk.StringVar()

        ttk.Entry(combat_methods_window, textvariable=method_vars[method_name][skill]["min"], width=3, validate="key", validatecommand=vcmd).grid(row=row, column=1, padx=2, pady=2)
        ttk.Entry(combat_methods_window, textvariable=method_vars[method_name][skill]["max"], width=3, validate="key", validatecommand=vcmd).grid(row=row, column=2, padx=2, pady=2)
        ttk.Entry(combat_methods_window, textvariable=method_vars[method_name][skill]["weight"], width=3, validate="key", validatecommand=vcmd).grid(row=row, column=3, padx=2, pady=2)

        row += 1

    save_button = ttk.Button(combat_methods_window, text="Save", command=lambda: save_combat_methods(method_name, combat_methods_window))
    save_button.grid(row=row, column=0, columnspan=4, pady=5)

    open_combat_windows[method_name] = combat_methods_window


def save_combat_methods(method_name, window):
    """Saves the combat method settings, validates inputs, checks requirements, and handles missing selections."""
    error_messages = []
    missing_selections = []
    method_requirements = {
        "Rat": {"Attack": 50, "Strength": 50},
        "Nmz": {"Attack": 60, "Strength": 60},
        "Crab": {},
        "Slay": {},
        "Cannon": {}
    }

    for skill, settings in method_vars[method_name].items():
        if not isinstance(settings, dict):
            continue

        min_level_str = settings["min"].get()
        max_level_str = settings["max"].get()
        weight_str = settings.get("weight", tk.StringVar()).get()  # Weight is optional
        selected = settings["selected"].get()

        if (min_level_str or max_level_str) and not selected:
            missing_selections.append(skill)
            continue

        if selected:
            # Validate inputs
            if not min_level_str or not max_level_str:
                error_messages.append(f"Min and Max values must be set for {method_name} - {skill}.")
                continue

            try:
                min_level = int(min_level_str)
                max_level = int(max_level_str)
            except ValueError:
                error_messages.append(f"Min and Max values must be integers for {method_name} - {skill}.")
                continue

            if min_level < 1 or max_level > 99:
                 error_messages.append(f"Min and Max levels must be between 1 and 99 for {method_name} - {skill}.")
                 continue

            if min_level > max_level:
                error_messages.append(f"Min level cannot be greater than Max level for {method_name} - {skill}.")
                continue
            
            if method_name in method_requirements:
                for req_skill, req_level in method_requirements[method_name].items():
                    if skill.lower() == req_skill.lower() and min_level < req_level:
                        error_messages.append(
                            f"{method_name} requires {req_skill} level {req_level} "
                            f"(You set Min: {min_level})."
                        )
                        
            if not error_messages: # Save only if there are no errors
                # Save validated settings
                settings["min"] = str(min_level)
                settings["max"] = str(max_level)
                settings["weight"] = str(weight_str) if weight_str else "1"  # Default weight is 1 if not provided

    # Handle missing selections
    if missing_selections:
        confirm = messagebox.askyesno(
            "Missing Selections",
            f"You have entered Min/Max for the following skills but did not enable them:\n\n"
            f"{', '.join(missing_selections)}\n\n"
            f"Do you want to save these settings anyway?"
        )
        if not confirm:
            return  # User chose to go back and review settings
    
    # Display errors if any
    if error_messages:
        messagebox.showerror("Error", "\n".join(error_messages))
    elif not missing_selections or confirm: # Only show success if theres no error messages and no missing selections or they accepted to save with missing selections.
        messagebox.showinfo("Success", f"Settings for {method_name} saved.")
        window.destroy()


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


def load_default_theme():
    """Loads the default theme from the config file, or the default if no file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            theme_name = f.readline().strip()
            return theme_name
    return "clam"  # Default if no file or invalid theme


def save_default_theme():
    """Saves the selected theme to the config file."""
    selected_theme = theme_var.get()
    with open(CONFIG_FILE, "w") as f:
        f.write(selected_theme)
    messagebox.showinfo("Default Theme", f"Default theme set to: {selected_theme}")


def apply_initial_theme(root, default_theme):
    """Applies the default theme after the mainloop has started."""
    root.set_theme(default_theme)
    theme_var.set(default_theme)

# --- Main Application Setup (ThemedTk) ---
default_theme = load_default_theme()
root = ThemedTk(theme="clam")  # Initialize with a default, we will reset it in the after call
root.title("OSRS Account Planner")

# Load themes before we load the root window
theme_names = root.get_themes()

# --- Theme Selection Dropdown ---
theme_var = tk.StringVar(value="clam")  # Set initial theme - default needed here
theme_menu = ttk.OptionMenu(root, theme_var, *theme_names, command=lambda _: root.set_theme(theme_var.get()))
theme_menu.grid(row=0, column=0, sticky="nw")


default_button = ttk.Button(root, text="Set Default", command=save_default_theme)
default_button.grid(row=0, column=1, sticky="nw", padx=5)


# Use after to load the correct default theme
root.after(100, apply_initial_theme, root, default_theme)

# --- Skills Frame ---
skills_frame = ttk.LabelFrame(root, text="Skills")
skills_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

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

        skill_label = ttk.Label(skills_frame, text=skill)
        skill_label.grid(row=row, column=col, sticky="w", padx=2)

        skill_entry = ttk.Entry(skills_frame, textvariable=skill_vars[skill], width=3, validate="key", validatecommand=vcmd)
        skill_entry.grid(row=row, column=col + 1, padx=2, pady=2)

        row += 1
        if row > (len(skills_order) - 1) / 2:
            row = 0
            col += 2

# --- Training Methods Frame ---
methods_frame = ttk.LabelFrame(root, text="Training Methods")
methods_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Initialize method_vars
for method in ["Agility", "Crab", "Nmz", "Rat", "Slay", "Cannon", "Fruit"]:
    method_vars[method] = {}

method_row = 0

# Special handling for Agility
method_vars["Agility"]["selected"] = tk.BooleanVar(value=False)
agility_checkbox = ttk.Checkbutton(
    methods_frame, text="Agility", variable=method_vars["Agility"]["selected"]
)
agility_checkbox.grid(row=method_row, column=0, sticky="w", padx=2, pady=2)

agility_button = ttk.Button(methods_frame, text="Agility Methods", command=open_agility_methods)
agility_button.grid(row=method_row, column=1, sticky="w", padx=2, pady=2)
method_row += 1

# Combat methods
combat_methods = ["Crab", "Nmz", "Rat", "Slay", "Cannon"]
for method in combat_methods:
    method_vars[method]["selected"] = tk.BooleanVar(value=False)
    method_checkbox = ttk.Checkbutton(
        methods_frame, text=method, variable=method_vars[method]["selected"]
    )
    method_checkbox.grid(row=method_row, column=0, sticky="w", padx=2, pady=2)

    method_button = ttk.Button(methods_frame, text=f"{method} Methods", command=lambda m=method: open_combat_methods(m))
    method_button.grid(row=method_row, column=1, sticky="w", padx=2, pady=2)
    method_row += 1

# Fruit method (Thieving)
method_vars["Fruit"]["selected"] = tk.BooleanVar(value=False)
fruit_checkbox = ttk.Checkbutton(
    methods_frame, text="Fruit (Thieving)", variable=method_vars["Fruit"]["selected"]
)
fruit_checkbox.grid(row=method_row, column=0, sticky="w", padx=2, pady=2)

fruit_label = ttk.Label(methods_frame, text="Fruit Methods")
fruit_label.grid(row=method_row, column=1, sticky="w", padx=2, pady=2)
method_row += 1


# Dictionary to track open combat method windows
open_combat_windows = {}

# --- Quests Frame ---
quests_frame = ttk.LabelFrame(root, text="Quests")
quests_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

quest_vars = {}
row = 0
col = 0
for quest_key, quest_data in QUESTS.items():
    quest_vars[quest_key] = tk.BooleanVar(value=False)
    quest_checkbutton = ttk.Checkbutton(quests_frame, text=quest_data["name"], variable=quest_vars[quest_key])
    quest_checkbutton.grid(row=row, column=col, sticky="w", padx=2)
    row += 1
    if row >= 18:
        row = 0
        col += 1

# --- Buttons Frame ---
buttons_frame = ttk.Frame(root)
buttons_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

generate_button = ttk.Button(buttons_frame, text="Generate Plan", command=generate_plan)
generate_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

copy_button = ttk.Button(buttons_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

# Configure column weights so buttons resize
buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)

# --- Output & Error Frame ---
output_frame = ttk.LabelFrame(root, text="Output")
output_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

error_frame = ttk.LabelFrame(root, text="Errors/Warnings")
error_frame.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Configure row weights so they share the vertical space
root.rowconfigure(4, weight=1)


output_text = tk.Text(output_frame, wrap="word", state="normal")
output_text.pack(expand=True, fill="both")


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
            if isinstance(widget, ttk.Label) and widget.cget("text").lower() == skill_key:
                ToolTip(widget, tooltip_text)
            elif isinstance(widget, ttk.Entry) and widget == skill_entry:
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
        if isinstance(widget, ttk.Checkbutton) and widget.cget("text") == quest_data["name"]:
            ToolTip(widget, tooltip_text)
            break


root.mainloop()