#!/usr/bin/env python3
###########################################################################
# Date created:  June 29 2025
# Date finished:
# Purpose:       Automate Recipe figures
# Author:        Joseph LoVerso
###########################################################################
import os
import json
import datetime

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
        elif choice == '1':
            console.clear()
            console.print("[bold blue]Calculating recipe...[/bold blue]")
            input("Press Enter to continue...")
        elif choice == '2':
            console.clear()
            console.print("[bold blue]Viewing recipes...[/bold blue]")
            input("Press Enter to continue...")
        elif choice == '3':
            new_recipe()
            input("Press Enter to continue...")
        elif choice == '4':
            console.clear()
            console.print("[bold blue]Deleting recipe...[/bold blue]")
            input("Press Enter to continue...")

def drawMenu():
    width = 42
    lines = [
        "Recipe Automation Program",
        "",  # Empty line
        "1. Calculate recipe",
        "2. View existing recipes",
        "3. New recipe",
        "4. Delete recipe",
        "Q. Exit",
        ""   # Empty line
    ]

    # Top border
    print("╔" + "═" * width + "╗")

    # Title with separator
    title = lines[0]
    padding = (width - len(title)) // 2
    print("║" + " " * padding + title + " " * (width - len(title) - padding) + "║")
    print("╠" + "═" * width + "╣")

    # Menu items
    for line in lines[1:]:
        if line == "":
            print("║" + " " * width + "║")
        else:
            # Left-align menu items with some padding
            padded_line = "  " + line
            remaining_space = width - len(padded_line)
            print("║" + padded_line + " " * remaining_space + "║")

    # Bottom border
    print("╚" + "═" * width + "╝")

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
            show_choices=False
        ).lower()

        if choice in ['1', '2', '3', '4']:
            return choice
        elif choice == 'q':
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
        recipe_name = Prompt.ask("[bold cyan]Enter recipe name[/bold cyan]").strip()
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
    console.print("[dim]Press Enter twice when finished, or type 'DONE' on a line by itself[/dim]")

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
        unit = Prompt.ask(f"[yellow]Unit of measurement for {ingredient_name}[/yellow] (e.g., cups, tbsp, lbs)").strip()
        if not unit:
            console.print("[red]Unit cannot be empty.[/red]")
            continue

        # Get quantity (float value)
        while True:
            try:
                quantity_str = Prompt.ask(f"[yellow]Quantity of {ingredient_name} in {unit}[/yellow]")
                quantity = float(quantity_str)
                break
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")

        # Add ingredient to list
        ingredients.append({
            "name": ingredient_name,
            "quantity": quantity,
            "unit": unit
        })

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
        "created_date": datetime.datetime.now().isoformat()
    }

    # Display recipe for confirmation
    display_recipe_preview(recipe_data)

    # Confirm before saving
    if Confirm.ask("\n[bold green]Save this recipe?[/bold green]"):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(recipe_data, f, indent=2, ensure_ascii=False)

            console.print(f"\n[bold green]✓ Recipe '{recipe_name}' saved successfully![/bold green]")
            console.print(f"[dim]Saved to: {filepath}[/dim]")

        except Exception as e:
            console.print(f"[bold red]Error saving recipe: {e}[/bold red]")
    else:
        console.print("[yellow]Recipe not saved.[/yellow]")

