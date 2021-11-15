#!/usr/bin/env python3
import argparse
import logging

import matplotlib.pyplot as plt

from galton import Board, Particle


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

    args = parse_args()

    if args.start != args.slots // 2:
        logging.warning("Simulation incomplete, position-cell mismatch")
    elif args.start != args.levels:
        logging.warning("Incomplete simulation, position-level mismatch")
    elif args.slots // 2 != args.levels:
        logging.warning("Simulation incomplete, cell-level mismatch")

    logging.info("The simulation has started!")
    logging.info(f"Parameters: {args}")

    # NOTE: If nothing happens, every particle will end up in `args.start` position
    board = Board(args.slots)
    board[args.start] = args.particles
    particles = [Particle(board, f"p{index}", args.start) for index in range(args.particles)]

    # Start the threads and optionally, log the results
    if args.intermediate:
        for particle in particles:
            particle.start()
            logging.info(board)
    else:
        for particle in particles:
            particle.start()

    # Wait till completion
    for particle in particles:
        particle.join()

    logging.info(f"Final board: {board}")

    # Verify that every particles fell into some cell
    assert board.particles == args.particles

    if args.plot:
        plt.style.use("ggplot")
        plt.bar(range(args.slots), board.slots, align="center", alpha=0.8)
        plt.xticks(range(args.slots))
        plt.yticks(board.slots)
        plt.xlabel("Slot")
        plt.ylabel("Particle")
        plt.title(f"Galton board simulation using {args.particles} threaded particles")
        plt.show()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )
    main()
