# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "colorama", "matplotlib"]
# ///

# Run the server first, then run the client

import random
import socket
from multiprocessing import Manager, Pool
from time import sleep, time
from typing import Any

from colorama import Fore, Style, init
from matplotlib import pyplot as plt


def f(t: tuple[str, socket.socket, Any, Any]) -> tuple[str, float, float]:
    """Process function that sends messages to the echo server.

    Args:
        t: Tuple containing (name, socket, lock0, lock1)

    Returns:
        Tuple of (name, start_time, end_time)
    """
    name, s, l0, l1 = t
    start_time = time()
    n = random.randint(1, 10)
    for i in range(n):
        l0.acquire()

        greetings = [
            f"{name} ({i}): hello",
            f"{name} ({i}): world",
            f"{name} ({i}): what's up",
        ]

        print(Fore.GREEN + greetings[0] + Style.RESET_ALL)
        s.send(greetings[0].encode())
        print(s.recv(1024).decode())

        sleep(random.random() * 1)

        l1.acquire()

        print(Fore.YELLOW + greetings[1] + Style.RESET_ALL)
        s.send(greetings[1].encode())
        print(s.recv(1024).decode())
        l0.release()

        sleep(random.random() * 1)
        print(Fore.CYAN + greetings[2] + Style.RESET_ALL)
        l1.release()

    end_time = time()
    return name, start_time, end_time


def main() -> None:
    """Main function demonstrating multiprocess socket communication."""
    with Manager() as manager:
        l0 = manager.Lock()
        l1 = manager.Lock()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 12345))

        pool_num = 3
        task_num = 10

        finished_order: list[tuple[str, float, float]] = []

        with Pool(pool_num) as pool:
            results = pool.imap_unordered(
                f, [(f"p{i}", s, l0, l1) for i in range(task_num)]
            )

            for _i, result in enumerate(results):
                name, start_time, end_time = result
                elapsed_time = end_time - start_time
                print(f"{name} took {elapsed_time:.2f} seconds")
                finished_order.append((name, start_time, end_time))

        # Print the finished order
        for name, start_time, end_time in finished_order:
            elapsed = end_time - start_time
            print(
                f"{name} took {elapsed:.2f} seconds. "
                f"(start: {start_time:.2f}, end: {end_time:.2f})"
            )

        # Plotting the execution times
        plt.figure(figsize=(10, 6))
        for i, (name, start_time, end_time) in enumerate(finished_order):
            plt.plot([start_time, end_time], [i, i], marker="o", label=name)

        plt.xlabel("Time (seconds)")
        plt.ylabel("Task Number")
        plt.title("Task Execution Times")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    # Initialize colorama
    init()

    main()
