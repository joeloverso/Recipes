#!/usr/bin/env python3
###########################################################################
# Date created:  June 29 2025
# Date finished: June 30 2025
# Purpose:       Automate Recipe figures
# Author:        Joseph LoVerso
###########################################################################
# Native imports
import os
import json
import datetime

# 3rd party imports
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


def main():
    while True:
        choice = mainMenuChoice()

        if choice is None:
            console.clear()
            console.print("[bold green]Exiting...[/bold green]")
            break
        elif choice == "1":
            calculate_recipe()
            input("Press Enter to continue...")
        elif choice == "2":
            view_recipes()
            input("Press Enter to continue...")
        elif choice == "3":
            new_recipe()
            input("Press Enter to continue...")
        elif choice == "4":
            delete_recipe()
            input("Press Enter to continue...")


def drawMenu():
    width = 42
    lines = [
        "Recipe Calculator",
        "",  # Empty line
        "1. Calculate recipe",
        "2. View existing recipes",
        "3. New recipe",
        "4. Delete recipe",
        "Q. Exit",
        "",  # Empty line
    ]

    # Top border - cyan color because that's beautiful
    console.print("╔" + "═" * width + "╗", style="cyan")

    # Title with separator - bold cyan
    title = lines[0]
    padding = (width - len(title)) // 2
    title_line = (
        "║" + " " * padding + title + " " * (width - len(title) - padding) + "║"
    )
    console.print(title_line, style="bold cyan")
    console.print("╠" + "═" * width + "╣", style="cyan")

    # Menu items
    for line in lines[1:]:
        if line == "":
            # Empty line
            console.print("║" + " " * width + "║", style="cyan")
        else:
            # Menu items with colors
            padded_line = "  " + line
            remaining_space = width - len(padded_line)
            menu_line = "║" + padded_line + " " * remaining_space + "║"

            # Color different menu items
            if line.startswith("1."):
                console.print(menu_line, style="yellow")  # Calculate - yellow
            elif line.startswith("2."):
                console.print(menu_line, style="green")  # View - green
            elif line.startswith("3."):
                console.print(menu_line, style="violet")  # New - violet
            elif line.startswith("4."):
                console.print(menu_line, style="red")  # Delete - red
            elif line.startswith("Q."):
                console.print(menu_line, style="bold white")  # Exit - bold white
            else:
                console.print(menu_line, style="cyan")

    # Bottom border - cyan color
    console.print("╚" + "═" * width + "╝", style="cyan")


def mainMenuChoice():
    while True:
        # Clear the console
        console.clear()
        # Draw the menu
        drawMenu()

        # Get user input with Rich prompt
        choice = Prompt.ask(
            "\n[bold yellow]Enter your choice[/bold yellow]",
            choices=["1", "2", "3", "4", "q", "Q"],
            show_choices=False,
        ).lower()

        if choice in ["1", "2", "3", "4"]:
            return choice
        elif choice == "q":
            return None


