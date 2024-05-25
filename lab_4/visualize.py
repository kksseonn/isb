import matplotlib.pyplot as plt
import logging


logging.basicConfig(level=logging.INFO)


def visualize_time_measurements(process_counts: list, time_measurements: list) -> None:
    """Visualize time measurements on a plot.

    Args:
        process_counts (list): List of process counts.
        time_measurements (list): List of corresponding time measurements.
    """
    try:
        fig = plt.figure(figsize=(15, 5))
        plt.plot(
            process_counts,
            time_measurements,
            linestyle=":",
            color="black",
            marker="x",
            markersize=10,
        )
        plt.bar(process_counts, time_measurements)
        plt.xlabel("Number of Processes")
        plt.ylabel("Time in Seconds")
        plt.title("Time vs Number of Processes")
        plt.show()
    except Exception as e:
        logging.error(f"An error occurred while visualizing time measurements: {e}")
