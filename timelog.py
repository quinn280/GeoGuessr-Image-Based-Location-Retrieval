import time


class TimeLog:
    """
    This class represents a log of times
    """

    def __init__(self):
        """
        This is the initializer for the TimeLog class
        """
        self.stamps = [time.perf_counter()]
        self.labels = ["start"]

    def add_stamp(self, label):
        """
        Appends time stamps and a label to two parallel arrays
        :param label:
        :return: n/a
        """
        self.stamps.append(time.perf_counter())
        self.labels.append(label)

    def print(self):
        """
        Prints label along with duration of each interval. Also prints total time.
        :return: n/a
        """
        for i in range(1, len(self.stamps)):
            print(f"{self.labels[i]} Time: {self.stamps[i] - self.stamps[i - 1]:.2f}.", end=" ")
        print(f"Total Time: {self.stamps[-1] - self.stamps[0]:.2f}.")