def new_recipe():
    """Create a new recipe and save it to a JSON file"""

    # Clear screen for new recipe creation
    console.clear()
    console.print("[bold cyan]═══ Create New Recipe ═══[/bold cyan]\n")

    # Ensure the Saved Recipes directory exists
    recipes_dir = "Saved Recipes"
    if not os.path.exists(recipes_dir):
        os.makedirs(recipes_dir)
        console.print(f"[green]Created directory: {recipes_dir}[/green]\n")

    # Get recipe name
    while True:
        recipe_name = (
            Prompt.ask("[bold cyan]Enter recipe name[/bold cyan]")
            .lower()
            .strip()
            .replace(" ", "-")
        )
        if recipe_name:
            break
        console.print("[red]Recipe name cannot be empty. Please try again.[/red]")

    # Check if file already exists
    filename = f"{recipe_name}.json"
    filepath = os.path.join(recipes_dir, filename)

    if os.path.exists(filepath):
        overwrite = Confirm.ask(
            f"[yellow]A recipe named '{recipe_name}' already exists. Do you want to overwrite it?[/yellow]"
        )
        if not overwrite:
            console.print("[red]Recipe creation cancelled.[/red]")
            return

    # Get recipe notes
    console.print("\n[bold cyan]Enter recipe notes/instructions:[/bold cyan]")
    console.print(
        "[dim]Press Enter twice when finished, or type 'DONE' on a line by itself[/dim]"
    )

    notes_lines = []
    empty_line_count = 0

    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        if line.strip() == "":
            empty_line_count += 1
            if empty_line_count >= 2:
                break
            notes_lines.append(line)
        else:
            empty_line_count = 0
            notes_lines.append(line)

    # Remove trailing empty lines
    while notes_lines and notes_lines[-1].strip() == "":
        notes_lines.pop()

    notes = "\n".join(notes_lines)

    # Get ingredients
    ingredients = []
    console.print("\n[bold cyan]Now let's add ingredients:[/bold cyan]")

    while True:
        # Get ingredient name
        ingredient_name = Prompt.ask("[yellow]Ingredient name[/yellow]").strip()
        if not ingredient_name:
            console.print("[red]Ingredient name cannot be empty.[/red]")
            continue

        # Get unit measurement
        unit = Prompt.ask(
            f"[yellow]Unit of measurement for {ingredient_name}[/yellow] (e.g., cups, tbsp, lbs)"
        ).strip()
        if not unit:
            console.print("[red]Unit cannot be empty.[/red]")
            continue

        # Get quantity (float value)
        while True:
            try:
                quantity_str = Prompt.ask(
                    f"[yellow]Quantity of {ingredient_name} in {unit}[/yellow]"
                )
                quantity = float(quantity_str)
                break
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")

        # Add ingredient to list
        ingredients.append(
            {"name": ingredient_name, "quantity": quantity, "unit": unit}
        )

        console.print(f"[green]Added: {quantity} {unit} of {ingredient_name}[/green]")

        # Ask if they want to add another ingredient
        add_another = Confirm.ask("\n[cyan]Add another ingredient?[/cyan]")
        if not add_another:
            break

    # Create recipe dictionary
    recipe_data = {
        "name": recipe_name,
        "notes": notes,
        "ingredients": ingredients,
        "created_date": datetime.datetime.now().isoformat(),
    }

    # Display recipe for confirmation
    display_recipe_preview(recipe_data)

    # Confirm before saving
    if Confirm.ask("\n[bold green]Save this recipe?[/bold green]"):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(recipe_data, f, indent=2, ensure_ascii=False)

            console.print(
                f"\n[bold green]✓ Recipe '{recipe_name}' saved successfully![/bold green]"
            )
            console.print(f"[dim]Saved to: {filepath}[/dim]")

        except Exception as e:
            console.print(f"[bold red]Error saving recipe: {e}[/bold red]")
    else:
        console.print("[yellow]Recipe not saved.[/yellow]")


def display_recipe_preview(recipe_data):
    """Display a formatted preview of the recipe"""
    console.print("\n" + "=" * 60)
    console.print(f"[bold cyan]Recipe Preview[/bold cyan]")
    console.print("=" * 60)

    # Recipe name
    console.print(f"\n[bold yellow]Name:[/bold yellow] {recipe_data['name']}")

    # Notes
    if recipe_data["notes"].strip():
        console.print(f"\n[bold yellow]Notes/Instructions:[/bold yellow]")
        # Display notes in a panel for better formatting
        notes_panel = Panel(recipe_data["notes"], border_style="dim")
        console.print(notes_panel)

    # Ingredients table
    if recipe_data["ingredients"]:
        console.print(f"\n[bold yellow]Ingredients:[/bold yellow]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Ingredient", style="cyan")
        table.add_column("Quantity", style="green", justify="right")
        table.add_column("Unit", style="yellow")

        for ingredient in recipe_data["ingredients"]:
            # Format quantity to remove unnecessary decimal places
            qty = ingredient["quantity"]
            if qty == int(qty):
                qty_str = str(int(qty))
            else:
                qty_str = f"{qty:.2f}".rstrip("0").rstrip(".")

            table.add_row(ingredient["name"], qty_str, ingredient["unit"])

        console.print(table)

    console.print("=" * 60)


