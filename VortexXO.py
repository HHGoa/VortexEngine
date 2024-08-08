from Engine.Vortex import Vortex
from ursina import *

class TicTacToeGame(Vortex):
    def __init__(self, PrivateKey="", Address="", Chain="Aptos", ApiKey=False, **kwargs):
        super().__init__(PrivateKey, Address, Chain, ApiKey, **kwargs)
        self.board = [[None for x in range(3)] for y in range(3)]
        self.player = Entity(name='o', color=color.azure)
        self.cursor = Tooltip(self.player.name, color=self.player.color, origin=(0, 0), scale=4, enabled=True)
        self.cursor.background.color = color.clear
        self.setup_game()
        self.display_info()

    def setup_game(self):
        camera.orthographic = True
        camera.fov = 4
        camera.position = (1, 1)
        Text.default_resolution *= 2

        bg = Entity(parent=scene, model='quad', texture='shore', scale=(16, 8), z=10, color=color.light_gray)
        mouse.visible = False

        for y in range(3):
            for x in range(3):
                b = Button(parent=scene, position=(x, y))
                self.board[x][y] = b
                b.on_click = self.create_on_click(b)

    def create_on_click(self, b):
        def on_click():
            b.text = self.player.name
            b.color = self.player.color
            b.collision = False
            self.check_for_victory()

            if self.player.name == 'o':
                self.player.name = 'x'
                self.player.color = color.orange
            else:
                self.player.name = 'o'
                self.player.color = color.azure

            self.cursor.text = self.player.name
            self.cursor.color = self.player.color
        return on_click

    def check_for_victory(self):
        name = self.player.name

        won = (
            (self.board[0][0].text == name and self.board[1][0].text == name and self.board[2][0].text == name) or # across the bottom
            (self.board[0][1].text == name and self.board[1][1].text == name and self.board[2][1].text == name) or # across the middle
            (self.board[0][2].text == name and self.board[1][2].text == name and self.board[2][2].text == name) or # across the top
            (self.board[0][0].text == name and self.board[0][1].text == name and self.board[0][2].text == name) or # down the left side
            (self.board[1][0].text == name and self.board[1][1].text == name and self.board[1][2].text == name) or # down the middle
            (self.board[2][0].text == name and self.board[2][1].text == name and self.board[2][2].text == name) or # down the right side
            (self.board[0][0].text == name and self.board[1][1].text == name and self.board[2][2].text == name) or # diagonal /
            (self.board[0][2].text == name and self.board[1][1].text == name and self.board[2][0].text == name))   # diagonal \

        if won:
            print('winner is:', name)
            self.cursor.text = ''
            mouse.visible = True
            Panel(z=1, scale=10, model='quad')
            t = Text(f'player\n{name}\nwon!', scale=3, origin=(0, 0), background=True)
            t.create_background(padding=(.5, .25), radius=Text.size / 2)
            t.background.color = self.player.color.tint(-.2)

    def display_info(self):
        info_text = (
            "package_folder: C:\\Python312\\Lib\\site-packages\\ursina\n"
            "asset_folder: .\n"
            "{'config': {'PrivateKey': '0xa4b20ab4faf41ee253f57dc8c5724a0aec3e7efa27600ffb83ec4d64be097225', "
            "'Address': '0x40a75d0c4c993c0a75d1167bf6fc40f6892a44578aa272aa12a6f50d7ec1192d', 'Chain': 'Aptos', "
            "'appInstance': <ursina.main.Ursina object at 0x00000253CFD86A80>}}\n"
            "Starting game...\n"
            "os: Windows\n"
            "development mode: True\n"
            "application successfully started\n"
            "info: changed aspect ratio: 1.778 -> 1.77\n"
        )
        self.info_label = Text(info_text, position=(-0.85, 0.4), scale=0.8, origin=(0, 0), background=True, color=color.white)

    def run(self, ipfs_api_addr, ipfs_api_port, blockchain_api_key, private_key, address):
        print("Starting game...")
        self.app.run()
        super().run(ipfs_api_addr, ipfs_api_port, blockchain_api_key, private_key, address)

if __name__ == "__main__":
    # Initialize the game with the private key, address, and chain
    game = TicTacToeGame(
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
