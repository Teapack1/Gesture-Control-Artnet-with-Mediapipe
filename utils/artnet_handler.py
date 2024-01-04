from pyartnet import ArtNetNode
import asyncio

class ArtnetHandler:
    def __init__(self, ip_address, port=6454):
        self.node = ArtNetNode(ip_address, port)
        self.universe = self.node.add_universe(0)
        self.channels = self.universe.add_channel(start=1, width=3, channel_name="class")
        
        self.last_sent_data = None
        self.previous_indices = [None, None, None]  # Store the previous 3 indices

    async def send_data(self, index, landmark, weight, height):
        if index == 2:
            landmark_x = landmark[8][0]
            landmark_y = landmark[8][1]
            print(f"l_X: {landmark_x}")
            print(f"l_Y: {landmark_y}")
            
            x_norm = int(((landmark_x)/weight) * 255)+25
            y_norm = int((landmark_y/height) * 255)+25
            print(f"X: {x_norm}")
            print(f"Y: {y_norm}")
            
            self.channels.add_fade([index, x_norm, y_norm], 0)
            await self.channels

        else:
            self.channels.add_fade([index, 0, 0], 0)
            await self.channels
        
    def is_valid_data(self, index):
        # Check if the last two indices match the current index and are different from the one before
        if index == 2 or (self.previous_indices[-1] == index and self.previous_indices[-2] != index):
        #if self.previous_indices[-1] != index:
            valid = True
        else:
            valid = False

        # Update the list of previous indices
        self.previous_indices.pop(0)
        self.previous_indices.append(index)

        return valid


# Example usage:
# sender = ArtNetSender("192.168.1.2")  # Replace with your Art-Net node IP
# if sender.is_valid_data(classification_index):
#     sender.send_data(classification_index)
