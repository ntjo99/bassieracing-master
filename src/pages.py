# BassieRacing - Pages

# Import modules
from constants import *
import math
from objects import *
import os
import random
# import tkinter.filedialog
from utils import *
import webbrowser
from widgets import *
import sys

# The page class
class Page:
    # Create empty page
    def __init__(self, game, backgroundColor = None):
        self.game = game

        # Pick random background color when background color null
        if backgroundColor != None:
            self.backgroundColor = backgroundColor
        else:
            self.backgroundColor = (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))

        # Create widgets
        self.widgets = []
        self.topWidgets = []
        self.create_widgets()

    # Handle page events
    def handle_event(self, event):
        # Send all events to the top widgets
        for widget in reversed(self.topWidgets):
            if widget.handle_event(event):
                return True

        # Send all events to the widgets
        for widget in reversed(self.widgets):
            if widget.handle_event(event):
                return True

        # On resize recreated widgets
        if event.type == pygame.VIDEORESIZE:
            self.widgets = []
            self.topWidgets = []
            self.create_widgets()

        return False

    # Update page
    def update(self, delta):
        pass

    # Draw page
    def draw(self, surface):
        # Draw background
        surface.fill(self.backgroundColor)

        # Draw widgets
        for widget in self.widgets:
            widget.draw(surface)

        # Draw top widgets
        for widget in self.topWidgets:
            widget.draw(surface)

# The intro page class
class IntroPage(Page):
    # Create menu page
    def __init__(self, game):
        Page.__init__(self, game, Color.WHITE)

        # Load and play intro sound
        if game.settings['sound-effects']['enabled']:
            game.introSound.set_volume(0.75)
        else:
            game.introSound.set_volume(0)
        self.introSoundChannel = game.introSound.play()
        self.introSoundChannel.set_endevent(pygame.USEREVENT + 2)

    # Create intro page widgets
    def create_widgets(self):
        y = (self.game.height - (256 + 32 + 96 + 16 + 64)) // 2
        self.widgets.append(Image(self.game, 'assets/images/logo.png', 0, y, self.game.width, 256))
        y += 256 + 32
        self.widgets.append(Label(self.game, 'BassieSoft', 0, y, self.game.width, 96, self.game.titleFont, Color.BLACK))
        y += 96 + 16
        self.widgets.append(Label(self.game, 'Presents a new racing game...', 0, y, self.game.width, 64, self.game.textFont, Color.BLACK))

    # Handle intro page events
    def handle_event(self, event):
        if Page.handle_event(self, event):
            return True

        if event.type == pygame.MOUSEBUTTONUP:
            self.introSoundChannel.set_endevent()
            if self.game.settings['sound-effects']['enabled']:
                self.game.clickSound.play()
            self.game.page = MenuPage(self.game)
            return True

        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.introSoundChannel.set_endevent()
            self.game.page = MenuPage(self.game)

        if event.type == pygame.USEREVENT + 2:
            self.game.page = MenuPage(self.game)

        return False

