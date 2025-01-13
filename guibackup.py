import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from quests import QUESTS
from skills import SKILLS
from utils.weights import calculate_weights  # Assuming this file exists
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
    center_window(agility_methods_window)
    agility_methods_window.transient(root)

    for method_name, method_data in SKILLS["agility"]["methods"].items():
        if method_name != "default":
            method_var = tk.BooleanVar(value=False)
            method_vars["Agility"][method_name] = method_var
            check_button = ttk.Checkbutton(
                agility_methods_window, text=method_name.capitalize(), variable=method_var
            )
            check_button.pack(anchor="w")
            tooltip_text = f"{method_name.capitalize()}:\n"
            if isinstance(method_data, dict):
                for level_range, details in method_data.items():
                    if isinstance(details, dict):
                        xp_per_hour = details.get("xp_per_hour", "N/A")
                        requirements = details.get("requirements", {})
                        tooltip_text += (
                            f"  • Level {level_range}\n"
                            f"      XP/hr: {xp_per_hour}\n"
                            f"      Requirements: {', '.join(f'{k.capitalize()}: {v}' for k, v in requirements.items()) or 'None'}\n"
                        )
            else:
                xp_per_hour = method_data.get("xp_per_hour", "N/A")
                requirements = method_data.get("requirements", {})
                tooltip_text += (
                    f"  • XP/hr: {xp_per_hour}\n"
                    f"      Requirements: {', '.join(f'{k.capitalize()}: {v}' for k, v in requirements.items()) or 'None'}"
                )
            ToolTip(check_button, tooltip_text)

    save_button = ttk.Button(agility_methods_window, text="Save", command=lambda: save_agility_methods(agility_methods_window))
    save_button.pack(pady=10)

def save_agility_methods(window):
    """Saves the selected agility methods and closes the window."""
    messagebox.showinfo("Success", "Agility methods saved.")
    window.destroy()

def open_combat_methods(method_name):
    """Opens a new window for selecting skills and setting min/max levels for a combat method."""
    if method_name in open_combat_windows and open_combat_windows[method_name].winfo_exists():
        open_combat_windows[method_name].lift()
        return

    combat_methods_window = tk.Toplevel(root)
    combat_methods_window.title(f"{method_name} Training Methods")
    center_window(combat_methods_window)
    combat_methods_window.transient(root)

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
        weight_str = settings.get("weight", tk.StringVar()).get()
        selected = settings["selected"].get()

        if (min_level_str or max_level_str) and not selected:
            missing_selections.append(skill)
            continue

        if selected:
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

            if not error_messages:
                settings["min"] = str(min_level)
                settings["max"] = str(max_level)
                settings["weight"] = str(weight_str) if weight_str else "1"

    if missing_selections:
        confirm = messagebox.askyesno(
            "Missing Selections",
            f"You have entered Min/Max for the following skills but did not enable them:\n\n"
            f"{', '.join(missing_selections)}\n\n"
            f"Do you want to save these settings anyway?"
        )
        if not confirm:
            return

    if error_messages:
        messagebox.showerror("Error", "\n".join(error_messages))
    elif not missing_selections or confirm:
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
    return "clam"

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

