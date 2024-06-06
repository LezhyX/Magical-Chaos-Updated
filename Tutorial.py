import pygame
import random
import sys
import math
from Button import MenuButton

bullets = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
mobs = pygame.sprite.Group()
elites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
boss_sprite = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        width = spawn_x
        height = spawn_y
        self.hp = 24
        self.speed = 5
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load('assets/bat.png')
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.frame = 0
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()
        self.points = [[width / 4, height / 6], [width * (3 / 4), height / 6],
                       [width / 4, height / 2], [width * (3 / 4), height / 2]]
        self.rect.x, self.rect.y = random.choice(self.points)

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (50, 50))
        return image

    def update(self, width, height):
        if self.rect.x <= width * (3 / 4) and self.rect.y <= height / 6:
            self.rect.x += self.speed
        if self.rect.x >= width * (3 / 4) and self.rect.y <= height / 2:
            self.rect.y += self.speed
        if self.rect.x >= width / 4 and self.rect.y >= height / 2:
            self.rect.x -= self.speed
        if self.rect.x <= width / 4 and self.rect.y >= height / 6:
            self.rect.y -= self.speed
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame = (self.frame + 1) % 4
            self.image = self.get_image(self.frame * 32, 0, 32, 32)
        self.image.set_colorkey((0, 0, 0))

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def shoot(self, player_position):
        dx = player_position[0] - self.rect.centerx
        dy = player_position[1] - self.rect.centery
        angle_to_player = math.atan2(dy, dx)
        projectile_center = Projectile(self.rect.centerx, self.rect.bottom, int(math.degrees(angle_to_player)))
        projectile_left = Projectile(self.rect.centerx, self.rect.bottom,
                                     int(math.degrees(angle_to_player + math.pi / 8)))
        projectile_right = Projectile(self.rect.centerx, self.rect.bottom,
                                      int(math.degrees(angle_to_player - math.pi / 8)))
        projectiles.add(projectile_center, projectile_left, projectile_right)


class Elite(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, spawn_type):
        self.spawn_type = spawn_type
        width = spawn_x
        height = spawn_y
        self.hp = 48
        self.speed = 10
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load('assets/bat.png')
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.frame = 0
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()
        self.spawn_points = [[width + 200, height / 8], [0 - 200, height / 8]]
        if spawn_type == 0:
            self.rect.x, self.rect.y = width + 200, height / 8
        else:
            self.rect.x, self.rect.y = -200, height / 8

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (100, 100))
        return image

    def update(self, width, height):
        if self.spawn_type == 0:
            if self.rect.x > width * (3 / 4):
                self.rect.x -= self.speed
        else:
            if self.rect.x < width / 4:
                self.rect.x += self.speed
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame = (self.frame + 1) % 4
            self.image = self.get_image(self.frame * 32, 0, 32, 32)
        self.image.set_colorkey((0, 0, 0))

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def shoot(self, player_position):
        dx = player_position[0] - self.rect.centerx
        dy = player_position[1] - self.rect.centery
        angle_to_player = math.atan2(dy, dx)
        projectile = Projectile(self.rect.centerx, self.rect.bottom, int(math.degrees(angle_to_player)))
        projectile_left = Projectile(self.rect.left, self.rect.bottom, int(math.degrees(angle_to_player)))
        projectile_right = Projectile(self.rect.right, self.rect.bottom, int(math.degrees(angle_to_player)))
        projectile_top = Projectile(self.rect.centerx, self.rect.top, int(math.degrees(angle_to_player)))
        projectile_topleft = Projectile(self.rect.left, self.rect.top, int(math.degrees(angle_to_player)))
        projectile_topright = Projectile(self.rect.right, self.rect.top, int(math.degrees(angle_to_player)))
        projectiles.add(projectile, projectile_right, projectile_left, projectile_topleft, projectile_top,
                        projectile_topright)


