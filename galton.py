"""
Galton board simulation using multithreading

Author: David Oniani
Date: 04/04/2019
License: MIT

                        G A L T O N  B O A R D

        0                         *
                                *   *
        1                     *   *   *
                            *   *   *   *
        3                 *   *   *   *   *
                        *   *   *   *   *   *
        4             *   *   *   *   *   *   *
                    *   *   *   *   *   *   *   *
        5         *   *   *   *   *   *   *   *   *
                *   *   *   *   *   *   *   *   *   *
            |___|___|___|___|___|___|___|___|___|___|___|
"""


import argparse
import matplotlib.pyplot as plt
from galton.particle import Particle
from galton.board import Board


def main():
    """The main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process the arguments.')

    # Number of slots in the Galton board
    parser.add_argument('--slots',
                        type=int,
                        default=11,
                        help='number of cells in the Galton board')

    # Number of particles in the simulation
    parser.add_argument('--particles',
                        type=int,
                        default=1000,
                        help='number of beans in the simulation')

    # Default start position for the particle
    parser.add_argument('--start',
                        type=int,
                        default=5,
                        help='start position of the particle')

    # Number of levels of pegs
    parser.add_argument('--levels',
                        type=int,
                        default=5,
                        help='number of levels of pegs')

    # Get the argparse.Namespace class to obtain the values of the arguments
    args = parser.parse_args()

    # Print out the possible warning messages
    def warning(message): print(f"\033[93m{message}\033[0m")

    if args.start != args.slots // 2:
        warning("Simulation incomplete, position-cell mismatch.\n")

    elif args.start != args.levels:
        warning("Incomplete simulation, position-level mismatch.\n")

    elif args.slots // 2 != args.levels:
        warning("Simulation incomplete, cell-level mismatch.\n")

    # Print the message
    print("\033[92mThe simulation has started!\033[0m\n\n"
          "\033[4mInformation\033[0m\n"
          f"NUMBER OF PARTICLES:   {args.particles}\n"
          f"NUMBER OF CELLS:       {args.slots}\n"
          f"START POSITION:        {args.start}\n"
          f"NUMBER OF LEVELS:      {args.levels}")

    # A Galton board
    board = Board(args.slots)

    # A list for threads
    particles = [Particle(f"p{index}", args.start, board)
                 for index
                 in range(args.particles)]

    # Start the threads
    for particle in particles:
        particle.start()

    # Ensure all of the threads have finished
    for particle in particles:
        particle.join()

    # Get the list of positions of all particles
    positions = [particle.position for particle in particles]

    # Arrange particles in the slots according to their positions
    for index in range(args.slots):
        board[index] = positions.count(index)

    # Print out board filled with particles
    print("FINAL BOARD:".ljust(22), board)

    # Verify that all the particles fell into some cell
    assert board.particles_number == args.particles

    # Plot the bar chart
    plt.bar(list(range(args.slots)), board.slots, align='center', alpha=0.5)
    plt.xticks(range(args.slots))
    plt.yticks(board)
    plt.title(f"Galton board simulation using {args.particles} "
              "threaded particles")
    plt.xlabel("Cell Number")
    plt.ylabel("Particle Number")
    plt.show()


if __name__ == "__main__":
    main()
