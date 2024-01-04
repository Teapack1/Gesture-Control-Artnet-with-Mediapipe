# Import necessary libraries
from pyartnet import ArtNetNode


class ArtnetHandler:
    def __init__(self, ip_address, port=6454):
        self.node = ArtNetNode(ip_address, port)
        self.last_sent_data = None
        self.universe = 0  # Set your Art-Net universe here
        self.previous_indices = [None, None, None]  # Store the previous 3 indices

    def send_data(self, index, landmark_list):
        # Check if data has changed from the last sent data
        if index != self.last_sent_data:
            self.last_sent_data = index
            # Prepare and send the Art-Net packet
            # Assuming 'data' is an integer representing the classification index
            if index == 2:
                dmx_data = [index] + landmark_list + [0] * (511 - len(landmark_list))
            else:
                dmx_data = [index] + [0] * 511  # Art-Net DMX packets are 512 bytes
            self.node.set_channel(self.universe, 1, dmx_data)
            self.node.flush()

    def is_valid_data(self, index):
        # Check if the index is different from the previous 3 indices
        if index not in self.previous_indices:
            self.previous_indices.pop(0)  # Remove the oldest index
            self.previous_indices.append(index)  # Add the new index
            return True
        else:
            return False


# Example usage:
# sender = ArtNetSender("192.168.1.2")  # Replace with your Art-Net node IP
# if sender.is_valid_data(classification_index):
#     sender.send_data(classification_index)