class Boss(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        width = spawn_x
        height = spawn_y
        self.hp = 2000
        self.speed = 20
        self.state = 0
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load('assets/boss2.png').convert()
        self.image = pygame.transform.scale(self.spritesheet, (300, 150))
        self.rect = self.image.get_rect()
        self.frame = 0
        self.animation_speed = 50
        self.last_update = pygame.time.get_ticks()
        self.rect.x = width / 4 - 300
        self.rect.y = height / 5

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (300, 150))
        return image

    def update(self, width, height):
        if self.rect.x <= width * (3 / 4) and self.state == 0:
            self.rect.x += self.speed
        if self.rect.x >= width / 4 - 150 and self.state == 1:
            self.rect.x -= self.speed
        if self.rect.x >= width * (3 / 4):
            self.state = 1
        if self.rect.x <= width / 4 - 150:
            self.state = 0
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame = (self.frame + 1) % 11
            self.image = self.get_image(self.frame * 200, 0, 200, 134)
        self.image.set_colorkey((255, 255, 255))

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def shoot(self, player_position):
        dx = player_position[0] - self.rect.centerx
        dy = player_position[1] - self.rect.centery
        angle_to_player = math.atan2(dy, dx)
        projectile_center = Projectile(self.rect.centerx, self.rect.bottom, int(math.degrees(angle_to_player)))
        projectile_left = Projectile(self.rect.centerx, self.rect.bottom,
                                     int(math.degrees(angle_to_player + math.pi / 8)))
        projectile_right = Projectile(self.rect.centerx, self.rect.bottom,
                                      int(math.degrees(angle_to_player - math.pi / 8)))
        projectile_topleft = Projectile(self.rect.left, self.rect.top, int(math.degrees(angle_to_player)))
        projectile_topright = Projectile(self.rect.right, self.rect.top, int(math.degrees(angle_to_player)))
        projectile_topright_left = Projectile(self.rect.right, self.rect.top,
                                              int(math.degrees(angle_to_player + math.pi / 8)))
        projectile_topleft_right = Projectile(self.rect.left, self.rect.top,
                                              int(math.degrees(angle_to_player - math.pi / 8)))
        projectiles.add(projectile_center, projectile_left, projectile_right, projectile_topleft, projectile_topright,
                        projectile_topright_left, projectile_topleft_right)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('assets/beam.png').convert_alpha(), (10, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 10
        self.angle = angle
        self.speedx = math.sin(math.radians(angle)) * self.speed
        self.speedy = -math.cos(math.radians(angle)) * self.speed
        self.damage = damage

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class BigBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("assets/beam.png"), (30, 75))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 10
        self.angle = angle
        self.speedx = math.sin(math.radians(angle)) * self.speed
        self.speedy = -math.cos(math.radians(angle)) * self.speed
        self.damage = damage

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=90):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load('assets/Fireball1.png').convert_alpha(), (30, 30)),
                       pygame.transform.scale(pygame.image.load('assets/Fireball2.png').convert_alpha(), (30, 30))]
        self.index = 0
        self.image = self.images[self.index]
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speed = 10
        self.angle = math.radians(angle)
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        self.animation_speed = 150
        self.last_update = pygame.time.get_ticks()
        self.damage = 10

    def update(self, height):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > height:
            self.kill()
        angle = math.degrees(math.atan2(-self.speed_y, self.speed_x))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("assets/player.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = spawn_x / 2
        self.rect.bottom = spawn_y - 50
        self.speed_x = 0
        self.speed_y = 0
        self.hp = 150
        self.invincible = False
        self.invincible_duration = 1000
        self.invincible_timer = pygame.time.get_ticks()
        self.last_flash = 0

    def update(self, range_x, range_y):
        current_time = pygame.time.get_ticks()
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speed_x = -7.5
        if keystate[pygame.K_d]:
            self.speed_x = 7.5
        if keystate[pygame.K_w]:
            self.speed_y = -7.5
        if keystate[pygame.K_s]:
            self.speed_y = 7.5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right >= range_x:
            self.rect.right = range_x
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= range_y:
            self.rect.bottom = range_y
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.invincible:
            if current_time - self.invincible_timer > self.invincible_duration:
                self.invincible = False
                self.image.set_alpha(255)
            elif current_time - self.last_flash > 100:
                self.image.set_alpha(80 if self.image.get_alpha() == 255 else 255)
                self.last_flash = current_time

    def hit(self, damage):
        if not self.invincible:
            self.hp -= damage
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()

    def default_shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 12)
        bullets.add(bullet)

    def shotgun_shoot(self):
        bullet_center = Bullet(self.rect.centerx, self.rect.top, 8, angle=0)
        bullet_left = Bullet(self.rect.centerx, self.rect.top, 8, angle=-15)
        bullet_right = Bullet(self.rect.centerx, self.rect.top, 8, angle=15)
        bullets.add(bullet_center)
        bullets.add(bullet_left)
        bullets.add(bullet_right)

    def triple_shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)

        bullet = Bullet(self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)

        bullet = Bullet(self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)

    def mega_shoot(self):
        bullet = BigBullet(self.rect.centerx, self.rect.top, 75)
        bullets.add(bullet)


