# main.py
import flet as ft
from game_logic import BalatroPoker

def main(page: ft.Page):
    page.title = "Balatro Poker Assistant"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Create the game instance
    game = BalatroPoker(page)
    
    # Set up the game
    game.start_round()
    
    # Display the UI
    page.update()

if __name__ == "__main__":
    ft.app(target=main)