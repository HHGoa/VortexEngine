from Engine.Vortex import Vortex
from ursina import *

class TreasureHuntGame(Vortex):
    def __init__(self, PrivateKey="", Address="", Chain="Aptos", ApiKey=False, **kwargs):
        super().__init__(PrivateKey, Address, Chain, ApiKey, **kwargs)
        self.treasures = []
        self.setup_game()

    def setup_game(self):
        # Create background, treasure entities, setup UI and controls
        self.create_background()
        self.create_treasure_entities()
        self.setup_ui()
        self.setup_controls()

    def create_background(self):
        # Create a background or environment for the game
        self.Object(model='plane', scale=(50, 1, 50), color=self.color('#87ceeb'), position=(0, -1, 0))  # Sky-blue background
        self.Object(model='plane', scale=(50, 1, 50), color=self.color('#228B22'), position=(0, -2, 0))  # Grass-green ground
        print("Background created")

    def create_treasure_entities(self):
        # Create some treasure entities
        for i in range(5):
            x, y, z = (i * 2, 0, random.uniform(-10, 10))
            color = self.color('#ffcc00')  # Gold color
            treasure = self.Object(model='cube', color=color, position=(x, y, z), scale=(1, 1, 1), collider='box')
            self.treasures.append(treasure)
            print(f"Created treasure at {(x, y, z)}")  # Debugging

    def setup_ui(self):
        # Add a simple UI label for game instructions
        self.instruction_label = self.Label(text="Find the treasures!", position=(0, 0.4), scale=2, color=self.color('#ffffff'))
        print("UI setup complete")  # Debugging

    def setup_controls(self):
        # Setup first-person controller for player movement
        self.controller = self.firstPersonController()
        self.controller.speed = 5  # Increase speed for more dynamic movement
        self.controller.jump_height = 2  # Increase jump height
        print("Controls setup complete")  # Debugging

    def update(self):
        for treasure in self.treasures:
            if treasure.intersects(self.controller).hit:
                print(f"Treasure found at {treasure.position}")
                self.treasures.remove(treasure)
                destroy(treasure)
                self.add_treasure_to_blockchain(unique_key=str(treasure), position=treasure.position)
                break

    def add_treasure_to_blockchain(self, unique_key, position):
        try:
            # Here you would interact with the blockchain to register the treasure
            print(f"Registered treasure at {position} with unique key {unique_key}")
        except Exception as e:
            print(f"Error adding treasure to blockchain: {e}")

    def run(self, ipfs_api_addr, ipfs_api_port, blockchain_api_key, private_key, address):
        print("Starting game...")
        self.app.run()
        super().run(ipfs_api_addr, ipfs_api_port, blockchain_api_key, private_key, address)

if __name__ == "__main__":
    # Initialize the game with the private key, address, and chain
    game = TreasureHuntGame(
        PrivateKey="0xa4b20ab4faf41ee253f57dc8c5724a0aec3e7efa27600ffb83ec4d64be097225", 
        Address="0x40a75d0c4c993c0a75d1167bf6fc40f6892a44578aa272aa12a6f50d7ec1192d", 
        Chain="Aptos", 
        ApiKey=False
    )
    game.run(
        ipfs_api_addr="ipfs.infura.io", 
        ipfs_api_port=5001, 
        blockchain_api_key="e6300ae2ffe84989b84921888cc2b09e", 
        private_key="0xa4b20ab4faf41ee253f57dc8c5724a0aec3e7efa27600ffb83ec4d64be097225", 
        address="0x40a75d0c4c993c0a75d1167bf6fc40f6892a44578aa272aa12a6f50d7ec1192d"
    )
