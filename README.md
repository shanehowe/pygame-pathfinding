# Python Pathfinding Game

This is a simple pathfinding game coded in Python, using the Pygame library. The game allows the user to pick a starting tile and an ending tile, and then create a maze to search through. The game uses breadth-first search to find the path from the starting tile to the ending tile.

## Installation

To install the required packages for the game, run the following command in your terminal:

```bash
pip install -r requirements.txt
```


This will install Pygame, which is necessary to run the game.

## How to Play

To start the game, simply run the `game.py` file in your Python environment. This will open up a window with a grid of tiles.

To select the starting tile, simply click on any tile in the grid. This will turn the tile blue and indicate that it is the starting point.

To select the ending tile, click on another tile. This will turn the tile green and indicate that it is the end point.

To create a maze, click and drag your mouse over the tiles that you want to turn into walls. This will turn the tiles red and make them impassable.

To find the path from the starting tile to the ending tile, press run button. The game will use breadth-first search to find the shortest path through the maze.