def center_window(window):
    """Centers a tkinter window on the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"+{x}+{y}")

def filter_quests():
    """Filters the displayed quests based on the selected criteria and re-organizes them."""
    search_term = search_var.get().lower()
    selected_length = length_var.get()
    selected_difficulty = difficulty_var.get()
    selected_rewards = [reward for reward, var in reward_vars.items() if var.get()]
    selected_member = member_var.get()
    selected_quest_points = quest_points_var.get()
    selected_xp_skill = xp_skill_var.get()
    xp_amount_str = xp_amount_var.get()
    min_xp_amount = int(xp_amount_str) if xp_amount_str.isdigit() else 0

    visible_quests = []
    for quest_key, quest_data in QUESTS.items():
        match_search = search_term in quest_data["name"].lower()
        match_length = not selected_length or selected_length == "Any" or quest_data.get("length") == selected_length
        match_difficulty = not selected_difficulty or selected_difficulty == "Any" or quest_data.get("difficulty") == selected_difficulty
        match_rewards = not selected_rewards or any(
            reward in quest_data.get("xp_rewards", {})
            for reward in selected_rewards
        )
        match_member = (selected_member == "Any" or
                        (selected_member == "Yes" and quest_data.get("members", False)) or
                        (selected_member == "No" and not quest_data.get("members", False)))
        match_quest_points = (selected_quest_points == "Any" or
                              (selected_quest_points != "Any" and quest_data.get("quest_points_reward", 0) == int(selected_quest_points)))
        match_xp_skill = (selected_xp_skill == "Any" or
                          (selected_xp_skill != "Any" and selected_xp_skill in quest_data.get("xp_rewards", {})))
        match_xp_amount = True
        if selected_xp_skill != "Any" and xp_amount_str:
            match_xp_amount = quest_data.get("xp_rewards", {}).get(selected_xp_skill, 0) >= min_xp_amount
        elif selected_xp_skill == "Any" and xp_amount_str:
            # Check if any of the xp rewards meet the minimum amount
            match_xp_amount = any(xp >= min_xp_amount for xp in quest_data.get("xp_rewards", {}).values())

        if match_search and match_length and match_difficulty and match_rewards and match_member and match_quest_points and match_xp_skill and match_xp_amount:
            visible_quests.append(quest_key)

    # Re-grid the visible quests
    row = 0
    col = 0
    max_rows_per_column = 18  # Keep the same maximum rows per column
    for quest_key in sorted(visible_quests):  # Sort the visible quests alphabetically
        quest_checkbuttons[quest_key].grid(row=row, column=col, sticky="w", padx=2)
        row += 1
        if row >= max_rows_per_column:
            row = 0
            col += 1

    # Hide quests that are not visible
    for quest_key in QUESTS:
        if quest_key not in visible_quests:
            quest_checkbuttons[quest_key].grid_remove()

def enable_all_quests():
    """Enables all quest checkboxes."""
    for var in quest_vars.values():
        var.set(True)
    filter_quests() # Apply filter after enabling all

def reset_filters():
    """Resets all quest filters to their default values with a confirmation."""
    if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all quest filters?"):
        search_var.set("")
        length_var.set("Any")
        difficulty_var.set("Any")
        member_var.set("Any")
        quest_points_var.set("Any")
        xp_skill_var.set("Any")
        xp_amount_var.set("")
        for var in reward_vars.values():
            var.set(False)
        for var in quest_vars.values():
            var.set(False)
        filter_quests() # Apply the reset state

# --- Main Application Setup (ThemedTk) ---
default_theme = load_default_theme()
root = ThemedTk(theme="clam")
root.title("OSRS Account Planner")

# Load themes before we load the root window
theme_names = root.get_themes()

# --- Theme Selection Dropdown and Set Default Button ---
theme_var = tk.StringVar(value="clam")
theme_menu = ttk.OptionMenu(root, theme_var, *theme_names, command=lambda _: root.set_theme(theme_var.get()))
theme_menu.grid(row=0, column=0, sticky="nw")

default_button = ttk.Button(root, text="Set Default", command=save_default_theme)
default_button.grid(row=0, column=1, sticky="nw", padx=5)

# Use after to load the correct default theme
root.after(100, apply_initial_theme, root, default_theme)

# --- Skills and Methods Frame (Top) ---
top_frame = ttk.Frame(root)
top_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# --- Skills Frame ---
skills_frame = ttk.LabelFrame(top_frame, text="Skills")
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

        skill_label = ttk.Label(skills_frame, text=skill)
        skill_label.grid(row=row, column=col, sticky="w", padx=2)

        skill_entry = ttk.Entry(skills_frame, textvariable=skill_vars[skill], width=3, validate="key", validatecommand=vcmd)
        skill_entry.grid(row=row, column=col + 1, padx=2, pady=2)

        row += 1
        if row > (len(skills_order) - 1) / 2:
            row = 0
            col += 2

# --- Training Methods Frame ---
methods_frame = ttk.LabelFrame(top_frame, text="Training Methods")
methods_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

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

# Configure grid weights for top frame columns
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)

# Dictionary to track open combat method windows
open_combat_windows = {}
# --- Quest Filters Frame ---
filters_frame = ttk.LabelFrame(root, text="Quest Filters")
filters_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Adjust reward_vars initialization
reward_vars = {}
possible_rewards = sorted(SKILLS.keys())  # Get skills from SKILLS dictionary
for reward in possible_rewards:
    reward_vars[reward] = tk.BooleanVar()

# Adjust row 0 of the main filters_frame
ttk.Label(filters_frame, text="Search:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
search_var = tk.StringVar()
search_entry = ttk.Entry(filters_frame, textvariable=search_var, width=15)
search_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")
search_entry.bind("<KeyRelease>", lambda event: filter_quests())

ttk.Label(filters_frame, text="Quests:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
enable_all_button = ttk.Button(filters_frame, text="Enable All", command=enable_all_quests)
enable_all_button.grid(row=0, column=3, padx=5, pady=2, sticky="w")

reset_button = ttk.Button(filters_frame, text="Reset", command=reset_filters)
reset_button.grid(row=0, column=4, padx=5, pady=2, sticky="w")

ttk.Label(filters_frame, text="Member:").grid(row=0, column=5, padx=5, pady=2, sticky="w")
member_var = tk.StringVar(value="Any")
member_choices = ["Any", "Yes", "No"]
member_combo = ttk.Combobox(filters_frame, textvariable=member_var, values=member_choices, state="readonly", width=10)
member_combo.grid(row=0, column=6, padx=5, pady=2, sticky="w")
member_combo.bind("<<ComboboxSelected>>", lambda event: filter_quests())

ttk.Label(filters_frame, text="XP Skill:").grid(row=0, column=7, padx=5, pady=2, sticky="w")
xp_skill_var = tk.StringVar(value="Any")
xp_skill_choices = ["Any"] + sorted(list(SKILLS.keys()))
xp_skill_combo = ttk.Combobox(filters_frame, textvariable=xp_skill_var, values=xp_skill_choices, state="readonly", width=10)
xp_skill_combo.grid(row=0, column=8, padx=5, pady=2, sticky="w")
xp_skill_combo.bind("<<ComboboxSelected>>", lambda event: filter_quests())

ttk.Label(filters_frame, text="XP Amount:").grid(row=0, column=9, padx=5, pady=2, sticky="w")
xp_amount_var = tk.StringVar()
xp_amount_entry = ttk.Entry(filters_frame, textvariable=xp_amount_var, width=10)
xp_amount_entry.grid(row=0, column=10, padx=5, pady=2, sticky="w")
xp_amount_entry.bind("<KeyRelease>", lambda event: filter_quests())

# Adjust row 1 of the main filters_frame
ttk.Label(filters_frame, text="Difficulty:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
difficulty_var = tk.StringVar(value="Any")
difficulty_choices = ["Any", "Novice", "Intermediate", "Experienced", "Master", "Grandmaster"]
difficulty_combo = ttk.Combobox(filters_frame, textvariable=difficulty_var, values=difficulty_choices, state="readonly", width=15)
difficulty_combo.grid(row=1, column=1, padx=5, pady=2, sticky="w")
difficulty_combo.bind("<<ComboboxSelected>>", lambda event: filter_quests())

ttk.Label(filters_frame, text="Quest Points:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
quest_points_var = tk.StringVar(value="Any")
quest_points_choices = ["Any"] + sorted(list(set(quest.get("quest_points_reward", 0) for quest in QUESTS.values() if quest.get("quest_points_reward"))))
quest_points_combo = ttk.Combobox(filters_frame, textvariable=quest_points_var, values=quest_points_choices, state="readonly", width=15)
quest_points_combo.grid(row=1, column=3, padx=5, pady=2, sticky="w")
quest_points_combo.bind("<<ComboboxSelected>>", lambda event: filter_quests())

ttk.Label(filters_frame, text="Length:").grid(row=1, column=4, padx=5, pady=2, sticky="w")
length_var = tk.StringVar(value="Any")
length_choices = ["Any", "Very Short", "Short", "Medium", "Long", "Very Long"]
length_combo = ttk.Combobox(filters_frame, textvariable=length_var, values=length_choices, state="readonly", width=15)
length_combo.grid(row=1, column=5, padx=5, pady=2, sticky="w")
length_combo.bind("<<ComboboxSelected>>", lambda event: filter_quests())

ttk.Label(filters_frame, text="Rewards:").grid(row=1, column=6, padx=5, pady=2, sticky="w")
rewards_menu_button = ttk.Menubutton(filters_frame, text="Select Rewards", direction='below')
rewards_menu = tk.Menu(rewards_menu_button, tearoff=0)
rewards_menu_button.config(menu=rewards_menu)

def update_rewards_text():
    selected_rewards_text = ", ".join([reward.capitalize() for reward, var in reward_vars.items() if var.get()])
    rewards_menu_button.config(text=selected_rewards_text if selected_rewards_text else "Select Rewards")
    filter_quests() # Apply filter immediately after reward selection

for reward in possible_rewards:
    rewards_menu.add_checkbutton(label=reward.capitalize(), variable=reward_vars[reward], command=update_rewards_text)

rewards_menu_button.grid(row=1, column=7, padx=5, pady=2, sticky="ew")

# Ensure all columns share equal weight
for i in range(11):  # Update the range to accommodate the new column
    filters_frame.columnconfigure(i, weight=1)

# --- Quests Frame ---
quests_frame = ttk.LabelFrame(root, text="Quests")
quests_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

quest_vars = {}
quest_checkbuttons = {} # To store the checkbutton widgets for filtering
row = 0
col = 0
for quest_key in sorted(QUESTS.keys()):  # Sort quest keys alphabetically here
    quest_data = QUESTS[quest_key]
    quest_vars[quest_key] = tk.BooleanVar(value=False)
    quest_checkbutton = ttk.Checkbutton(quests_frame, text=quest_data["name"], variable=quest_vars[quest_key])
    quest_checkbuttons[quest_key] = quest_checkbutton # Store the widget
    # Initialize the grid layout for all quests
    quest_checkbutton.grid(row=row, column=col, sticky="w", padx=2)
    row += 1
    if row >= 18:
        row = 0
        col += 1

# --- Buttons Frame ---
buttons_frame = ttk.Frame(root)
buttons_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

generate_button = ttk.Button(buttons_frame, text="Generate Plan", command=generate_plan)
generate_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

copy_button = ttk.Button(buttons_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

# Configure column weights so buttons resize
buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)

# --- Output & Error Frame ---
output_frame = ttk.LabelFrame(root, text="Output")
output_frame.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

error_frame = ttk.LabelFrame(root, text="Errors/Warnings")
error_frame.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

# Configure row weights so they share the vertical space
root.rowconfigure(5, weight=1)

output_text = tk.Text(output_frame, wrap="word", state="normal")
output_text.pack(expand=True, fill="both")

error_text = tk.Text(error_frame, wrap="word", state="normal", height=5)
error_text.pack(expand=True, fill="both")

# --- Tooltips ---
for skill_key, skill_data in SKILLS.items():
    tooltip_text = ""  # Initialize tooltip_text for every skill_key
    if skill_key in skill_vars:
        tooltip_text = f"{skill_key.capitalize()}:\n"
        for method_key, method_data in skill_data["methods"].items():
            if method_key == "default":
                continue
            tooltip_text += f"\n  {method_data['name']}:\n"
            if "requirements" in method_data:
                requirements = method_data["requirements"]
                if requirements:
                    for req_key, req_value in requirements.items():
                        tooltip_text += f"      {req_key.capitalize()}: {req_value}\n"
                else:
                    tooltip_text += "    Requirements: None\n"

    for widget in skills_frame.winfo_children():
        if isinstance(widget, ttk.Label) and widget.cget("text").lower() == skill_key:
            ToolTip(widget, tooltip_text)
        elif isinstance(widget, ttk.Entry) and widget.winfo_exists() and widget.getvar(widget['textvariable']) == skill_vars.get(skill_key, tk.StringVar()).get():
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
    if "quest_points_reward" in quest_data and quest_data["quest_points_reward"] > 0:
        tooltip_text += f"\n  Reward:\n    Quest Points: {quest_data['quest_points_reward']}\n"

    for widget in quests_frame.winfo_children():
        if isinstance(widget, ttk.Checkbutton) and widget.cget("text") == quest_data["name"]:
            ToolTip(widget, tooltip_text)
            break

root.mainloop()