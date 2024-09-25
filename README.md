# Pygame Top-Down Shooter
Overview

This is a simple 2D top-down shooter game developed using Pygame. The player controls a character that shoots projectiles at incoming enemies, aiming to score points while avoiding letting enemies pass by.

How to Play

Movement:

Use the Arrow Keys or WASD to move the player character around the screen.

Shooting:

Press the Spacebar to shoot projectiles towards the right side of the screen.

Objective:

Score points by hitting enemies. The game ends when you reach a score of 10,000 points.

Missed Enemies:

If enemies pass off the left side of the screen, points will be deducted for each missed enemy. You can miss a maximum of 5 enemies before facing a penalty.

Restarting the Game:

After winning, press R to restart the game.
Game Functions
Player Movement: The player character can move in four directions and shoot projectiles.
Enemy Spawning: Enemies spawn at regular intervals from the right side of the screen.
Scoring System: Points are awarded based on the color of the enemies hit:
Blue (slowest): +75 points
Green (middle speed): +100 points
Red (fastest): +125 points
Important Parts of the Game
Player Class: Handles player movement and shooting.
Projectile Class: Manages the projectiles shot by the player, including their movement and removal upon leaving the screen.
Enemy Class: Manages enemy properties, including speed and color, and removes them when they leave the screen.
Game State: Keeps track of the current state of the game (playing or won).
Collision Detection: Detects when projectiles hit enemies and updates the score accordingly.
Getting Started
To run the game, ensure you have Python and Pygame installed on your system. Clone the repository and run the main Python file.

Requirements
Python 3.x
Pygame
