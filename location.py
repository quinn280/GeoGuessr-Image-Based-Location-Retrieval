class Location:
    """
    This class represents a single location
    """

    estimated_heading = "N/A"

    def __init__(self, latitude, longitude, heading, file_path):
        """
        This is the initializer for location class.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.file_path = file_path

        self.proximity = "N/A"
        self.CBIR_score = "N/A"

    def coordinate_str(self):
        return f"{self.latitude}, {self.longitude}"

    def location_str(self):
        ...  # use geopy to return location string from coordinates

    def google_map_link(self):
        return f'https://maps.google.com/?q=' \
               f'{self.latitude},{self.longitude}&ll={self.latitude},{self.longitude}&z=7'

    def update_proximity(self):
        """
        Calculates and updates new proximity value with the class variable estimated heading
        """
        self.proximity = abs(self.heading - Location.estimated_heading) % 360
        if self.proximity > 180:
            self.proximity = 360 - self.proximity

    def reset(self):
        """
        Resets proximity and CBIR score
        """
        self.proximity = "N/A"
        self.CBIR_score = "N/A"

    def __str__(self):
        """
        Return a str that that shows all location info.
        """
        return f"Coordinates: {self.coordinate_str()}\nCBIR Score: {self.CBIR_score:.2f}. " \
               f"Proximity: {self.proximity:.2f}. Estimated Heading: {Location.estimated_heading:.2f}. " \
               f"Actual Heading: {self.heading:.2f}.\nGoogle Map Link: {self.google_map_link()}"
