#!/usr/bin/env python3
import argparse
import logging

import matplotlib.pyplot as plt

from galton import Board
from galton import Particle


def parse_args() -> argparse.Namespace:
    """Parses the command line arguments."""

    parser = argparse.ArgumentParser(description="Process the arguments.")

    parser.add_argument("--intermediate", action="store_true", help="log intermediate results")
    parser.add_argument("--levels", type=int, default=5, help="number of levels")
    parser.add_argument("--particles", type=int, default=1000, help="number of particles")
    parser.add_argument("--plot", action="store_true", help="plot the bar chart of results")
    parser.add_argument("--slots", type=int, default=11, help="number of slots")
    parser.add_argument("--start", type=int, default=5, help="particle start position")

    return parser.parse_args()


def main() -> None:
    """Performs Galton board simulations."""

    # Get the command line arguments
    args = parse_args()

    # Issue warnings based on input parameters
    if args.start != args.slots // 2:
        logging.warning("Simulation incomplete, position-cell mismatch.")
    elif args.start != args.levels:
        logging.warning("Incomplete simulation, position-level mismatch.")
    elif args.slots // 2 != args.levels:
        logging.warning("Simulation incomplete, cell-level mismatch.")

    logging.info("The simulation has started!")
    logging.info(f"Parameters: {args}")

    # A Galton board
    board = Board(args.slots)

    # A promise that if nothing happens, every particle will end up in the middle slot
    board[board.size // 2] = args.particles

    # A list containing particle threads
    particles = [Particle(board, f"p{index}", args.start) for index in range(args.particles)]

    if args.intermediate:
        # Start the threads
        for particle in particles:
            particle.start()
            logging.info(board)

        # Wait till completion
        for particle in particles:
            particle.join()

        logging.info(board)

    else:
        # Start the threads
        for particle in particles:
            particle.start()

        # Wait till completion
        for particle in particles:
            particle.join()

        logging.info(f"Final board: {board}")

    # Verify that all the particles fell into some cell
    assert board.particles == args.particles

    # Plot the bar chart
    if args.plot:
        plt.style.use("ggplot")
        plt.bar(range(args.slots), board.slots, align="center", alpha=0.8)
        plt.xticks(range(args.slots))
        plt.yticks(board.slots)
        plt.title(f"Galton board simulation using {args.particles} threaded particles")
        plt.xlabel("Slot")
        plt.ylabel("Particle")
        plt.show()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )
    main()
