# weights.py

def calculate_weights(current_levels, method_vars, skill):
    """
    Calculates the training method weights, taking into account:
        - User-defined weights.
        - +5 bonus to Attack and Strength (unless Defence is lagging).
        - +5 bonus to Defence if it's lagging behind Attack or Strength.
        - +3 bonus for milestone-recommended methods.

    Args:
        current_levels (dict): A dictionary of the user's current skill levels.
        method_vars (dict): The dictionary storing method variables (including weights).
        skill (str): The skill being trained.

    Returns:
        dict: A dictionary where keys are method names and values are the final calculated weights.
    """
    weights = {}
    
    # Define the mapping for simplification
    method_name_mapping = {
        "Crab": "Sand Crabs",
        "Nmz": "Nightmare Zone",
        "Rat": "Scurrius",
        "Slay": "Slayer",
        "Cannon": "Dwarf Cannon"
    }

    for method_name, method_data in method_vars.items():
        if isinstance(method_data, dict) and method_data["selected"].get():
            # Check if the method can be used for the current skill
            
            if method_name.lower() == "agility" and skill.lower() != "agility":
                continue
            if method_name.lower() == "fruit" and skill.lower() != "thieving":
                continue

            # Check if Min/Max is defined for the specific skill. If not, skip this method.
            if isinstance(method_data.get(skill, {}), dict) and "min" in method_data[skill] and "max" in method_data[skill]:
                
                min_level = int(method_data[skill]["min"].get() or 1)
                max_level = int(method_data[skill]["max"].get() or 99)

                if min_level <= current_levels[skill] <= max_level:
                    
                    # Check for combat skills and apply +5 to attack and strength if defence is not 10+ behind
                    if skill.lower() in ["attack", "strength"] and max(current_levels.get("Attack", 1), current_levels.get("Strength", 1)) - current_levels.get("Defence", 1) <= 10:
                        
                        # Use get method with default value to avoid KeyError
                        weight = int(method_data[skill].get("weight", tk.StringVar()).get() or 0) + 5

                        
                    elif skill.lower() == "defence" and max(current_levels.get("Attack", 1), current_levels.get("Strength", 1)) - current_levels.get("Defence", 1) > 10:
                        weight = int(method_data[skill].get("weight", tk.StringVar()).get() or 0) + 5
                    else:
                        weight = int(method_data[skill].get("weight", tk.StringVar()).get() or 0)

                    weights[method_name] = weight
            elif method_name.lower() == "agility":
                weights[method_name] = int(method_data.get("weight", tk.StringVar()).get() or 0)

    # Apply milestone bonus
    if current_levels[skill] in SKILLS[skill]["milestones"]:
        recommended_method = SKILLS[skill]["milestones"][current_levels[skill]]["method"]
        if recommended_method in weights:
            weights[recommended_method] += 3

    return weights