def view_recipes():
    """View all existing recipes"""
    console.clear()
    console.print("[bold cyan]═══ View Existing Recipes ═══[/bold cyan]\n")

    recipes_dir = "Saved Recipes"

    # Check if recipes directory exists
    if not os.path.exists(recipes_dir):
        console.print(
            "[yellow]No recipes directory found. Create some recipes first![/yellow]"
        )
        return

    # Get all JSON files in the recipes directory
    recipe_files = [f for f in os.listdir(recipes_dir) if f.endswith(".json")]

    if not recipe_files:
        console.print("[yellow]No recipes found. Create some recipes first![/yellow]")
        return

    # Load all recipe data
    all_recipes = []
    for filename in recipe_files:
        filepath = os.path.join(recipes_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                recipe_data = json.load(f)
            all_recipes.append((filename, recipe_data))
        except Exception as e:
            console.print(f"[red]Error reading {filename}: {e}[/red]")
            continue

    # Sort recipes alphabetically by name
    all_recipes.sort(key=lambda x: x[1].get("name", x[0]).lower())

    # Search functionality
    filtered_recipes = all_recipes
    search_term = ""

    # Only show search option if there are more than 5 recipes
    if len(all_recipes) > 5:
        search_choice = Prompt.ask(
            f"[cyan]Found {len(all_recipes)} recipes. Search by name? (y/n)[/cyan]",
        ).lower()

        if search_choice == "y":
            search_term = Prompt.ask(
                "[yellow]Enter search term (recipe name)[/yellow]"
            ).strip()

            if search_term:
                # Filter recipes by name (case-insensitive, partial matching)
                filtered_recipes = [
                    (filename, recipe_data)
                    for filename, recipe_data in all_recipes
                    if search_term.lower()
                    in recipe_data.get("name", filename.replace(".json", "")).lower()
                ]

                if filtered_recipes:
                    console.print(
                        f"\n[green]Found {len(filtered_recipes)} recipe(s) matching '{search_term}':[/green]\n"
                    )
                else:
                    console.print(
                        f"\n[yellow]No recipes found matching '{search_term}'. Showing all recipes:[/yellow]\n"
                    )
                    filtered_recipes = all_recipes
            else:
                console.print(
                    f"\n[yellow]No search term entered. Showing all recipes:[/yellow]\n"
                )
    else:
        console.print(f"[green]Found {len(all_recipes)} recipe(s):[/green]\n")

    # Create a table of available recipes
    recipes_table = Table(show_header=True, header_style="bold magenta")
    recipes_table.add_column("#", style="cyan", width=3)
    recipes_table.add_column("Recipe Name", style="white")
    recipes_table.add_column("Created", style="dim", width=12)

    recipe_data_list = []

    for i, (filename, recipe_data) in enumerate(filtered_recipes, 1):
        # Get recipe name and creation date
        recipe_name = recipe_data.get("name", filename.replace(".json", ""))
        created_date = recipe_data.get("created_date", "Unknown")

        # Format date for display
        if created_date != "Unknown":
            try:
                date_obj = datetime.datetime.fromisoformat(created_date)
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except:
                formatted_date = "Unknown"
        else:
            formatted_date = "Unknown"

        # Highlight search term if it exists
        display_name = recipe_name
        if search_term and search_term.lower() in recipe_name.lower():
            # Find the matching part and highlight it
            start_idx = recipe_name.lower().find(search_term.lower())
            if start_idx != -1:
                end_idx = start_idx + len(search_term)
                display_name = (
                    recipe_name[:start_idx]
                    + f"[bold yellow]{recipe_name[start_idx:end_idx]}[/bold yellow]"
                    + recipe_name[end_idx:]
                )

        recipes_table.add_row(str(i), display_name, formatted_date)
        recipe_data_list.append((filename, recipe_data))

    console.print(recipes_table)

    # Let user select a recipe to view
    while True:
        try:
            prompt_text = f"\n[bold yellow]Enter recipe number to view (1-{len(recipe_data_list)})"
            if search_term:
                prompt_text += f", 's' to search again,"
            prompt_text += f" or 'q' to go back[/bold yellow]"

            choice = Prompt.ask(prompt_text, default="q").strip().lower()

            if choice == "q":
                return
            elif choice == "s" and search_term:
                # Start over with new search
                view_recipes()
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(recipe_data_list):
                filename, recipe_data = recipe_data_list[choice_num - 1]
                display_full_recipe(recipe_data)

                # Ask if they want to view another recipe
                if not Confirm.ask("\n[cyan]View another recipe?[/cyan]"):
                    return
                else:
                    # Return to the search results, not start over
                    console.clear()
                    console.print(
                        "[bold cyan]═══ View Existing Recipes ═══[/bold cyan]\n"
                    )
                    if search_term:
                        console.print(
                            f"[green]Showing {len(filtered_recipes)} recipe(s) matching '{search_term}':[/green]\n"
                        )
                    else:
                        console.print(
                            f"[green]Found {len(filtered_recipes)} recipe(s):[/green]\n"
                        )
                    console.print(recipes_table)
            else:
                console.print(
                    f"[red]Please enter a number between 1 and {len(recipe_data_list)}[/red]"
                )

        except ValueError:
            console.print(
                "[red]Please enter a valid number, 's' to search again, or 'q' to quit[/red]"
            )
        except KeyboardInterrupt:
            return


def display_full_recipe(recipe_data):
    """Display a complete recipe with all details"""
    console.clear()

    # Recipe header
    recipe_name = recipe_data.get("name", "Unknown Recipe")
    console.print(f"[bold cyan]{'═' * 20} {recipe_name} {'═' * 20}[/bold cyan]")

    # Created date
    created_date = recipe_data.get("created_date", "Unknown")
    if created_date != "Unknown":
        try:
            date_obj = datetime.datetime.fromisoformat(created_date)
            formatted_date = date_obj.strftime("%B %d, %Y at %I:%M %p")
            console.print(f"[dim]Created: {formatted_date}[/dim]\n")
        except:
            console.print(f"[dim]Created: {created_date}[/dim]\n")

    # Ingredients section
    ingredients = recipe_data.get("ingredients", [])
    if ingredients:
        console.print("[bold yellow]🥘 Ingredients:[/bold yellow]")

        ingredients_table = Table(
            show_header=True, header_style="bold magenta", box=None
        )
        ingredients_table.add_column("Ingredient", style="cyan")
        ingredients_table.add_column("Amount", style="green", justify="right")
        ingredients_table.add_column("Unit", style="yellow")

        for ingredient in ingredients:
            qty = ingredient.get("quantity", 0)
            # Format quantity nicely
            if qty == int(qty):
                qty_str = str(int(qty))
            else:
                qty_str = f"{qty:.2f}".rstrip("0").rstrip(".")

            ingredients_table.add_row(
                ingredient.get("name", "Unknown"), qty_str, ingredient.get("unit", "")
            )

        console.print(ingredients_table)
        console.print()

    # Notes/Instructions section
    notes = recipe_data.get("notes", "").strip()
    if notes:
        console.print("[bold yellow]📝 Instructions:[/bold yellow]")
        notes_panel = Panel(
            notes,
            border_style="blue",
            padding=(1, 2),
            title="Recipe Notes",
            title_align="left",
        )
        console.print(notes_panel)
    else:
        console.print("[dim]No instructions provided.[/dim]")

    console.print(f"\n[bold cyan]{'═' * (42 + len(recipe_name))}[/bold cyan]")


def calculate_recipe():
    """Calculate scaled recipe amounts based on user input"""
    console.clear()
    console.print("[bold cyan]═══ Calculate Recipe Portions ═══[/bold cyan]\n")

    recipes_dir = "Saved Recipes"

    # Check if recipes directory exists
    if not os.path.exists(recipes_dir):
        console.print(
            "[yellow]No recipes directory found. Create some recipes first![/yellow]"
        )
        return

    # Get all JSON files in the recipes directory
    recipe_files = [f for f in os.listdir(recipes_dir) if f.endswith(".json")]

    if not recipe_files:
        console.print("[yellow]No recipes found. Create some recipes first![/yellow]")
        return

    # Load all recipe data
    all_recipes = []
    for filename in recipe_files:
        filepath = os.path.join(recipes_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                recipe_data = json.load(f)
            all_recipes.append((filename, recipe_data))
        except Exception as e:
            console.print(f"[red]Error reading {filename}: {e}[/red]")
            continue

    # Sort recipes alphabetically by name
    all_recipes.sort(key=lambda x: x[1].get("name", x[0]).lower())

    # Search functionality
    filtered_recipes = all_recipes
    search_term = ""

    # Only show search option if there are more than 5 recipes
    if len(all_recipes) > 5:
        search_choice = Prompt.ask(
            f"[cyan]Found {len(all_recipes)} recipes. Search by name? (y/n)[/cyan]",
            choices=["y", "n", "Y", "N"],
            default="n",
        ).lower()

        if search_choice == "y":
            search_term = Prompt.ask(
                "[yellow]Enter search term (recipe name)[/yellow]"
            ).strip()

            if search_term:
                # Filter recipes by name (case-insensitive, partial matching)
                filtered_recipes = [
                    (filename, recipe_data)
                    for filename, recipe_data in all_recipes
                    if search_term.lower()
                    in recipe_data.get("name", filename.replace(".json", "")).lower()
                ]

                if filtered_recipes:
                    console.print(
                        f"\n[green]Found {len(filtered_recipes)} recipe(s) matching '{search_term}':[/green]\n"
                    )
                else:
                    console.print(
                        f"\n[yellow]No recipes found matching '{search_term}'. Showing all recipes:[/yellow]\n"
                    )
                    filtered_recipes = all_recipes
            else:
                console.print(
                    f"\n[yellow]No search term entered. Showing all recipes:[/yellow]\n"
                )
    else:
        console.print(f"[green]Found {len(all_recipes)} recipe(s):[/green]\n")

    # Create a table of available recipes
    recipes_table = Table(show_header=True, header_style="bold magenta")
    recipes_table.add_column("#", style="cyan", width=3)
    recipes_table.add_column("Recipe Name", style="white")
    recipes_table.add_column("Base Ingredient", style="yellow")

    recipe_data_list = []

    for i, (filename, recipe_data) in enumerate(filtered_recipes, 1):
        recipe_name = recipe_data.get("name", filename.replace(".json", ""))
        ingredients = recipe_data.get("ingredients", [])

        # Get the first ingredient as the base
        if ingredients:
            first_ingredient = ingredients[0]
            base_info = f"{first_ingredient.get('name', 'Unknown')} ({first_ingredient.get('unit', 'units')})"
        else:
            base_info = "No ingredients"

        # Highlight search term if it exists
        display_name = recipe_name
        if search_term and search_term.lower() in recipe_name.lower():
            # Find the matching part and highlight it
            start_idx = recipe_name.lower().find(search_term.lower())
            if start_idx != -1:
                end_idx = start_idx + len(search_term)
                display_name = (
                    recipe_name[:start_idx]
                    + f"[bold yellow]{recipe_name[start_idx:end_idx]}[/bold yellow]"
                    + recipe_name[end_idx:]
                )

        recipes_table.add_row(str(i), display_name, base_info)
        recipe_data_list.append((filename, recipe_data))

    console.print(recipes_table)

    # Let user select a recipe
    while True:
        try:
            prompt_text = f"\n[bold yellow]Enter recipe number to calculate (1-{len(recipe_data_list)})"
            if search_term:
                prompt_text += f", 's' to search again,"
            prompt_text += f" or 'q' to go back[/bold yellow]"

            choice = Prompt.ask(prompt_text, default="q").strip().lower()

            if choice == "q":
                return
            elif choice == "s" and search_term:
                # Start over with new search
                calculate_recipe()
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(recipe_data_list):
                filename, recipe_data = recipe_data_list[choice_num - 1]
                perform_recipe_calculation(recipe_data)

                # Ask if they want to calculate another recipe
                if not Confirm.ask("\n[cyan]Calculate another recipe?[/cyan]"):
                    return
                else:
                    # Return to the search results, not start over
                    console.clear()
                    console.print(
                        "[bold cyan]═══ Calculate Recipe Portions ═══[/bold cyan]\n"
                    )
                    if search_term:
                        console.print(
                            f"[green]Showing {len(filtered_recipes)} recipe(s) matching '{search_term}':[/green]\n"
                        )
                    else:
                        console.print(
                            f"[green]Found {len(filtered_recipes)} recipe(s):[/green]\n"
                        )
                    console.print(recipes_table)
            else:
                console.print(
                    f"[red]Please enter a number between 1 and {len(recipe_data_list)}[/red]"
                )

        except ValueError:
            console.print(
                "[red]Please enter a valid number, 's' to search again, or 'q' to quit[/red]"
            )
        except KeyboardInterrupt:
            return


def perform_recipe_calculation(recipe_data):
    """Perform the actual recipe scaling calculation"""
    console.clear()

    recipe_name = recipe_data.get("name", "Unknown Recipe")
    ingredients = recipe_data.get("ingredients", [])

    if not ingredients:
        console.print("[red]This recipe has no ingredients to calculate![/red]")
        return

    # Get the base ingredient (first ingredient)
    base_ingredient = ingredients[0]
    base_name = base_ingredient.get("name", "Unknown")
    base_quantity = base_ingredient.get("quantity", 1.0)
    base_unit = base_ingredient.get("unit", "units")

    console.print(f"[bold cyan]Calculating portions for: {recipe_name}[/bold cyan]\n")

    # Get user input for base ingredient amount
    console.print(f"[bold yellow]Base ingredient: {base_name}[/bold yellow]")
    console.print(f"[dim]Original amount: {base_quantity} {base_unit}[/dim]")

    while True:
        try:
            user_amount = Prompt.ask(
                f"[cyan]How much {base_name} will you be using? (in {base_unit})[/cyan]"
            )
            user_quantity = float(user_amount)
            if user_quantity <= 0:
                console.print("[red]Please enter a positive number.[/red]")
                continue
            break
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

    # Calculate scaling factor
    scaling_factor = user_quantity / base_quantity

    console.print(f"\n[bold green]Scaling factor: {scaling_factor:.3f}x[/bold green]")
    console.print(
        f"[dim](You're making {scaling_factor:.1f}x the original recipe)[/dim]\n"
    )

    # Calculate scaled amounts
    console.print("[bold yellow]Your Calculated Recipe:[/bold yellow]")

    scaled_table = Table(
        show_header=True, header_style="bold magenta", title="Scaled Recipe", box=None
    )
    scaled_table.add_column("Ingredient", style="cyan")
    scaled_table.add_column("Your Amount", style="green", justify="right")
    scaled_table.add_column("Unit", style="yellow")

    for ingredient in ingredients:
        name = ingredient.get("name", "Unknown")
        original_qty = ingredient.get("quantity", 0)
        unit = ingredient.get("unit", "")

        # Calculate scaled quantity
        scaled_qty = original_qty * scaling_factor

        # Format numbers nicely
        if scaled_qty == int(scaled_qty):
            scaled_str = str(int(scaled_qty))
        else:
            # For very small amounts, show more precision
            if scaled_qty < 0.1:
                scaled_str = f"{scaled_qty:.3f}".rstrip("0").rstrip(".")
            else:
                scaled_str = f"{scaled_qty:.2f}".rstrip("0").rstrip(".")

        scaled_table.add_row(name, scaled_str, unit)

    console.print(scaled_table)

    # Show recipe notes if available
    notes = recipe_data.get("notes", "").strip()
    if notes:
        console.print(f"\n[bold yellow]📝 Instructions:[/bold yellow]")
        notes_panel = Panel(
            notes,
            border_style="blue",
            padding=(1, 2),
            title="Recipe Instructions",
            title_align="left",
        )
        console.print(notes_panel)


def delete_recipe():
    """Delete an existing recipe"""
    console.clear()
    console.print("[bold red]═══ Delete Recipe ═══[/bold red]\n")

    recipes_dir = "Saved Recipes"

    # Check if recipes directory exists
    if not os.path.exists(recipes_dir):
        console.print(
            "[yellow]No recipes directory found. No recipes to delete![/yellow]"
        )
        return

    # Get all JSON files in the recipes directory
    recipe_files = [f for f in os.listdir(recipes_dir) if f.endswith(".json")]

    if not recipe_files:
        console.print("[yellow]No recipes found. No recipes to delete![/yellow]")
        return

    # Sort recipes alphabetically
    recipe_files.sort()

    console.print(
        f"[yellow]Found {len(recipe_files)} recipe(s) to choose from:[/yellow]\n"
    )
    console.print("[dim]⚠️  This action cannot be undone![/dim]\n")

    # Create a table of available recipes
    recipes_table = Table(show_header=True, header_style="bold magenta")
    recipes_table.add_column("#", style="cyan", width=3)
    recipes_table.add_column("Recipe Name", style="white")
    recipes_table.add_column("Created", style="dim", width=12)
    recipes_table.add_column("Ingredients", style="green", width=8)

    recipe_data_list = []

    for i, filename in enumerate(recipe_files, 1):
        filepath = os.path.join(recipes_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                recipe_data = json.load(f)

            # Get recipe details
            recipe_name = recipe_data.get("name", filename.replace(".json", ""))
            created_date = recipe_data.get("created_date", "Unknown")
            ingredients_count = len(recipe_data.get("ingredients", []))

            # Format date for display
            if created_date != "Unknown":
                try:
                    date_obj = datetime.datetime.fromisoformat(created_date)
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except:
                    formatted_date = "Unknown"
            else:
                formatted_date = "Unknown"

            recipes_table.add_row(
                str(i), recipe_name, formatted_date, f"{ingredients_count} items"
            )
            recipe_data_list.append((filename, recipe_data, filepath))

        except Exception as e:
            console.print(f"[red]Error reading {filename}: {e}[/red]")
            continue

    console.print(recipes_table)

    # Let user select a recipe to delete
    while True:
        try:
            choice = (
                Prompt.ask(
                    f"\n[bold yellow]Enter recipe number to DELETE (1-{len(recipe_data_list)}) or 'q' to cancel[/bold yellow]",
                    default="q",
                )
                .strip()
                .lower()
            )

            if choice == "q":
                console.print("[green]Delete operation cancelled.[/green]")
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(recipe_data_list):
                filename, recipe_data, filepath = recipe_data_list[choice_num - 1]

                # Show the recipe that will be deleted
                recipe_name = recipe_data.get("name", "Unknown Recipe")
                console.print(f"\n[bold red]You are about to delete:[/bold red]")
                console.print(f"[white]Recipe: {recipe_name}[/white]")
                console.print(f"[dim]File: {filename}[/dim]")

                # Show ingredients count
                ingredients = recipe_data.get("ingredients", [])
                console.print(f"[dim]Contains {len(ingredients)} ingredient(s)[/dim]")

                # Double confirmation
                console.print(
                    f"\n[bold red]⚠️  This will permanently delete the recipe![/bold red]"
                )

                if Confirm.ask(
                    f"[red]Are you absolutely sure you want to delete '{recipe_name}'?[/red]"
                ):
                    try:
                        os.remove(filepath)
                        console.print(
                            f"\n[bold green]✓ Recipe '{recipe_name}' has been deleted successfully![/bold green]"
                        )
                        console.print(f"[dim]Removed: {filepath}[/dim]")

                        # Ask if they want to delete another recipe
                        if recipe_data_list and len(recipe_data_list) > 1:
                            if Confirm.ask("\n[cyan]Delete another recipe?[/cyan]"):
                                # Refresh the list and start over
                                delete_recipe()
                                return
                        else:
                            console.print(
                                "\n[yellow]No more recipes to delete.[/yellow]"
                            )

                        return

                    except Exception as e:
                        console.print(
                            f"[bold red]Error deleting recipe: {e}[/bold red]"
                        )
                        return
                else:
                    console.print(
                        f"[green]Delete cancelled. Recipe '{recipe_name}' was not deleted.[/green]"
                    )

                    # Ask if they want to try deleting a different recipe
                    if Confirm.ask("\n[cyan]Delete a different recipe?[/cyan]"):
                        continue
                    else:
                        return
            else:
                console.print(
                    f"[red]Please enter a number between 1 and {len(recipe_data_list)}[/red]"
                )

        except ValueError:
            console.print("[red]Please enter a valid number or 'q' to cancel[/red]")
        except KeyboardInterrupt:
            console.print("\n[green]Delete operation cancelled.[/green]")
            return


if __name__ == "__main__":
    main()
