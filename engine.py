import pygame 
import os
import sys
from setting import *
from sprites import PlayerCar, EnemyCar, Coin, FloatingText

class GameEngine :
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("2D Car Racing Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "Menu"
        self.menu_options = ["Start Race", "Settings", "Quit"]
        self.menu_index = 0
        self.settings_options = ["Music: ", "Theme: ", "Back"]
        self.settings_index = 0
        self.music_on = True
        self.theme_colors = [GREEN, CYAN, MAGENTA, ORANGE] 
        self.theme_names = ["GREEN", "CYAN", "MAGENTA", "ORANGE"]
        self.current_theme = 0

        self.race_active = False

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30, bold=True)        
        self.large_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
        self.SPAWN_COIN_EVENT = pygame.USEREVENT + 2

        self.player_car_paths = [
            "assets/images/car1.png",
            "assets/images/car2.png",
            "assets/images/car3.png"
        ]
        self.selected_car_index = 0

        self.high_score = 0
        self.load_high_score()

        try:
            self.crash_sound = pygame.mixer.Sound("assets/sounds/crash.mp3")
            pygame.mixer.music.load("assets/sounds/music.mp3")
            self.engine_start_sound = pygame.mixer.Sound("assets/sounds/engine_start.mp3")
            self.engine_run_sound = pygame.mixer.Sound("assets/sounds/engine_run.mp3")
            self.coin_sound = pygame.mixer.Sound("assets/sounds/coin.mp3")
            self.coin_sound.set_volume(1.0)

            self.engine_channel = pygame.mixer.Channel(1)

            self.crash_sound.set_volume(1.0)
            pygame.mixer.music.set_volume(0.4)
            self.engine_start_sound.set_volume(0.8)
        except:
            print("Audio files missing! Check names and folder.")
            self.crash_sound = None
            self.engine_start_sound = None
            self.engine_run_sound = None
            self.engine_channel = None

        self.reset_game()

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as file:
                try:
                    self.high_score = int(file.read())
                except:
                    self.high_score = 0

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def reset_game(self):
        """NEW: Resets all variable to start a new game."""
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        selected_car_index = self.player_car_paths[self.selected_car_index]
        self.player = PlayerCar(selected_car_index)
        self.all_sprites.add(self.player)
        self.score = 0
        self.coins_collected = 0
        self.bg_y = 0
        self.game_over = False
        self.race_active = False
        self.ai_mode = False

        self.current_enemy_speed = OBSTACLE_SPEED
        self.spawn_time = 1500
        pygame.time.set_timer(self.SPAWN_ENEMY_EVENT, self.spawn_time)
        pygame.time.set_timer(self.SPAWN_COIN_EVENT, 2500)

        self.level = 1             
        self.level_up_timer = 0

        if hasattr(self, 'engine_channel') and self.engine_channel:
            self.engine_channel.stop()

    def run(self):
        """The main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Process keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

                # Menu Logic
                if self.state == "Menu":
                    if event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_options) 
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.menu_index == 0:
                            self.state = "Garage"
                        elif self.menu_index == 1:
                            self.state = "Settings"
                        elif self.menu_index == 2:
                            self.running = False

                # Settings Logic
                elif self.state == "Settings":
                    if event.key == pygame.K_UP:
                        self.settings_index = (self.settings_index - 1) % len(self.settings_options) 
                    elif event.key == pygame.K_DOWN:
                        self.settings_index = (self.settings_index + 1) % len(self.settings_options)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_RETURN:
                        if self.settings_index == 0:
                            self.music_on = not self.music_on
                        elif self.settings_index == 1:
                            if event.key == pygame.K_LEFT:
                                self.current_theme = (self.current_theme - 1) % len(self.theme_colors)
                            else:
                                self.current_theme = (self.current_theme + 1) % len(self.theme_colors)
                        elif self.settings_index == 2 and event.key == pygame.K_RETURN:
                            self.state = "Menu"

                # Garage Logic
                elif self.state == "Garage":
                    if event.key == pygame.K_LEFT:
                        self.selected_car_index = (self.selected_car_index - 1) % len(self.player_car_paths) 
                    elif event.key == pygame.K_RIGHT:
                        self.selected_car_index = (self.selected_car_index + 1) % len(self.player_car_paths)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "Menu"
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = "Playing"
                        try:
                            if self.engine_start_sound and self.music_on:
                                self.engine_start_sound.play()
                            if self.engine_channel and self.engine_run_sound and self.music_on:
                                self.engine_channel.play(self.engine_run_sound, loops=-1)
                                self.engine_channel.set_volume(0.2)
                        except:
                            pass

                # Playing Logic
                elif self.state == "Playing":
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = "Paused"
                        try:
                            pygame.mixer.music.pause()
                            if self.engine_channel: 
                                self.engine_channel.pause()
                        except:
                            pass
                    elif event.key == pygame.K_a:
                        self.ai_mode = not self.ai_mode

                # Paused Logic
                elif self.state == "Paused":
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = "Playing"
                        try:
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            if self.engine_channel and self.music_on:
                                self.engine_channel.unpause()
                        except:
                            pass
                    elif event.key == pygame.K_p:
                        self.state = "Menu"
                        try:
                            pygame.mixer.music.stop()
                            if self.engine_channel:
                                self.engine_channel.stop()
                        except:
                            pass

                # Game Over Logic
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.state = "Garage"
                    elif event.key == pygame.K_q:
                        self.state = "Menu"

            # Spawning
            if self.state == "Playing" and self.race_active:
                if event.type == self.SPAWN_ENEMY_EVENT:
                    enemy = EnemyCar(self.current_enemy_speed)
                    self.all_sprites.add(enemy)
                    self.obstacles.add(enemy)
                elif event.type == self.SPAWN_COIN_EVENT:
                    coin = Coin(self.current_enemy_speed) 
                    self.all_sprites.add(coin)
                    self.coins.add(coin)

    def update(self):
        """Update game state and data structure (To be implemented)."""
        if self.state != "Playing":
            return
        
        keys = pygame.key.get_pressed()
        if self.ai_mode:
            if not self.race_active:
                self.race_active = True
                try:
                    if self.music_on:
                        pygame.mixer.music.play(-1)
                except:
                    pass
            if hasattr(self, 'engine_channel') and self.engine_channel and self.music_on:
                self.engine_channel.set_volume(1.0)
            target_x = SCREEN_WIDTH // 2
            danger = False

            # Dodge Enemy
            for obs in self.obstacles:
                if obs.rect.bottom < self.player.rect.top + 150 and obs.rect.top > -50:
                    if abs(obs.rect.centerx - self.player.rect.centerx) < 80:
                        danger = True
                        if obs.rect.centerx >  self.player.rect.centerx:
                            target_x = self.player.rect.x - 120
                        else:
                            target_x = self.player.rect.x + 120
                        break
            # Chase Coins
            if not danger:
                closest_coin = None
                min_dist = 1000
                for c in self.coins:
                    if c.rect.bottom < self.player.rect.bottom:
                        dist = self.player.rect.top - c.rect.bottom
                        if 0 < dist < min_dist:
                            min_dist = dist
                            closest_coin = c
                if closest_coin:
                    target_x = closest_coin.rect.centerx
            # Apply Smooth Movement
            if self.player.rect.centerx < target_x and self.player.rect.right < SCREEN_WIDTH - 150:
                self.player.rect.x += PLAYER_SPEED
            elif self.player.rect.centerx > target_x and self.player.rect.left > 150:
                self.player.rect.x -= PLAYER_SPEED

        else:
            if hasattr(self, 'engine_channel') and self.engine_channel:
                if keys[pygame.K_UP]:
                    if not self.race_active:
                        self.race_active = True
                        try:
                            pygame.mixer.music.play(-1)
                        except:
                            pass
                    self.engine_channel.set_volume(1.0)
                elif keys[pygame.K_DOWN]:
                    self.engine_channel.set_volume(0.1)
                else:
                    self.engine_channel.set_volume(0.4)

        if self.race_active:
            self.all_sprites.update()
            self.score += 1

            if self.score > 0 and self.score % 400 == 0:
                self.current_enemy_speed += 2
                self.level += 1
                self.level_up_timer = 60
                if self.spawn_time > 500:
                    self.spawn_time -= 200
                    pygame.time.set_timer(self.SPAWN_ENEMY_EVENT, self.spawn_time)

            self.bg_y += self.current_enemy_speed

            if self.bg_y >= 100:
                self.bg_y = 0

            coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True, pygame.sprite.collide_mask)
            for coin in coin_hits:
                self.score += 50
                self.coins_collected += 1
                floating_text = FloatingText("+50", coin.rect.centerx, coin.rect.centery)
                self.all_sprites.add(floating_text)
                if hasattr(self, 'coin_sound') and self.coin_sound and self.music_on:
                    self.coin_sound.play()


            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask)
            if hits or (self.player.rect.left < 150 or self.player.rect.right > SCREEN_WIDTH - 80):
                self.state = "GAME_OVER"

                pygame.mixer.music.stop()
                if self.engine_channel:
                    self.engine_channel.stop()
                if self.crash_sound:
                    self.crash_sound.play()

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()


    def draw(self):
        """Render grapics to the screen."""
        theme_color = self.theme_colors[self.current_theme]

        # Menu Screen Logic
        if self.state == "Menu":
            self.screen.fill(BLACK) 
            title = self.title_font.render("RETRO RACER", True, theme_color)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            for i, option in enumerate(self.menu_options):
                color = WHITE if i != self.menu_index else theme_color
                text = self.large_font.render(option, True, color)
                if i == self.menu_index:
                    text = self.large_font.render(f"> {option} <", True, color)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 80))

        # Setting Screen Logic
        elif self.state == "Settings":
            self.screen.fill(BLACK) 
            title = self.large_font.render("Settings", True, theme_color)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            opts = [
                f"Music: {'ON' if self.music_on else 'OFF'}",
                f"Theme: {self.theme_names[self.current_theme]}",
                "Back"
            ]
            for i, option in enumerate(opts):
                color = WHITE if i != self.settings_index else theme_color
                text = self.font.render(option,True, color)
                if i == self.settings_index:
                    text = self.font.render(f"> {option} <", True, color)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

            hint = self.font.render(f"Use Left/Right Arrow to change", True, GRAY)
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 500))

        # Garage Screen Logic
        elif self.state == "Garage":
            self.screen.fill(BLACK) 
            title = self.large_font.render("Select Your Car", True, theme_color)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            hs_text = self.font.render(f"High Score: {self.high_score}", True, YELLOW)
            self.screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 200))
            try:
                car_img = pygame.image.load(self.player_car_paths[self.selected_car_index]).convert_alpha()
                car_img = pygame.transform.scale(car_img, (100, 160)) 
                self.screen.blit(car_img, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
            except:
                pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 160))
            
            nav_text = self.font.render("<-- Use LEFT / RIGHT Arrows -->", True, WHITE)
            start_text = self.font.render("Press SPACE to Start Race", True, RED)
            esc_text = self.font.render("Press ESC to go back", True, RED)
            
            self.screen.blit(nav_text, (SCREEN_WIDTH // 2 - nav_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))
            self.screen.blit(esc_text, (SCREEN_WIDTH // 2 - esc_text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))

        # Playing, Paused & Game Over Screen Logic
        else:
            is_night = (self.level % 2 == 0) 
            road_color = (40, 40, 40) if is_night else GRAY 
            side_color = (17, 70, 15) if is_night else (34, 139, 34) 
            line_color = (255, 255, 0) if is_night else WHITE
            
            self.screen.fill(road_color)
            grass_width = 150
            pygame.draw.rect(self.screen, side_color, (0, 0, grass_width, SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, side_color, (SCREEN_WIDTH - grass_width, 0, grass_width, SCREEN_HEIGHT))

            for y in range(-100, SCREEN_HEIGHT, 100):
                pygame.draw.rect(self.screen, line_color, (SCREEN_WIDTH // 2 - 5, y + self.bg_y, 10, 50))

            self.all_sprites.draw(self.screen)

            pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, 40))
            hud_font = pygame.font.SysFont("Arial", 22, bold=True)

            score_text = hud_font.render(f"Score: {self.score}", True, WHITE)
            level_text = hud_font.render(f"Level: {self.level}", True, GREEN)
            high_score_text = hud_font.render(f"Best: {max(self.score, self.high_score)}", True, YELLOW)
            coin_text = hud_font.render(f"Coins: {self.coins_collected}", True, (255, 215, 0))

            self.screen.blit(score_text, (20, 8))
            self.screen.blit(level_text, (220, 8))
            self.screen.blit(high_score_text, (620, 8))
            self.screen.blit(coin_text, (420, 8))

            if self.state == "Playing" and not self.race_active :
                ready_text = self.font.render("Press UP Arrow to Go!", True, YELLOW)
                pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH // 2 - 165, SCREEN_HEIGHT // 2 - 5, 330, 45))
                self.screen.blit(ready_text, (SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2))

            # AI Mode Indicator
            if self.state == "Playing" and self.ai_mode:
                ai_text = self.font.render("AI AUTO-PILOT ON", True, (0, 255, 255))
                pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH // 2 - ai_text.get_width()//2 - 10, 55, ai_text.get_width() + 20, 40))
                self.screen.blit(ai_text, (SCREEN_WIDTH // 2 - ai_text.get_width() // 2, 60))
                
            if self.level_up_timer > 0:
                lvl_up_text = self.large_font.render("LEVEL UP!", True, GREEN)
                self.screen.blit(lvl_up_text, (SCREEN_WIDTH // 2 - lvl_up_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                self.level_up_timer -= 1

            # Pause Overlay logic
            if self.state == "Paused":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))

                pause_text = self.title_font.render("Paused", True, theme_color)
                resume_text = self.font.render("Press 'P' to Resume", True, WHITE)
                quit_text = self.font.render("Press 'Q' to Quit to Menu", True, RED)

                self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width()//2, SCREEN_HEIGHT // 2 - 100))
                self.screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width()//2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width()//2, SCREEN_HEIGHT // 2 + 70))

            # Game Over Overlay
            elif self.state == "GAME_OVER":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))

                game_over_text = self.title_font.render("GAME OVER", True, RED)
                restart_text = self.font.render("Press 'R' to Restart", True, WHITE)
                quit_text = self.font.render("Press 'Q' to Quit to Menu", True, GRAY)
                
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width()//2, SCREEN_HEIGHT // 2 - 100))
                self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width()//2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width()//2, SCREEN_HEIGHT // 2 + 70))

        pygame.display.flip()