# The menu page class
class MenuPage(Page):
    # Create menu page
    def __init__(self, game):
        Page.__init__(self, game)
        

        # Start music if enabled in settings
        if game.settings['music']['enabled'] and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(0, game.settings['music']['position'])

    # Create menu page widgets
    def create_widgets(self):     
        y = ((self.game.height - 32) - (72 + (64 + 16) * 5)) // 2
        self.widgets.append(Label(self.game, 'BassieRacing', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 16
        self.widgets.append(Button(self.game, 'Play', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.play_button_clicked))
        y += 64 + 16
        
        self.widgets.append(Button(self.game, 'Map Editor', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.edit_button_clicked))
        y += 64 + 16
        # self.widgets.append(Button(self.game, 'Help', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.help_button_clicked))
        # y += 64 + 16
        self.widgets.append(Button(self.game, 'Settings', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.settings_button_clicked))
        y += 64 + 16
        self.widgets.append(Button(self.game, 'Exit', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.exit_button_clicked))

        if self.game.newVersionAvailable != None:
            self.widgets.append(Label(self.game, 'A newer version (v' + self.game.newVersionAvailable + ') is available', 16, 16, self.game.width - 16 - 256 - 16, 32, self.game.textFont, Color.WHITE, TextAlign.LEFT, self.new_version_label_clicked))
        self.widgets.append(Label(self.game, 'v' + Config.VERSION, self.game.width - 16 - 256, 16, 256, 32, self.game.textFont, Color.WHITE, TextAlign.RIGHT, self.version_label_clicked))

        self.widgets.append(Label(self.game, 'Made by Bastiaan van der Plaat', 0, self.game.height - 64 - 16, self.game.width, 64, self.game.textFont, Color.WHITE, TextAlign.CENTER, self.footer_label_clicked))

    # New version label clicked
    def new_version_label_clicked(self):
        webbrowser.open_new(Config.GIT_REPO_URL + '/releases')

    # Version label clicked
    def version_label_clicked(self):
        webbrowser.open_new(Config.GIT_REPO_URL)

    # Play button clicked
    def play_button_clicked(self):
        self.game.page = PlayPage(self.game)

    # Edit button clicked
    def edit_button_clicked(self):
        self.game.page = EditorPage(self.game)

    # Help button clicked
    def help_button_clicked(self):
        self.game.page = HelpPage(self.game)

    # Settings button clicked
    def settings_button_clicked(self):
        self.game.page = SettingsPage(self.game)

    # Exit button clicked
    def exit_button_clicked(self):
        self.game.page = ExitPage(self.game)

    # Footer label clicked
    def footer_label_clicked(self):
        webbrowser.open_new('https://bastiaan.ml/')

# The play page class
class PlayPage(Page):
    # Create play page
    def __init__(self, game):
        Page.__init__(self, game)
        # self.game.page = SelectMapPage(game, GameMode.SINGLE_PLAYER)

    # Create play page widgets
    def create_widgets(self):
        y = (self.game.height - (96 + (64 + 16) * 3 + 24 + 64)) // 2
        self.widgets.append(Label(self.game, 'Select a game mode', 0, y, self.game.width, 96, self.game.titleFont, Color.WHITE))
        y += 96 + 16
        self.widgets.append(Button(self.game, 'Single Player', self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.single_player_button_clicked))
        y += 64 + 16
        self.widgets.append(Button(self.game, 'Split Screen', self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.split_screen_button_clicked))
        y += 64 + 16
        self.widgets.append(Button(self.game, 'Multiplayer', self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.multiplayer_button_clicked))
        y += 64 + 24
        self.widgets.append(Button(self.game, 'Back', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

    # Single Player button clicked
    def single_player_button_clicked(self):
        self.game.page = SelectMapPage(self.game, GameMode.SINGLE_PLAYER)

    # Split Screen button clicked
    def split_screen_button_clicked(self):
        self.game.page = SelectMapPage(self.game, GameMode.SPLIT_SCREEN)

    # Multiplayer button clicked
    def multiplayer_button_clicked(self):
        self.game.page = MultiplayerPage(self.game)

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = MenuPage(self.game)

# The multiplayer page class
class MultiplayerPage(Page):
    # Create multiplayer page
    def __init__(self, game):
        Page.__init__(self, game)

    # Create multiplayer page widgets
    def create_widgets(self):
        y = (self.game.height - (72 + 24 + 64 + 24 + 320 + 24 + 64)) // 2
        self.widgets.append(Label(self.game, 'Multiplayer', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 24
        self.widgets.append(Button(self.game, 'Host a game', self.game.width // 6, y, self.game.width // 3 - 8, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.host_button_clicked))
        self.widgets.append(Button(self.game, 'Direct connect', self.game.width // 6 + (self.game.width // 3 - 8) + 16, y, (self.game.width // 3 - 8), 64, self.game.textFont, Color.BLACK, Color.WHITE, self.direct_connect_button_clicked))
        y += 64 + 24
        self.widgets.append(Label(self.game, 'Hosted games in your network will appear here', 0, y, self.game.width, 320, self.game.textFont, Color.WHITE))
        y += 320 + 24
        self.widgets.append(Button(self.game, 'Back', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

    # Host button clicked
    def host_button_clicked(self):
        self.game.page = SelectMapPage(self.game, GameMode.MULTIPLAYER)

    # Direct connect button clicked
    def direct_connect_button_clicked(self):
        self.game.page = DirectConnectPage(self.game)

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = PlayPage(self.game)

# The direct connect page class
class DirectConnectPage(Page):
    # Create direct connect page
    def __init__(self, game):
        Page.__init__(self, game)

    # Create direct conect page widgets
    def create_widgets(self):
        y = (self.game.height - (72 + 24 + 48 + 24 + 64 + 32 + 64)) // 2
        self.widgets.append(Label(self.game, 'Direct Connect', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 24
        self.widgets.append(Label(self.game, 'Enter the IP address of the host', 0, y, self.game.width, 48, self.game.textFont, Color.WHITE))
        y += 48 + 24
        self.widgets.append(TextEdit(self.game, self.game.settings['multiplayer']['last-address'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, 'IP address...', Color.GRAY, 24, self.ip_address_text_edit_changed))
        y += 64 + 32
        self.widgets.append(Button(self.game, 'Back', self.game.width // 4, y, self.game.width // 4 - 8, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))
        self.widgets.append(Button(self.game, 'Connect', self.game.width // 2 + 16, y, self.game.width // 4 - 8, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.connect_button_clicked))

    # IP address text edit changed
    def ip_address_text_edit_changed(self, text):
        self.game.settings['multiplayer']['last-address'] = text

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = MultiplayerPage(self.game)

    # Connect button clicked
    def connect_button_clicked(self):
        pass

# The lobby page class
class LobbyPage(Page):
    # Create lobby page
    def __init__(self, game, gamemode, map):
        self.gamemode = gamemode
        self.map = map
        Page.__init__(self, game)

    # Create lobby page widgets
    def create_widgets(self):
        self.widgets.append(Label(self.game, 'Game Lobby', 0, 24, self.game.width, 72, self.game.titleFont, Color.WHITE))
        self.widgets.append(Button(self.game, 'Close', 16, self.game.height - 64 - 16, 240, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.close_button_clicked))
        self.widgets.append(Button(self.game, 'Race!', self.game.width - 16 - 240, self.game.height - 64 - 16, 240, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.race_button_clicked))

    # Close button clicked
    def close_button_clicked(self):
        self.game.page = MultiplayerPage(self.game)

    # Race button clicked
    def race_button_clicked(self):
        pass

# The select map page class
class SelectMapPage(Page):
    # Create select map page
    def __init__(self, game, gamemode):
        self.gamemode = gamemode
        Page.__init__(self, game)

    # Create select map page widgets
    def create_widgets(self):
        self.widgets.append(Label(self.game, 'Select a map to race', 0, 24, self.game.width, 72, self.game.titleFont, Color.WHITE))
        self.mapSelector = MapSelector(self.game, 16, 24 + 72 + 16, self.game.width - 16 - 16, self.game.height - (24 + 72 + 16) - (48 + 64 + 16), self.game.settings['selected']['map-id'], self.map_selector_changed)
        self.widgets.append(self.mapSelector)
        self.widgets.append(Button(self.game, 'Back', 16, self.game.height - 64 - 16, 240, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))
        self.widgets.append(Button(self.game, 'Load custom map', (self.game.width - 420) // 2, self.game.height - 64 - 16, 420, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.load_button_clicked))
        self.widgets.append(Button(self.game, 'Continue', self.game.width - 16 - 240, self.game.height - 64 - 16, 240, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.continue_button_clicked))

    # Map selector changed
    def map_selector_changed(self, selectedMap):
        self.game.settings['selected']['map-id'] = selectedMap.id

    # Back button clicked
    def back_button_clicked(self):
        if self.gamemode == GameMode.MULTIPLAYER:
            self.game.page = MultiplayerPage(self.game)
        else:
            self.game.page = PlayPage(self.game)

    # Load button clicked
    # def load_button_clicked(self):
    #     # file_path = tkinter.filedialog.askopenfilename(title='Select a BassieRacing Map to load...', filetypes=[ ( 'JSON files', '*.json' ) ])
    #     if file_path:
    #         self.game.focus()
    #         self.mapSelector.load_map(file_path)

    # Continue button clicked
    def continue_button_clicked(self):
        if self.gamemode == GameMode.MULTIPLAYER:
            self.game.page = LobbyPage(self.game, self.gamemode, self.mapSelector.selectedMap)
        else:
            self.game.page = SelectVehiclePage(self.game, self.gamemode, self.mapSelector.selectedMap)

# The select vehicle page class
class SelectVehiclePage(Page):
    # Create select vehicle page
    def __init__(self, game, gamemode, map):
        self.gamemode = gamemode
        self.map = map
        Page.__init__(self, game)

    # Create select vehicle page widgets
    def create_widgets(self):
        if self.gamemode == GameMode.SINGLE_PLAYER:
            self.widgets.append(Label(self.game, 'Select a vehicle', 0, 24, self.game.width, 72, self.game.titleFont, Color.WHITE))
            self.leftVehicleSelector = VehicleSelector(self.game, 16, 24 + 72 + 16, self.game.width - (16 + 16), self.game.height - (24 + 72 + 16) - (48 + 64 + 16), self.game.settings['selected']['left']['vehicle-id'], self.game.settings['selected']['left']['vehicle-color'], self.left_vehicle_selector_changed)
            self.widgets.append(self.leftVehicleSelector)

        if self.gamemode == GameMode.SPLIT_SCREEN:
            self.widgets.append(Label(self.game, 'Select both a vehicle', 0, 24, self.game.width, 72, self.game.titleFont, Color.WHITE))
            self.leftVehicleSelector = VehicleSelector(self.game, 16, 24 + 72 + 16, self.game.width // 2 - (16 + 16), self.game.height - (24 + 72 + 16) - (48 + 64 + 16), self.game.settings['selected']['left']['vehicle-id'], self.game.settings['selected']['left']['vehicle-color'], self.left_vehicle_selector_changed)
            self.widgets.append(self.leftVehicleSelector)
            self.rightVehicleSelector = VehicleSelector(self.game, 16 + self.game.width // 2, 24 + 72 + 16, self.game.width // 2 - (16 + 16), self.game.height - (24 + 72 + 16) - (48 + 64 + 16), self.game.settings['selected']['right']['vehicle-id'], self.game.settings['selected']['right']['vehicle-color'], self.right_vehicle_selector_changed)
            self.widgets.append(self.rightVehicleSelector)

        self.widgets.append(Button(self.game, 'Back', 16, self.game.height - 64 - 16, 240, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))
        self.widgets.append(Button(self.game, 'Race!', self.game.width - 16 - 240, self.game.height - 64 - 16, 240, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.race_button_clicked))

    # Left vehicle selector changed
    def left_vehicle_selector_changed(self, selectedVehicle, selectedVehicleColor):
        self.game.settings['selected']['left']['vehicle-id'] = selectedVehicle['id']
        self.game.settings['selected']['left']['vehicle-color'] = selectedVehicleColor

    # Right vehicle selector changed
    def right_vehicle_selector_changed(self, selectedVehicle, selectedVehicleColor):
        self.game.settings['selected']['right']['vehicle-id'] = selectedVehicle['id']
        self.game.settings['selected']['right']['vehicle-color'] = selectedVehicleColor

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = SelectMapPage(self.game, self.gamemode)

    # Race button clicked
    def race_button_clicked(self):
        
        if self.gamemode == GameMode.SINGLE_PLAYER:
            self.game.page = GamePage(self.game, self.gamemode, self.map, [
                {
                    'type': self.leftVehicleSelector.selectedVehicle,
                    'color': self.game.settings['selected']['left']['vehicle-color']
                }
            ])
        if self.gamemode == GameMode.SPLIT_SCREEN:
            self.game.page = GamePage(self.game, self.gamemode, self.map, [
                {
                    'type': self.leftVehicleSelector.selectedVehicle,
                    'color': self.game.settings['selected']['left']['vehicle-color']
                },
                {
                    'type': self.rightVehicleSelector.selectedVehicle,
                    'color': self.game.settings['selected']['right']['vehicle-color']
                }
            ])


# The game page class
class GamePage(Page):
    # Create game page
    def __init__(self, game, gamemode, map, vehicleData):
        self.gamemode = gamemode
        self.map = map

        # Create the vehicles
        self.vehicles = []

        # Check if finish is horizontal
        if map.finish['height'] > map.finish['width']:
            self.leftVehicle = Vehicle(game, VehicleId.LEFT, vehicleData[0]['type'], vehicleData[0]['color'], map, self.vehicles,
                (map.finish['x'] - 1) * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                (map.finish['y'] + map.finish['height'] // 2 - 1) * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                math.radians(270)
            )
            self.vehicles.append(self.leftVehicle)

            if gamemode == GameMode.SPLIT_SCREEN:
                self.rightVehicle = Vehicle(game, VehicleId.RIGHT, vehicleData[1]['type'], vehicleData[1]['color'], map, self.vehicles,
                    (map.finish['x'] - 1)  * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                    (map.finish['y'] + map.finish['height'] // 2)  * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                    math.radians(270)
                )
                self.vehicles.append(self.rightVehicle)

        # Or when the finish is vertical
        else:
            self.leftVehicle = Vehicle(game, VehicleId.LEFT, vehicleData[0]['type'], vehicleData[0]['color'], map, self.vehicles,
                (map.finish['x'] + map.finish['width'] // 2 - 1) * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                (map.finish['y'] + map.finish['height']) * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                0
            )
            self.vehicles.append(self.leftVehicle)

            if gamemode == GameMode.SPLIT_SCREEN:
                self.rightVehicle = Vehicle(game, VehicleId.RIGHT, vehicleData[1]['type'], vehicleData[1]['color'], map, self.vehicles,
                    (map.finish['x'] + map.finish['width'] // 2)  * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                    (map.finish['y'] + map.finish['height'])  * Config.TILE_SPRITE_SIZE + Config.TILE_SPRITE_SIZE / 2,
                    0
                )
                self.vehicles.append(self.rightVehicle)

        # Create page
        Page.__init__(self, game, Color.BLACK)

    # Create game page widgets
    def create_widgets(self):
        minimap_size = self.game.width / 5

        if self.gamemode == GameMode.SINGLE_PLAYER:
            self.leftVehicleViewport = VehicleViewport(self.game, self.gamemode, self.leftVehicle, 0, 0, self.game.width, self.game.height, self.map, self.vehicles)
            self.widgets.append(self.leftVehicleViewport)

            self.widgets.append(Rect(self.game, self.game.width - minimap_size - 12, self.game.height - minimap_size - 12, minimap_size + 4, minimap_size + 4, Color.BLACK))
            self.widgets.append(MiniMap(self.game, self.map, self.vehicles, self.game.width - minimap_size - 10, self.game.height - minimap_size - 10, minimap_size, minimap_size))

        if self.gamemode == GameMode.SPLIT_SCREEN:
            self.leftVehicleViewport = VehicleViewport(self.game, self.gamemode, self.leftVehicle, 0, 0, self.game.width // 2 - 1, self.game.height, self.map, self.vehicles)
            self.widgets.append(self.leftVehicleViewport)
            self.rightVehicleViewport = VehicleViewport(self.game, self.gamemode, self.rightVehicle, self.game.width // 2 + 1, 0, self.game.width // 2 - 1, self.game.height, self.map, self.vehicles)
            self.widgets.append(self.rightVehicleViewport)

            self.widgets.append(Rect(self.game, (self.game.width - minimap_size) // 2 - 2, 8, minimap_size + 4, minimap_size + 4, Color.BLACK))
            self.widgets.append(MiniMap(self.game, self.map, self.vehicles, (self.game.width - minimap_size) // 2, 10, minimap_size, minimap_size))

        self.widgets.append(Button(self.game, 'Back', self.game.width - 16 - 128, 16, 128, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = PlayPage(self.game)

    # Update game page
    def update(self, delta):
        # Update vehicle viewports
        self.leftVehicleViewport.update(delta)
        if self.gamemode == GameMode.SPLIT_SCREEN:
            self.rightVehicleViewport.update(delta)

        # When countdown is over start vehicle
        if not self.leftVehicle.started and self.leftVehicleViewport.countdownClock.ended:
            self.leftVehicle.started = True
            self.leftVehicle.startTime = self.game.time

        if self.gamemode == GameMode.SPLIT_SCREEN and not self.rightVehicle.started and self.rightVehicleViewport.countdownClock.ended:
            self.rightVehicle.started = True
            self.rightVehicle.startTime = self.game.time
        x = math.floor(self.leftVehicle.x / self.leftVehicleViewport.camera.tileSize)
        y = math.floor(self.leftVehicle.y / self.leftVehicleViewport.camera.tileSize)
        
        
        calcDist(self, x, y)
        # Update all the vehicles
        for vehicle in self.vehicles:
            if vehicle.id == VehicleId.LEFT:
                vehicle.update(delta, self.leftVehicleViewport.camera)
        #     if vehicle.id == VehicleId.RIGHT:
        #         vehicle.update(delta, self.rightVehicleViewport.camera)

        # When both vehicles are finished go to the stats page
        if self.gamemode == GameMode.SINGLE_PLAYER and self.leftVehicle.finished:
            self.game.page = StatsPage(self.game, self.gamemode, self.map, self.vehicles)
        if self.gamemode == GameMode.SPLIT_SCREEN and self.leftVehicle.finished and self.rightVehicle.finished:
            self.game.page = StatsPage(self.game, self.gamemode, self.map, self.vehicles)

def closestDirections(self, radians, directions):
    degrees = radians * (180 / 3.14159)  # Convert radians to degrees
    degrees %= 360  # Normalize degrees within [0, 360)
    cardinals = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = int((degrees + 22.5) / 45) % 8  # Determine which part of the circle you're in
    
    main_direction = cardinals[index]
    
    # Determine the 4 closest directions
    if main_direction == 'N':
        closest_directions = ['N', 'NE', 'NW', 'E', 'W']
        self.leftVehicle.f = directions[0]
        self.leftVehicle.fe = directions[1]
        self.leftVehicle.fw = directions[7]
        self.leftVehicle.fee = directions[2]
        self.leftVehicle.fww = directions[6]
    elif main_direction == 'NE':
        closest_directions = ['NE', 'E', 'N', 'SE', 'NW']
        self.leftVehicle.f = directions[1]
        self.leftVehicle.fe = directions[2]
        self.leftVehicle.fw = directions[0]
        self.leftVehicle.fee = directions[3]
        self.leftVehicle.fww = directions[7]
    elif main_direction == 'E':
        closest_directions = ['E', 'SE', 'NE', 'S', 'N']
        self.leftVehicle.f = directions[2]
        self.leftVehicle.fe = directions[3]
        self.leftVehicle.fw = directions[1]
        self.leftVehicle.fee = directions[4]
        self.leftVehicle.fww = directions[0]
    elif main_direction == 'SE':
        closest_directions = ['SE', 'S', 'E', 'SW', 'NE']
        self.leftVehicle.f = directions[3]
        self.leftVehicle.fe = directions[4]
        self.leftVehicle.fw = directions[2]
        self.leftVehicle.fee = directions[5]
        self.leftVehicle.fww = directions[1]
    elif main_direction == 'S':
        closest_directions = ['S', 'SW', 'SE', 'W', 'E']
        self.leftVehicle.f = directions[4]
        self.leftVehicle.fe = directions[5]
        self.leftVehicle.fw = directions[3]
        self.leftVehicle.fee = directions[6]
        self.leftVehicle.fww = directions[2]
    elif main_direction == 'SW':
        closest_directions = ['SW', 'W', 'S', 'NW', 'SE']
        self.leftVehicle.f = directions[5]
        self.leftVehicle.fe = directions[6]
        self.leftVehicle.fw = directions[4]
        self.leftVehicle.fee = directions[7]
        self.leftVehicle.fww = directions[3]
    elif main_direction == 'W':
        closest_directions = ['W', 'NW', 'SW', 'N', 'S']
        self.leftVehicle.f = directions[6]
        self.leftVehicle.fe = directions[7]
        self.leftVehicle.fw = directions[5]
        self.leftVehicle.fee = directions[0]
        self.leftVehicle.fww = directions[4]
    else:  # main_direction == 'NW'
        closest_directions = ['NW', 'N', 'W', 'NE', 'SW']
        self.leftVehicle.f = directions[7]
        self.leftVehicle.fe = directions[0]
        self.leftVehicle.fw = directions[6]
        self.leftVehicle.fee = directions[1]
        self.leftVehicle.fww = directions[5]
# The stats page class
def calcDist(self, x, y):
    xe = x
    xw = x
    xne = x
    xnw = x
    xse = x
    xsw = x
    
    yn = y
    ys = y
    yne = y
    ynw = y
    yse = y
    ysw = y
    
    z = self.map.track[y][x]
 
    yChange = self.leftVehicle.y - self.leftVehicle.oldY
    xChange = self.leftVehicle.x - self.leftVehicle.oldX
    # or (xChange == 0 and yChange == 0)
    if self.leftVehicle.crashed or self.leftVehicle.finished:
        self.game.genome.fitness = (self.leftVehicle.checkpoints - (((self.game.time - self.leftVehicle.startTime) / 6))) + (self.leftVehicle.lap * 10)
        # print(self.game.genome.fitness)
        self.game.running = False
        self.game.event = pygame.QUIT
        pygame.quit()
        # sys.exit()
        # self.game.page = PlayPage(self.game)
        # print(self.map.gens)
        self.map.gens += 1
    while ( z != 0):
        xe += 1
        z = self.map.track[y][xe]
        
    z = self.map.track[y][x]
    
    while ( z != 0):
        xw -= 1
        z = self.map.track[y][xw]
    
    z = self.map.track[y][x]
    
    while ( z != 0):
        yn += 1
        z = self.map.track[yn][x]
    
    z = self.map.track[y][x]
    
    while ( z != 0 ):
        ys -= 1
        z = self.map.track[ys][x]
    
    z = self.map.track[y][x]
    
    while ( z != 0 ):
        yne += 1
        xne += 1
        z = self.map.track[yne][xne]
        
    z = self.map.track[y][x]
    
    while ( z != 0 ):
        ynw += 1
        xnw -= 1
        z = self.map.track[ynw][xnw]
        
    z = self.map.track[y][x]
    
    while ( z != 0 ):
        yse -= 1
        xse += 1
        z = self.map.track[yse][xse]
        
    z = self.map.track[y][x]
    
    while ( z != 0 ):
        ysw -= 1
        xsw -= 1
        z = self.map.track[ysw][xsw]
    n = int(yn - y)
    ne = int(yne - y)
    e = int(xe - x)
    se = int(xse - x)
    s = int(y - ys)
    sw = int(y - ysw)
    w = int(x - xw)
    nw = int(ynw - y)
    directions = [n, ne, e, se, s, sw, w, nw]
    closest = closestDirections(self, self.leftVehicle.angle, directions)
    

    
class StatsPage(Page):
    # Create stats page
    def __init__(self, game, gamemode, map, vehicles):
        self.gamemode = gamemode
        self.map = map
        self.vehicles = vehicles

        # Calculate fastest time
        if gamemode == GameMode.SINGLE_PLAYER:
            fastestTime = vehicles[VehicleId.LEFT].finishTime - vehicles[VehicleId.LEFT].startTime
        if gamemode == GameMode.SPLIT_SCREEN:
            fastestTime = min(
                vehicles[VehicleId.LEFT].finishTime - vehicles[VehicleId.LEFT].startTime,
                vehicles[VehicleId.RIGHT].finishTime - vehicles[VehicleId.RIGHT].startTime
            )

        # Save high score
        highscoreExisted = False
        for score in game.settings['high-scores']:
            if score['map-id'] == map.id and score['time'] > fastestTime:
                score['time'] = round(fastestTime, 3)
                highscoreExisted = True
                break

        if not highscoreExisted:
            game.settings['high-scores'].append({
                'map-id': map.id,
                'time': round(fastestTime, 3)
            })

        Page.__init__(self, game)

    # Create stats page widgets
    def create_widgets(self):
        if self.map.laps > 3:
            lapLinesAmount = math.ceil(self.map.laps / 2)
        else:
            lapLinesAmount = self.map.laps

        y = (self.game.height - (72 + 16 + 128 + 16 + (48 + 16) * (2 + lapLinesAmount) + 16 + 64)) // 2
        self.widgets.append(Label(self.game, 'Game stats', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 16

        # Create stats for the single player gamemode
        if self.gamemode == GameMode.SINGLE_PLAYER:
            # Create vehicle image
            vehicleImageSurface = self.game.vehiclesImage.subsurface((
                self.vehicles[VehicleId.LEFT].vehicleType['colors'][self.vehicles[VehicleId.LEFT].color]['x'],
                self.vehicles[VehicleId.LEFT].vehicleType['colors'][self.vehicles[VehicleId.LEFT].color]['y'],
                self.vehicles[VehicleId.LEFT].vehicleType['width'],
                self.vehicles[VehicleId.LEFT].vehicleType['height']
            ))
            self.widgets.append(Image(self.game, vehicleImageSurface, self.game.width // 4, y, self.game.width // 2, 128))
            y += 128 + 16

            self.widgets.append(Label(self.game, 'You won!', self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
            y += 48 + 16

            self.widgets.append(Label(self.game, 'Total: %s' % (formatTime(self.vehicles[VehicleId.LEFT].finishTime - self.vehicles[VehicleId.LEFT].startTime)), self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
            y += 48 + 16

            if self.map.laps > 3:
                i = 0
                while i < self.map.laps:
                    text = 'Lap %d: %s' % (i + 1, formatTime(self.vehicles[VehicleId.LEFT].lapTimes[i]))

                    i += 1
                    if i != self.map.laps:
                        text += '  Lap %d: %s' % (i + 1, formatTime(self.vehicles[VehicleId.LEFT].lapTimes[i]))

                    self.widgets.append(Label(self.game, text, self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
                    y += 48 + 16

                    i += 1
            else:
                for i, time in enumerate(self.vehicles[VehicleId.LEFT].lapTimes):
                    self.widgets.append(Label(self.game, 'Lap %d: %s' % (i + 1, formatTime(time)), self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
                    y += 48 + 16
            y += 16

        # Create stats for the split screen gamemode
        if self.gamemode == GameMode.SPLIT_SCREEN:
            if self.vehicles[VehicleId.LEFT].finishTime - self.vehicles[VehicleId.LEFT].startTime < self.vehicles[VehicleId.RIGHT].finishTime - self.vehicles[VehicleId.RIGHT].startTime:
                # Create vehicle image
                vehicleImageSurface = self.game.vehiclesImage.subsurface((
                    self.vehicles[VehicleId.LEFT].vehicleType['colors'][self.vehicles[VehicleId.LEFT].color]['x'],
                    self.vehicles[VehicleId.LEFT].vehicleType['colors'][self.vehicles[VehicleId.LEFT].color]['y'],
                    self.vehicles[VehicleId.LEFT].vehicleType['width'],
                    self.vehicles[VehicleId.LEFT].vehicleType['height']
                ))
                self.widgets.append(Image(self.game, vehicleImageSurface, self.game.width // 4, y, self.game.width // 2, 128))
                y += 128 + 16

                self.widgets.append(Label(self.game, 'Left player wins!', self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
                y += 48 + 16
            else:
                # Create vehicle image
                vehicleImageSurface = self.game.vehiclesImage.subsurface((
                    self.vehicles[VehicleId.RIGHT].vehicleType['colors'][self.vehicles[VehicleId.RIGHT].color]['x'],
                    self.vehicles[VehicleId.RIGHT].vehicleType['colors'][self.vehicles[VehicleId.RIGHT].color]['y'],
                    self.vehicles[VehicleId.RIGHT].vehicleType['width'],
                    self.vehicles[VehicleId.RIGHT].vehicleType['height']
                ))
                self.widgets.append(Image(self.game, vehicleImageSurface, self.game.width // 4, y, self.game.width // 2, 128))
                y += 128 + 16

                self.widgets.append(Label(self.game, 'Right player wins!', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.WHITE))
                y += 64 + 16

            self.widgets.append(Label(self.game, 'Total: %s %s' % (formatTime(self.vehicles[VehicleId.LEFT].finishTime - self.vehicles[VehicleId.LEFT].startTime), formatTime(self.vehicles[VehicleId.RIGHT].finishTime - self.vehicles[VehicleId.RIGHT].startTime)), self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
            y += 48 + 16

            if self.map.laps > 3:
                i = 0
                while i < self.map.laps:
                    text = 'Lap %d: %s %s' % (i + 1, formatTime(self.vehicles[VehicleId.LEFT].lapTimes[i]), formatTime(self.vehicles[VehicleId.RIGHT].lapTimes[i]))

                    i += 1
                    if i != self.map.laps:
                        text += '  Lap %d: %s %s' % (i + 1, formatTime(self.vehicles[VehicleId.LEFT].lapTimes[i]), formatTime(self.vehicles[VehicleId.RIGHT].lapTimes[i]))

                    self.widgets.append(Label(self.game, text, self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
                    y += 48 + 16

                    i += 1
            else:
                for i, time in enumerate(self.vehicles[VehicleId.LEFT].lapTimes):
                    self.widgets.append(Label(self.game, 'Lap %d: %s %s' % (i + 1, formatTime(time), formatTime(self.vehicles[VehicleId.RIGHT].lapTimes[i])), self.game.width // 4, y, self.game.width // 2, 48, self.game.textFont, Color.WHITE))
                    y += 48 + 16
            y += 16

        self.widgets.append(Button(self.game, 'Continue', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.continue_button_clicked))

    # Continue button clicked
    def continue_button_clicked(self):
        self.game.page = PlayPage(self.game)

# The edit page class
class EditorPage(Page):
    # Create edit page
    def __init__(self, game, map = None):
        if map == None:
            loaded = False

            # Open last opend path
            if game.settings['map-editor']['last-path'] != None:
                if os.path.isfile(game.settings['map-editor']['last-path']):
                    self.map = Map.load_from_file(game.settings['map-editor']['last-path'])
                    if self.map != None:
                        loaded = True
                        pygame.display.set_caption(game.settings['map-editor']['last-path'] + ' - BassieRacing')
                    else:
                        game.settings['map-editor']['last-path'] = None
                else:
                    game.settings['map-editor']['last-path'] = None

            if not loaded:
                pygame.display.set_caption('Unsaved - BassieRacing')
                self.map = Map.generate_new(game)
        else:
            self.map = map

        self.mapCamera = { 'x': None, 'y': None }

        Page.__init__(self, game, Color.DARK)

    # Create edit page widgets
    def create_widgets(self):
        self.mapEditor = MapEditor(self.game, self.map, 0, 0, self.game.width, self.game.height, self.game.settings['map-editor']['brush'], self.game.settings['map-editor']['grid'], self.mapCamera)
        self.widgets.append(self.mapEditor)

        self.widgets.append(Button(self.game, 'New', 16, 16, 128, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.new_button_clicked))
        self.widgets.append(Button(self.game, 'Open', 16 + (128 + 16), 16, 128, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.open_button_clicked))
        self.widgets.append(Button(self.game, 'Save', 16 + (128 + 16) * 2, 16, 128, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.save_button_clicked))
        self.widgets.append(ToggleButton(self.game, [ 'Grid off', 'Grid on' ], self.game.settings['map-editor']['grid'], 16 + (128 + 16) * 3 + 16, 16, 256, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.grid_togglebutton_changed))
        self.widgets.append(Button(self.game, 'Back', self.game.width - (16 + 128), 16, 128, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

        self.widgets.append(Button(self.game, 'Map Options', 16, self.game.height - 64 - 16, (self.game.width - 16 * 4) // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.map_options_button_clicked))
        self.brushComboBox = ComboBox(self.game, self, MapEditor.TOOL_LABELS, self.game.settings['map-editor']['brush'], 16 + ((self.game.width - 16 * 4) // 2) + 16, self.game.height - 64 - 16, (self.game.width - 16 * 2) // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.brush_combo_box_changed)
        self.widgets.append(self.brushComboBox)

    # Handle map editor page events
    def handle_event(self, event):
        if Page.handle_event(self, event):
            return True

        # Handle key up events
        if event.type == pygame.KEYUP:
            if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_n:
                self.new_button_clicked()
            if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_o:
                self.open_button_clicked()
            if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_s:
                self.save_button_clicked()

        return False

    # Update map editor widget
    def update(self, delta):
        self.mapEditor.update(delta)
        self.mapCamera['x'] = self.mapEditor.camera.x
        self.mapCamera['y'] = self.mapEditor.camera.y

    # New button clicked
    def new_button_clicked(self):
        self.game.settings['map-editor']['last-path'] = None

        pygame.display.set_caption('Unsaved - BassieRacing')

        self.map = Map.generate_new(self.game)
        self.mapEditor.map = self.map
        self.mapEditor.center_camera()

    # Open button clicked
    # def open_button_clicked(self):
    #     # file_path = tkinter.filedialog.askopenfilename(title='Select a BassieRacing Map to open...', filetypes=[ ( 'JSON files', '*.json' ) ])
    #     if file_path:
    #         self.game.settings['map-editor']['last-path'] = file_path

    #         pygame.display.set_caption(file_path + ' - BassieRacing')
    #         self.game.focus()

    #         self.map = Map.load_from_file(file_path)
    #         if self.map != None:
    #             self.mapEditor.map = self.map
    #             self.mapEditor.center_camera()

    # Save button clicked
    # def save_button_clicked(self):
    #     if self.game.settings['map-editor']['last-path'] == None:
    #         file_path = tkinter.filedialog.asksaveasfilename(title='Select a location to save the BassieRacing Map...', filetypes=[ ( 'JSON files', '*.json' ) ], defaultextension='.json')
    #         if file_path:
    #             self.game.settings['map-editor']['last-path'] = file_path

    #             pygame.display.set_caption(file_path + ' - BassieRacing')
    #             self.game.focus()

    #             self.map.blend_track(True)

    #     if self.game.settings['map-editor']['last-path'] != None:
    #         self.map.save_to_file(self.game.settings['map-editor']['last-path'])

    # Grid toggle button changed
    def grid_togglebutton_changed(self, active):
        self.game.settings['map-editor']['grid'] = active
        self.mapEditor.grid = active
        self.mapEditor.camera.grid = active

    # Back button clicked
    def back_button_clicked(self):
        pygame.display.set_caption('BassieRacing')
        self.game.page = MenuPage(self.game)

    # Map options button clicked
    def map_options_button_clicked(self):
        self.game.page = MapOptionsPage(self.game, self.map)

    # Brush combo box changed
    def brush_combo_box_changed(self, selectedOptionIndex):
        self.game.settings['map-editor']['brush'] = selectedOptionIndex
        self.mapEditor.tool = selectedOptionIndex

# The map options page class
class MapOptionsPage(Page):
    # Create map options page
    def __init__(self, game, map):
        self.map = map

        # Save map options to the settings

        # Select map name
        game.settings['map-options']['name'] = map.name

        # Select the right size amount
        foundSize = False
        for i, size in enumerate(Config.MAP_SIZES):
            if size == map.width:
                foundSize = True
                game.settings['map-options']['size'] = i
                break

        if not foundSize:
            game.settings['map-options']['size'] = len(Config.MAP_SIZES)

        # Select the right laps amount
        foundLaps = False
        for i, laps in enumerate(Config.MAP_LAPS):
            if laps == map.laps:
                foundLaps = True
                game.settings['map-options']['laps'] = i
                break

        if not foundLaps:
            game.settings['map-options']['laps'] = len(Config.MAP_LAPS)

        # Select crash enabled
        game.settings['map-options']['crashes']['enabled'] = map.crashes['enabled']

        # Select the right crash timeout amount
        foundCrashTimeout = False
        for i, crashTimeout in enumerate(Config.MAP_CRASH_TIMEOUTS):
            if crashTimeout == map.crashes['timeout']:
                foundCrashTimeout = True
                game.settings['map-options']['crashes']['timeout'] = i
                break

        if not foundCrashTimeout:
            game.settings['map-options']['crashes']['timeout'] = len(Config.MAP_CRASH_TIMEOUTS)

        Page.__init__(self, game)

    # Create map options page widgets
    def create_widgets(self):
        y = (self.game.height - (72 + 24 + (64 + 16) * 5 + 8 * 2 + 64)) // 2
        self.widgets.append(Label(self.game, 'Map Options', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 24

        self.widgets.append(TextEdit(self.game, self.game.settings['map-options']['name'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, 'Map name...', Color.GRAY, 24, self.name_text_edit_changed))
        y += 64 + 16

        self.sizeComboBox = ComboBox(self.game, self, [ '%s (%dx%d)' % (Config.MAP_SIZE_LABELS[i], size, size) for i, size in enumerate(Config.MAP_SIZES) ],
            0 if self.game.settings['map-options']['size'] == len(Config.MAP_SIZES) else self.game.settings['map-options']['size'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.size_combo_box_changed)
        if self.game.settings['map-options']['size'] == len(Config.MAP_SIZES):
            self.sizeComboBox.set_text('Custom (%dx%d) \u25BC' % (self.map.width, self.map.height))
        self.widgets.append(self.sizeComboBox)
        y += 64 + 16

        self.lapsComboBox = ComboBox(self.game, self, [ 'Laps: %d' % (laps) for laps in Config.MAP_LAPS ], self.game.settings['map-options']['laps'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.laps_combo_box_changed)
        if self.game.settings['map-options']['laps'] == len(Config.MAP_LAPS):
            self.lapsComboBox.set_text('Laps: %d \u25BC' % (self.map.laps))
        self.widgets.append(self.lapsComboBox)
        y += 64 + 24

        self.widgets.append(ToggleButton(self.game, [ 'Crashes disabled', 'Crashes enabled' ], self.game.settings['map-options']['crashes']['enabled'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.crashes_enabled_toggle_button_changed))
        y += 64 + 16

        self.crashesTimeoutComboBox = ComboBox(self.game, self, [ 'Crash timeout: %.1f s' % (crashTimeout) for crashTimeout in Config.MAP_CRASH_TIMEOUTS ], self.game.settings['map-options']['crashes']['timeout'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.crashes_timeout_combo_box_changed)
        if self.game.settings['map-options']['crashes']['timeout'] == len(Config.MAP_CRASH_TIMEOUTS):
            self.crashesTimeoutComboBox.set_text('Crash timeout: %.1f s \u25BC' % (self.map.crashes['timeout']))
        self.widgets.append(self.crashesTimeoutComboBox)
        y += 64 + 24

        self.widgets.append(Button(self.game, 'Back', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

    # Name text edit changed
    def name_text_edit_changed(self, text):
        self.game.settings['map-options']['name'] = text
        self.map.name = text

    # Size combo box changed
    def size_combo_box_changed(self, selectedOptionIndex):
        self.game.settings['map-options']['size'] = selectedOptionIndex

    # Laps combo box changed
    def laps_combo_box_changed(self, selectedOptionIndex):
        self.game.settings['map-options']['laps'] = selectedOptionIndex
        self.map.laps = Config.MAP_LAPS[selectedOptionIndex]

    # Crashes enabled toggle button changed
    def crashes_enabled_toggle_button_changed(self, active):
        self.game.settings['map-options']['crashes']['enabled'] = active
        self.map.crashes['enabled'] = active

    # Crashes timeout combo box changed
    def crashes_timeout_combo_box_changed(self, selectedOptionIndex):
        self.game.settings['map-options']['crashes']['timeout'] = selectedOptionIndex
        self.map.crashes['timeout'] = Config.MAP_CRASH_TIMEOUTS[selectedOptionIndex]

    # Back button clicked
    def back_button_clicked(self):
        if self.game.settings['map-options']['size'] != len(Config.MAP_SIZES):
            self.map.resize(Config.MAP_SIZES[self.game.settings['map-options']['size']], Config.MAP_SIZES[self.game.settings['map-options']['size']])
        self.game.page = EditorPage(self.game, self.map)

# The help page class
class HelpPage(Page):
    # Create help page
    def __init__(self, game):
        Page.__init__(self, game)

    # Create help page widgets
    def create_widgets(self):
        y = (self.game.height - (72 + (64 + 16) * 5 + 64 + 32)) // 2
        self.widgets.append(Label(self.game, 'Help', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 16
        self.widgets.append(Label(self.game, 'BassieRacing is a topdown 2D two player racing game', 0, y, self.game.width, 64, self.game.textFont, Color.WHITE))
        y += 64 + 16
        self.widgets.append(Label(self.game, 'You can control the main/left car by using WASD keys', 0, y, self.game.width, 64, self.game.textFont, Color.WHITE))
        y += 64 + 16
        self.widgets.append(Label(self.game, 'You can control the right car by using the arrow keys', 0, y, self.game.width, 64, self.game.textFont, Color.WHITE))
        y += 64 + 16
        self.widgets.append(Label(self.game, 'There are multiple maps and vehicles that you can try', 0, y, self.game.width, 64, self.game.textFont, Color.WHITE))
        y += 64 + 16
        self.widgets.append(Label(self.game, 'You can also create or edit custom maps', 0, y, self.game.width, 64, self.game.textFont, Color.WHITE))
        y += 64 + 32
        self.widgets.append(Button(self.game, 'Back', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = MenuPage(self.game)

# The settings page class
class SettingsPage(Page):
    # Create settings page
    def __init__(self, game):
        Page.__init__(self, game)

    # Create settings page widgets
    def create_widgets(self):
        y = (self.game.height - (72 + (64 + 16) * 6 + 8 * 2 + 24 + 64)) // 2
        self.widgets.append(Label(self.game, 'Settings', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 16
        self.widgets.append(TextEdit(self.game, self.game.settings['account']['username'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, 'Username...', Color.GRAY, 24, self.username_text_edit_changed))
        y += 64 + 24
        self.widgets.append(ToggleButton(self.game, [ 'Intro disabled', 'Intro enabled' ], self.game.settings['intro']['enabled'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.intro_toggle_button_changed))
        y += 64 + 16
        self.widgets.append(ToggleButton(self.game, [ 'Fancy music disabled', 'Fancy music enabled' ], self.game.settings['music']['enabled'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.music_toggle_button_changed))
        y += 64 + 16
        self.widgets.append(ToggleButton(self.game, [ 'Sound effects disabled', 'Sound effects enabled' ], self.game.settings['sound-effects']['enabled'], self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, Color.LIGHT_GRAY, self.sound_effects_toggle_button_changed))
        y += 64 + 24
        self.widgets.append(Button(self.game, 'Resest high scores', self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.reset_high_scores_button_clicked))
        y += 64 + 16
        self.widgets.append(Button(self.game, 'Clear custom maps cache', self.game.width // 6, y, self.game.width // 3 * 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.clear_custom_maps_cache_button_clicked))
        y += 64 + 24
        self.widgets.append(Button(self.game, 'Back', self.game.width // 4, y, self.game.width // 2, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.back_button_clicked))

    # Username text edit changed
    def username_text_edit_changed(self, text):
        self.game.settings['account']['username'] = text

    # Intro toggle button changed
    def intro_toggle_button_changed(self, active):
        self.game.settings['intro']['enabled'] = active

    # Music toggle button changed
    def music_toggle_button_changed(self, active):
        self.game.settings['music']['enabled'] = active

        if active:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(0, self.game.settings['music']['position'])
            else:
                pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    # Sound effects toggle button changed
    def sound_effects_toggle_button_changed(self, active):
        self.game.settings['sound-effects']['enabled'] = active

    # Reset high scores button clicked
    def reset_high_scores_button_clicked(self):
        self.game.settings['high-scores'] = []

    # Clear custom maps cache button clicked
    def clear_custom_maps_cache_button_clicked(self):
        self.game.settings['custom-maps'] = []

    # Back button clicked
    def back_button_clicked(self):
        self.game.page = MenuPage(self.game)

# The exit page class
class ExitPage(Page):
    # Create exit page
    def __init__(self, game):
        Page.__init__(self, game)

    # Create exit page widgets
    def create_widgets(self):
        y = (self.game.height - (72 + 24 + 32 + 8 + 32 + 32 + 64)) // 2
        self.widgets.append(Label(self.game, 'Are you sure to exit?', 0, y, self.game.width, 72, self.game.titleFont, Color.WHITE))
        y += 72 + 24
        self.widgets.append(Label(self.game, 'All your settings and high scores', 0, y, self.game.width, 32, self.game.textFont, Color.WHITE))
        y += 32 + 8
        self.widgets.append(Label(self.game, 'will be saved when you exit', 0, y, self.game.width, 32, self.game.textFont, Color.WHITE))
        y += 32 + 32
        self.widgets.append(Button(self.game, 'Yes', self.game.width // 4, y, self.game.width // 4 - 8, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.yes_button_clicked))
        self.widgets.append(Button(self.game, 'No', self.game.width // 2 + 16, y, self.game.width // 4 - 8, 64, self.game.textFont, Color.BLACK, Color.WHITE, self.no_button_clicked))

    # Yes button clicked
    def yes_button_clicked(self):
        self.game.save_settings()
        self.game.running = False

    # No button clicked
    def no_button_clicked(self):
        self.game.page = MenuPage(self.game)