class Gameplay:
    def __init__(self, width, height, screen, weapon_selected, volume):
        self.width = width
        self.height = height
        self.screen = screen
        self.weapon_selected = weapon_selected
        self.volume = volume
        self.game_over = False

    def start_tutorial(self):
        to_menu = MenuButton(self.width * 7 / 8 - 300, self.height / 1.5, 300, self.height / 15, 'В меню',
                             'assets/red_button.png',
                             'assets/red_button_hover.png', 'assets/click.ogg')
        font = pygame.font.Font('assets/Silver.ttf', 50)
        score, combo, last_mob_spawn, last_mob_shoot, last_elite_spawn, last_elite_type, last_elite_shoot, last_fireball_spawn, last_boss_shoot, pause_start_time, pause_duration, boss_count = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        mobs_music = 'assets/cave_mobs.mp3'
        boss_music = 'assets/cave_boss.mp3'
        pygame.mixer.music.load(mobs_music)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        paused = False
        clock = pygame.time.Clock()
        player = Player(self.width, self.height)
        player_sprite.add(player)
        background = pygame.transform.scale(pygame.image.load('assets/cave.png').convert(), (self.width, self.height))
        pause_surface = pygame.Surface((self.width, self.height))
        pause_surface.set_alpha(128)
        start_time = pygame.time.get_ticks()
        boss_music_playing = False
        running = True
        while running:
            clock.tick(60)
            if not paused:
                game_time = pygame.time.get_ticks() - pause_duration
                self.screen.blit(background, (0, 0))

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.weapon_selected == 0:
                                player.default_shoot()
                            elif self.weapon_selected == 1:
                                player.shotgun_shoot()
                            elif self.weapon_selected == 2:
                                player.triple_shoot()
                            elif self.weapon_selected == 3:
                                player.mega_shoot()
                        elif event.key == pygame.K_ESCAPE:
                            paused = not paused

                if not boss_music_playing and game_time - start_time >= 89000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(boss_music)
                    pygame.mixer.music.set_volume(self.volume * 0.8)
                    pygame.mixer.music.play()
                    boss_music_playing = True

                if 7000 <= game_time - start_time <= 44000:
                    if game_time - last_mob_spawn >= 3000:
                        mob = Mob(self.width, self.height)
                        mobs.add(mob)
                        last_mob_spawn = game_time
                if 68000 <= game_time - start_time <= 89000:
                    if game_time - last_mob_spawn >= 5000:
                        mob = Mob(self.width, self.height)
                        mobs.add(mob)
                        last_mob_spawn = game_time

                if 89000 >= game_time - start_time >= 44000:
                    if game_time - last_elite_spawn >= 3000:
                        elite = Elite(self.width, self.height, last_elite_type)
                        elites.add(elite)
                        last_elite_spawn = game_time
                        if last_elite_type == 0:
                            last_elite_type = 1
                        elif last_elite_type == 1:
                            last_elite_type = 0

                if game_time - start_time >= 89000:
                    if boss_count < 1:
                        for mob in mobs:
                            mob.kill()
                        for elite in elites:
                            elite.kill()
                        boss = Boss(self.width, self.height)
                        boss_sprite.add(boss)
                        boss_count = 1

                if game_time - start_time >= 59000 or 44000 >= game_time - start_time >= 22000:
                    if game_time - last_fireball_spawn >= 500:
                        fireball = Projectile(random.randint(0, self.width), 0)
                        projectiles.add(fireball)
                        last_fireball_spawn = game_time

                if game_time - last_mob_shoot >= 2000:
                    for mob in mobs:
                        mob.shoot((player.rect.centerx, player.rect.centery))
                    last_mob_shoot = game_time

                if game_time - last_elite_shoot >= 3000:
                    for elite in elites:
                        elite.shoot((player.rect.centerx, player.rect.centery))
                    last_elite_shoot = game_time

                if game_time - last_boss_shoot >= 1500:
                    for boss in boss_sprite:
                        boss.shoot((player.rect.centerx, player.rect.centery))
                    last_boss_shoot = game_time

                boss_sprite.update(self.width, self.height)
                mobs.update(self.width, self.height)
                elites.update(self.width, self.height)
                projectiles.update(self.height)
                bullets.update()
                player_sprite.update(self.width, self.height)

                hits = pygame.sprite.spritecollide(player, mobs, False)
                for hit in hits:
                    combo = 0
                    player.hit(10)

                hits = pygame.sprite.spritecollide(player, elites, False)
                for hit in hits:
                    combo = 0
                    player.hit(20)

                hits = pygame.sprite.spritecollide(player, boss_sprite, False)
                for hit in hits:
                    combo = 0
                    player.hit(40)

                for mob in mobs:
                    hits = pygame.sprite.spritecollide(mob, bullets, True)
                    for bullet in hits:
                        combo += 10
                        score += combo
                        mob.hit(bullet.damage)

                for elite in elites:
                    hits = pygame.sprite.spritecollide(elite, bullets, True)
                    for bullet in hits:
                        combo += 10
                        score += combo
                        elite.hit(bullet.damage)

                for boss in boss_sprite:
                    hits = pygame.sprite.spritecollide(boss, bullets, True)
                    for bullet in hits:
                        combo += 10
                        score += combo
                        boss.hit(bullet.damage)

                hits = pygame.sprite.groupcollide(player_sprite, projectiles, False, True)
                if hits:
                    player.hit(10)

                if player.hp <= 0:
                    pygame.mixer.music.stop()
                    bullets.empty()
                    mobs.empty()
                    elites.empty()
                    boss_sprite.empty()
                    projectiles.empty()
                    player_sprite.empty()
                    self.update_file(score, self.weapon_selected)
                    self.game_over_screen('Игра окончена', score, self.width, self.height, self.screen,
                                          self.weapon_selected, self.volume)
                    running = False
                if game_time - start_time >= 89000:
                    if boss.hp <= 0:
                        pygame.mixer.music.stop()
                        bullets.empty()
                        mobs.empty()
                        elites.empty()
                        boss_sprite.empty()
                        projectiles.empty()
                        player_sprite.empty()
                        self.update_file(score, self.weapon_selected)
                        self.game_over_screen('Уровень пройден!', score, self.width, self.height, self.screen,
                                              self.weapon_selected, self.volume)
                        running = False

            if paused:
                if pause_start_time == 0:
                    pause_start_time = pygame.time.get_ticks()
                    pygame.mixer.music.pause()

                self.screen.blit(background, (0, 0))
                self.screen.blit(pause_surface, (0, 0))
                text_surface = font.render("Пауза", True, (106, 90, 205))
                text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
                self.screen.blit(text_surface, text_rect)

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pause_end_time = pygame.time.get_ticks()
                            pause_duration += pause_end_time - pause_start_time
                            pause_start_time = 0
                            pygame.mixer.music.unpause()
                            paused = not paused

                    if event.type == pygame.USEREVENT:
                        if event.button == to_menu:
                            boss_music_playing = False
                            pygame.mixer.music.stop()
                            bullets.empty()
                            mobs.empty()
                            elites.empty()
                            boss_sprite.empty()
                            projectiles.empty()
                            player_sprite.empty()
                            self.update_file(score, self.weapon_selected)
                            self.fade(self.width, self.height, self.screen)
                            self.game_over_screen('Игра окончена', score, self.width, self.height, self.screen,
                                                  self.weapon_selected, self.volume)
                            running = False

                    for button in [to_menu]:
                        button.check_click(event)

                for button in [to_menu]:
                    button.check_hover(pygame.mouse.get_pos())
                    button.show(self.screen)

            game_time -= pause_duration
            player_sprite.draw(self.screen)
            projectiles.draw(self.screen)
            bullets.draw(self.screen)
            mobs.draw(self.screen)
            elites.draw(self.screen)
            boss_sprite.draw(self.screen)
            score_text = font.render("Счет:" + str(score), True, (255, 255, 255))
            hp_text = font.render('HP:' + str(player.hp), True, (255, 255, 255))
            if game_time - start_time >= 89000:
                boss_hp_text = font.render('Boss HP:' + str(boss.hp), True, (255, 255, 255))
                self.screen.blit(boss_hp_text, (self.width * (3 / 4), 90))
            self.screen.blit(score_text, (self.width * (3 / 4), 10))
            self.screen.blit(hp_text, (self.width * (3 / 4), 50))
            pygame.display.flip()

    def game_over_screen(self, text, score, width, height, screen, weapon_selected, volume):
        restart = MenuButton(width / 8, height / 1.5, 300, height / 15, 'Заново', 'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        to_menu = MenuButton(width * 7 / 8 - 300, height / 1.5, 300, height / 15, 'В меню', 'assets/red_button.png',
                             'assets/red_button_hover.png', 'assets/click.ogg')
        running = True
        while running:
            screen.fill((0, 0, 0))
            background = pygame.transform.scale(pygame.image.load('assets/cave.png').convert(), (width, height))
            screen.blit(background, (0, 0))
            font = pygame.font.Font('assets/Silver.ttf', 50)
            game_over_text = font.render(f'{text}', True, (255, 255, 255))
            screen.blit(game_over_text,
                        (width / 2 - game_over_text.get_width() / 2, height / 3 - game_over_text.get_height() / 3))
            score_text = font.render(f'Счет: {score}', True, (255, 255, 255))
            screen.blit(score_text,
                        (width / 2 - score_text.get_width() / 2, height / 2 - score_text.get_height() / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == restart:
                    self.fade(width, height, screen)
                    self.start_tutorial()
                    running = False

                if event.type == pygame.USEREVENT and event.button == to_menu:
                    pygame.mixer.music.load('assets/menu_music.mp3')
                    self.fade(width, height, screen)
                    running = False

                for button in [restart, to_menu]:
                    button.check_click(event)

            for button in [restart, to_menu]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(screen)

            pygame.display.flip()

    def update_file(self, new_score, weapon_selected):
        additional_gold = int(new_score / 10)
        with open('assets/info.txt', 'r') as file:
            data = file.read().split(',')
            current_score = int(data[0])
            current_gold = int(data[3])
            score2 = int(data[1])
            score3 = int(data[2])
            current_score = max(current_score, new_score)
            current_gold += additional_gold
            with open('assets/info.txt', 'w') as file:
                file.write(f"{current_score},{score2},{score3},{current_gold},{weapon_selected}")

    def fade(self, width, height, screen):
        clock = pygame.time.Clock()
        running = True
        fade_alpha = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            fade_surface = pygame.Surface((width, height))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

            fade_alpha += 5
            if fade_alpha >= 75:
                fade_alpha = 255
                running = False

            pygame.display.flip()
            clock.tick(60)