def display_recipe_preview(recipe_data):
    """Display a formatted preview of the recipe"""
    console.print("\n" + "="*60)
    console.print(f"[bold cyan]Recipe Preview[/bold cyan]")
    console.print("="*60)

    # Recipe name
    console.print(f"\n[bold yellow]Name:[/bold yellow] {recipe_data['name']}")

    # Notes
    if recipe_data['notes'].strip():
        console.print(f"\n[bold yellow]Notes/Instructions:[/bold yellow]")
        # Display notes in a panel for better formatting
        notes_panel = Panel(recipe_data['notes'], border_style="dim")
        console.print(notes_panel)

    # Ingredients table
    if recipe_data['ingredients']:
        console.print(f"\n[bold yellow]Ingredients:[/bold yellow]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Ingredient", style="cyan")
        table.add_column("Quantity", style="green", justify="right")
        table.add_column("Unit", style="yellow")

        for ingredient in recipe_data['ingredients']:
            # Format quantity to remove unnecessary decimal places
            qty = ingredient['quantity']
            if qty == int(qty):
                qty_str = str(int(qty))
            else:
                qty_str = f"{qty:.2f}".rstrip('0').rstrip('.')

            table.add_row(
                ingredient['name'],
                qty_str,
                ingredient['unit']
            )

        console.print(table)

    console.print("="*60)

def display_full_recipe(recipe_data):
    """Display a complete recipe with all details"""
    console.clear()

    # Recipe header
    recipe_name = recipe_data.get('name', 'Unknown Recipe')
    console.print(f"[bold cyan]{'═' * 20} {recipe_name} {'═' * 20}[/bold cyan]")

    # Created date
    created_date = recipe_data.get('created_date', 'Unknown')
    if created_date != 'Unknown':
        try:
            date_obj = datetime.datetime.fromisoformat(created_date)
            formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
            console.print(f"[dim]Created: {formatted_date}[/dim]\n")
        except:
            console.print(f"[dim]Created: {created_date}[/dim]\n")

    # Ingredients section
    ingredients = recipe_data.get('ingredients', [])
    if ingredients:
        console.print("[bold yellow]🥘 Ingredients:[/bold yellow]")

        ingredients_table = Table(show_header=True, header_style="bold magenta", box=None)
        ingredients_table.add_column("Ingredient", style="cyan")
        ingredients_table.add_column("Amount", style="green", justify="right")
        ingredients_table.add_column("Unit", style="yellow")

        for ingredient in ingredients:
            qty = ingredient.get('quantity', 0)
            # Format quantity nicely
            if qty == int(qty):
                qty_str = str(int(qty))
            else:
                qty_str = f"{qty:.2f}".rstrip('0').rstrip('.')

            ingredients_table.add_row(
                ingredient.get('name', 'Unknown'),
                qty_str,
                ingredient.get('unit', '')
            )

        console.print(ingredients_table)
        console.print()

    # Notes/Instructions section
    notes = recipe_data.get('notes', '').strip()
    if notes:
        console.print("[bold yellow]📝 Instructions:[/bold yellow]")
        notes_panel = Panel(
            notes,
            border_style="blue",
            padding=(1, 2),
            title="Recipe Notes",
            title_align="left"
        )
        console.print(notes_panel)
    else:
        console.print("[dim]No instructions provided.[/dim]")

    console.print(f"\n[bold cyan]{'═' * (42 + len(recipe_name))}[/bold cyan]")

    # Recipe name
    console.print(f"\n[bold yellow]Name:[/bold yellow] {recipe_data['name']}")

    # Notes
    if recipe_data['notes'].strip():
        console.print(f"\n[bold yellow]Notes/Instructions:[/bold yellow]")
        # Display notes in a panel for better formatting
        notes_panel = Panel(recipe_data['notes'], border_style="dim")
        console.print(notes_panel)

    # Ingredients table
    if recipe_data['ingredients']:
        console.print(f"\n[bold yellow]Ingredients:[/bold yellow]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Ingredient", style="cyan")
        table.add_column("Quantity", style="green", justify="right")
        table.add_column("Unit", style="yellow")

        for ingredient in recipe_data['ingredients']:
            # Format quantity to remove unnecessary decimal places
            qty = ingredient['quantity']
            if qty == int(qty):
                qty_str = str(int(qty))
            else:
                qty_str = f"{qty:.2f}".rstrip('0').rstrip('.')

            table.add_row(
                ingredient['name'],
                qty_str,
                ingredient['unit']
            )

        console.print(table)

    console.print("="*60)

if __name__ == "__main__":
    main()
