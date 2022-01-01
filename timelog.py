import time


class TimeLog:
    """
    This class represents a log of times
    """

    def __init__(self):
        self.start = time.perf_counter()
        self.stamps = [self.start]
        self.labels = ["start"]

    def add_stamp(self, label):
        self.stamps.append(time.perf_counter())
        self.labels.append(label)

    def print(self):
        for i in range(1, len(self.stamps)):
            print(f"{self.labels[i]} Time: {self.stamps[i] - self.stamps[i - 1]:.2f}.", end=" ")
        print(f"Total Time: {self.stamps[-1] - self.stamps[0]:.2f}.")


