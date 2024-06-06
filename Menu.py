import pygame
import sys
from Button import MenuButton
from Tutorial import Gameplay
from Level1 import Gameplay1
from Level2 import Gameplay2


class Main_menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.width, self.height, self.max_fps = 1280, 720, 30
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Magical Chaos")
        self.menu_background = pygame.image.load('assets/menu_background_720.jpg')
        self.clock = pygame.time.Clock()
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.fullscreen_mode = False
        self.current_volume = 0.2
        pygame.mixer.music.load('assets/menu_music.mp3')
        pygame.mixer.music.set_volume(self.current_volume)
        pygame.mixer.music.play(-1)

    def main_menu(self):
        choose_level = MenuButton(self.width / 2 - 200, self.height / 5, 400, self.height / 10, 'Выбрать уровень',
                                  'assets/red_button.png',
                                  'assets/red_button_hover.png', 'assets/click.ogg')
        gear = MenuButton(self.width / 2 - 200, self.height / 3, self.width / 3.2, 50, 'Снаряжение',
                          'assets/yellow_button.png',
                          'assets/yellow_button_hover.png', 'assets/click.ogg')
        introduction = MenuButton(self.width / 2 - 200, self.height / 3 + 80, self.width / 3.2, self.height / 14.4,
                                  'Справка', 'assets/yellow_button.png', 'assets/yellow_button_hover.png',
                                  'assets/click.ogg')
        settings = MenuButton(self.width / 2 - 200, self.height / 3 + 160, self.width / 3.2, self.height / 14.4,
                              'Настройки', 'assets/yellow_button.png', 'assets/yellow_button_hover.png',
                              'assets/click.ogg')
        log_out = MenuButton(self.width / 2 - 200, self.height / 3 + 240, self.width / 3.2, self.height / 14.4, 'Выйти',
                             'assets/yellow_button.png', 'assets/yellow_button_hover.png', 'assets/click.ogg')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 150)
            text_surface = font.render("Magical Chaos", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.logout_confirmation()

                if event.type == pygame.USEREVENT and event.button == choose_level:
                    self.fade()
                    self.level_selection()

                if event.type == pygame.USEREVENT and event.button == settings:
                    self.fade()
                    self.settings_menu()

                if event.type == pygame.USEREVENT and event.button == gear:
                    self.fade()
                    self.gear_menu()

                if event.type == pygame.USEREVENT and event.button == introduction:
                    self.fade()
                    self.introduction_menu()

                if event.type == pygame.USEREVENT and event.button == log_out:
                    self.logout_confirmation()

                for button in [choose_level, gear, introduction, settings, log_out]:
                    button.check_click(event)

            for button in [choose_level, gear, introduction, settings, log_out]:
                button.set_pos(self.width / 2 - 200)
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()

    def level_selection(self):
        with open('assets/info.txt', 'r') as file:
            data = file.read().split(',')
            score1 = int(data[0])
            score2 = int(data[1])

        if score1 >= 75000:
            text1 = 'В небе...'
        else:
            text1 = 'Наберите 75000 очков в пещерах'

        if score2 >= 100000:
            text2 = 'Под водой...'
        else:
            text2 = 'Наберите 100000 очков в небе'

        tutorial = MenuButton(self.width / 2 - 200, self.height / 5, 400, self.height / 15, 'В пещерах...',
                              'assets/yellow_button.png',
                              'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_one = MenuButton(self.width / 2 - 200, self.height / 5 + 72, 400, self.height / 15, text1,
                               'assets/yellow_button.png',
                               'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_two = MenuButton(self.width / 2 - 200, self.height / 5 + 144, 400, self.height / 15, text2,
                               'assets/yellow_button.png',
                               'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width / 2 - 200, self.height / 5 + 216, 400, self.height / 15, 'Назад',
                          'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 150)
            text_surface = font.render("Выбор уровня", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.USEREVENT and event.button == tutorial:
                    self.tutorial_selection()
                    self.fade()

                if event.type == pygame.USEREVENT and event.button == level_one:
                    if score1 >= 75000:
                        self.level1_selection()
                        self.fade()
                    else:
                        pass

                if event.type == pygame.USEREVENT and event.button == level_two:
                    if score2 >= 100000:
                        self.level2_selection()
                        self.fade()
                    else:
                        pass

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                for button in [tutorial, level_one, level_two, back]:
                    button.check_click(event)

            for button in [tutorial, level_one, level_two, back]:
                button.set_pos(self.width / 2 - 200)
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()

    def tutorial_selection(self):
        with open('assets/info.txt', 'r') as file:
            data = file.read().split(',')
            weapon_selected = int(data[4])
        start = MenuButton(self.width / 8, self.height / 1.5, 300, self.height / 15, 'Начать',
                           'assets/yellow_button.png',
                           'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width * 7 / 8 - 300, self.height / 1.5, 300, self.height / 15, 'Назад',
                          'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')

        running = True
        while running:
            with open('assets/info.txt', 'r') as file:
                data = file.read().split(',')
                score = int(data[0])

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 50)
            text_surface = font.render("Первый уровень", True, (255, 0, 0))
            text_surface1 = font.render(f'Максимум очков: {score}', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.width / 2, 300))
            text_rect1 = text_surface1.get_rect(center=(self.width / 2, 350))
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(text_surface1, text_rect1)

            font = pygame.font.Font('assets/Silver.ttf', 150)
            text_surface = font.render("Уровень 1: Пещеры", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == start:
                    self.fade()
                    pygame.mixer.music.stop()
                    game = Gameplay(self.width, self.height, self.screen, weapon_selected, self.current_volume)
                    game.start_tutorial()
                    pygame.mixer.music.play(-1)

                for button in [start, back]:
                    button.check_click(event)

            for button in [start, back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()

    def settings_menu(self):
        video = MenuButton(self.width / 2 - 200, self.height / 5, 400, self.height / 15, 'Видео',
                           'assets/yellow_button.png',
                           'assets/yellow_button_hover.png', 'assets/click.ogg')
        audio = MenuButton(self.width / 2 - 200, self.height / 5 + 72, 400, self.height / 15, 'Аудио',
                           'assets/yellow_button.png',
                           'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width / 2 - 200, self.height / 5 + 144, 400, self.height / 15, 'Назад',
                          'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 100)
            text_surface = font.render("Настройки", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, 100))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == video:
                    self.fade()
                    self.video_settings()

                if event.type == pygame.USEREVENT and event.button == audio:
                    self.fade()
                    self.change_volume()

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                for button in [video, audio, back]:
                    button.check_click(event)

            for button in [video, audio, back]:
                button.set_pos(self.width / 2 - 200)
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()

    def gear_menu(self):
        default = pygame.transform.scale(pygame.image.load('assets/default_weapon.png').convert_alpha(),
                                         (self.width / 8, self.width / 8))
        shotgun = pygame.transform.scale(pygame.image.load('assets/shotgun.png').convert_alpha(),
                                         (self.width / 8, self.width / 8))
        triple = pygame.transform.scale(pygame.image.load('assets/triple.png').convert_alpha(),
                                         (self.width / 8, self.width / 8))
        mega = pygame.transform.scale(pygame.image.load('assets/bigshot.png').convert_alpha(),
                                         (self.width / 8, self.width / 8))
        with open('assets/info.txt', 'r') as file:
            data = file.read().split(',')
            weapon_selected = int(data[4])
            score1 = int(data[0])
            score2 = int(data[1])
            score3 = int(data[2])
        if weapon_selected == 0:
            text_1 = 'Выбрано'
            if score1 < 50000:
                text_2 = 'Набрать 50000 очков в пещерах'
            else:
                text_2 = 'Выбрать'
            if score2 < 50000:
                text_3 = 'Набрать 50000 очков в небе'
            else:
                text_3 = 'Выбрать'
            if score3 < 50000:
                text_4 = 'Набрать 50000 очков под водой'
            else:
                text_4 = 'Выбрать'
        elif weapon_selected == 1:
            text_1 = 'Выбрать'
            text_2 = 'Выбрано'
            if score2 < 50000:
                text_3 = 'Набрать 50000 очков в небе'
            else:
                text_3 = 'Выбрать'
            if score3 < 50000:
                text_4 = 'Набрать 50000 очков под водой'
            else:
                text_4 = 'Выбрать'
        elif weapon_selected == 2:
            text_1 = 'Выбрать'
            text_3 = 'Выбрано'
            if score1 < 50000:
                text_2 = 'Набрать 50000 очков в пещерах'
            else:
                text_2 = 'Выбрать'
            if score3 < 50000:
                text_4 = 'Набрать 50000 очков под водой'
            else:
                text_4 = 'Выбрать'
        elif weapon_selected == 3:
            text_1 = 'Выбрать'
            text_4 = 'Выбрано'
            if score1 < 50000:
                text_2 = 'Набрать 50000 очков в пещерах'
            else:
                text_2 = 'Выбрать'
            if score2 < 50000:
                text_3 = 'Набрать 50000 очков в небе'
            else:
                text_3 = 'Выбрать'
        select_1 = MenuButton(self.width / 8 - 75, self.height / 1.5, self.width / 6, self.height / 15,
                              f'{text_1}',
                              'assets/yellow_button.png',
                              'assets/yellow_button_hover.png', 'assets/click.ogg')
        select_2 = MenuButton(self.width * 3 / 8 - 75, self.height / 1.5, self.width / 6, self.height / 15, f'{text_2}',
                              'assets/yellow_button.png', 'assets/yellow_button_hover.png', 'assets/click.ogg')
        select_3 = MenuButton(self.width * 5 / 8 - 75, self.height / 1.5, self.width / 6, self.height / 15,
                              f'{text_3}',
                              'assets/yellow_button.png',
                              'assets/yellow_button_hover.png', 'assets/click.ogg')
        select_4 = MenuButton(self.width * 7 / 8 - 75, self.height / 1.5, self.width / 6, self.height / 15,
                              f'{text_4}',
                              'assets/yellow_button.png',
                              'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width * 0.01, (self.height * 0.98) - (self.height / 14), self.width / 6,
                          self.height / 14, 'Назад',
                          'assets/red_button.png', 'assets/red_button_hover.png', 'assets/click.ogg')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 100)
            text_surface = font.render("Снаряжение", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == select_1:
                    if weapon_selected == 0:
                        pass
                    else:
                        with open('assets/info.txt', 'r') as file:
                            data = file.read().split(',')
                            score1 = int(data[0])
                            score2 = int(data[1])
                            score3 = int(data[2])
                            gold = int(data[3])
                            weapon_to_rewrite = 0
                            with open('assets/info.txt', 'w') as file:
                                file.write(f"{score1},{score2},{score3},{gold},{weapon_to_rewrite}")
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == select_2:
                    if weapon_selected == 1:
                        pass
                    with open('assets/info.txt', 'r') as file:
                        data = file.read().split(',')
                        score1 = int(data[0])
                        score2 = int(data[1])
                        score3 = int(data[2])
                        gold = int(data[1])
                    if score1 < 50000:
                        pass
                    else:
                        weapon_to_rewrite = 1
                        with open('assets/info.txt', 'w') as file:
                            file.write(f"{score1},{score2},{score3},{gold},{weapon_to_rewrite}")
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == select_3:
                    if weapon_selected == 2:
                        pass
                    with open('assets/info.txt', 'r') as file:
                        data = file.read().split(',')
                        score1 = int(data[0])
                        score2 = int(data[1])
                        score3 = int(data[2])
                        gold = int(data[1])
                    if score2 < 75000:
                        pass
                    else:
                        weapon_to_rewrite = 2
                        with open('assets/info.txt', 'w') as file:
                            file.write(f"{score1},{score2},{score3},{gold},{weapon_to_rewrite}")
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == select_4:
                    if weapon_selected == 3:
                        pass
                    with open('assets/info.txt', 'r') as file:
                        data = file.read().split(',')
                        score1 = int(data[0])
                        score2 = int(data[1])
                        score3 = int(data[2])
                        gold = int(data[1])
                    if score3 < 100000:
                        pass
                    else:
                        weapon_to_rewrite = 3
                        with open('assets/info.txt', 'w') as file:
                            file.write(f"{score1},{score2},{score3},{gold},{weapon_to_rewrite}")
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                for button in [select_1, select_2, select_3, select_4, back]:
                    button.check_click(event)

            self.screen.blit(default, (self.width / 8 - 50, self.height / 3))
            self.screen.blit(shotgun, (self.width * 3 / 8 - 50, self.height / 3))
            self.screen.blit(triple, (self.width * 5 / 8 - 50, self.height / 3))
            self.screen.blit(mega, (self.width * 7 / 8 - 50, self.height / 3))
            for button in [select_1, select_2, select_3, select_4, back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)

            pygame.display.flip()

    def introduction_menu(self):
        back = MenuButton(self.width / 2 - 200, self.height / 2, 400, self.height / 10, 'Ok', 'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 50)
            text_surface = font.render("Меню: Esc-назад", True, (255, 100, 150))
            text_surface1 = font.render("Игра: WASD-движение, Пробел-стрельба, Esc-пауза", True, (255, 100, 150))
            text_rect = text_surface.get_rect(center=(self.width / 2, 200))
            text_rect1 = text_surface.get_rect(center=(self.width / 2 - text_surface1.get_width() / 4, 300))
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(text_surface1, text_rect1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                for button in [back]:
                    button.check_click(event)

            for button in [back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)

            pygame.display.flip()

    def logout_confirmation(self):
        logout = MenuButton((self.width / 3) - (self.width / 6.4), self.height / 1.8, self.width / 3.2,
                            self.height / 9.6, 'Да',
                            'assets/red_button.png',
                            'assets/red_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width * 2 / 3 - (self.width / 6.4), self.height / 1.8, self.width / 3.2,
                          self.height / 9.6, 'Нет',
                          'assets/yellow_button.png', 'assets/yellow_button_hover.png', 'assets/click.ogg')

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 100)
            text_surface = font.render("Выйти из игры?", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, 200))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    running = False

                if event.type == pygame.USEREVENT and event.button == logout:
                    running = False
                    pygame.quit()
                    sys.exit()

                for button in [logout, back]:
                    button.check_click(event)

            for button in [logout, back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)

            pygame.display.flip()

    def video_settings(self):
        sd = MenuButton(self.width / 2 - 200, self.height / 4, 400, self.height / 15, '960x544',
                        'assets/yellow_button.png',
                        'assets/yellow_button_hover.png', 'assets/click.ogg')
        hd = MenuButton(self.width / 2 - 200, self.height / 4 + 72, 400, self.height / 15, '1280x720',
                        'assets/yellow_button.png',
                        'assets/yellow_button_hover.png', 'assets/click.ogg')
        fullhd = MenuButton(self.width / 2 - 200, self.height / 4 + 144, 400, self.height / 15, '1920x1080',
                            'assets/yellow_button.png',
                            'assets/yellow_button_hover.png', 'assets/click.ogg')
        fullscreen = MenuButton(self.width / 2 - 200, self.height / 4 + 216, 400, self.height / 15, 'Полный экран',
                                'assets/yellow_button.png',
                                'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width / 2 - 200, self.height / 4 + 288, 400, self.height / 15, 'Назад',
                          'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 100)
            text_surface = font.render("Выбор разрешения", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, 100))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == sd:
                    self.change_resolution(960, 544)
                    running = False

                if event.type == pygame.USEREVENT and event.button == hd:
                    self.change_resolution(1280, 720)
                    running = False

                if event.type == pygame.USEREVENT and event.button == fullhd:
                    self.change_resolution(1920, 1080)
                    running = False

                if event.type == pygame.USEREVENT and event.button == fullscreen:
                    self.switch_fullscreen()
                    running = False

                for button in [sd, hd, fullhd, fullscreen, back]:
                    button.check_click(event)

            for button in [sd, hd, fullhd, fullscreen, back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()

    def change_volume(self):
        main_font = pygame.font.Font('assets/Silver.ttf', 100)
        second_font = pygame.font.Font('assets/Silver.ttf', 70)
        if self.current_volume == 0:
            display_volume = 0
        else:
            display_volume = int(self.current_volume * 250)
        back = MenuButton(self.width * 0.01, (self.height * 0.98) - (self.height / 14), self.width / 6,
                          self.height / 14, 'Назад',
                          'assets/red_button.png', 'assets/red_button_hover.png', 'assets/click.ogg')
        level_0 = MenuButton(self.width / 8, self.height / 2, self.width / 10, self.height / 10, '0',
                             'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_1 = MenuButton(self.width / 8 * 2, self.height / 2, self.width / 10, self.height / 10, '20%',
                             'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_2 = MenuButton(self.width / 8 * 3, self.height / 2, self.width / 10, self.height / 10, '40%',
                             'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_3 = MenuButton(self.width / 8 * 4, self.height / 2, self.width / 10, self.height / 10, '60%',
                             'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_4 = MenuButton(self.width / 8 * 5, self.height / 2, self.width / 10, self.height / 10, '80%',
                             'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        level_5 = MenuButton(self.width / 8 * 6, self.height / 2, self.width / 10, self.height / 10, '100%',
                             'assets/yellow_button.png',
                             'assets/yellow_button_hover.png', 'assets/click.ogg')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))
            volume_text = second_font.render(f'Текущий уровень громкости: {display_volume}%', True, (255, 0, 0))
            self.screen.blit(volume_text,
                             (self.width / 2 - volume_text.get_width() / 2,
                              self.height / 2.5 - volume_text.get_height() / 2.5))
            text_surface = main_font.render("Изменить громкость", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade()
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == level_0:
                    self.current_volume = 0
                    pygame.mixer.music.set_volume(self.current_volume)
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == level_1:
                    self.current_volume = 0.08
                    pygame.mixer.music.set_volume(self.current_volume)
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == level_2:
                    self.current_volume = 0.16
                    pygame.mixer.music.set_volume(self.current_volume)
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == level_3:
                    self.current_volume = 0.24
                    pygame.mixer.music.set_volume(self.current_volume)
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == level_4:
                    self.current_volume = 0.32
                    pygame.mixer.music.set_volume(self.current_volume)
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == level_5:
                    self.current_volume = 0.4
                    pygame.mixer.music.set_volume(self.current_volume)
                    self.fade()
                    running = False

                for button in [back, level_0, level_1, level_2, level_3, level_4, level_5]:
                    button.check_click(event)

            for button in [back, level_0, level_1, level_2, level_3, level_4, level_5]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)

            pygame.display.flip()

    def change_resolution(self, w, h):
        self.width, self.height = w, h
        self.screen = pygame.display.set_mode((w, h))
        self.menu_background = pygame.image.load(f'assets/menu_background_{h}.jpg')
        self.fade()

    def switch_fullscreen(self):
        self.width, self.height = self.monitor_size
        self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
        self.menu_background = pygame.image.load('assets/menu_background_1080.jpg')

    def fade(self):
        running = True
        fade_alpha = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            self.screen.blit(fade_surface, (0, 0))

            fade_alpha += 5
            if fade_alpha >= 75:
                fade_alpha = 255
                running = False

            pygame.display.flip()
            self.clock.tick(self.max_fps)

    def level1_selection(self):
        with open('assets/info.txt', 'r') as file:
            data = file.read().split(',')
            weapon_selected = int(data[4])
        start = MenuButton(self.width / 8, self.height / 1.5, 300, self.height / 15, 'Начать',
                           'assets/yellow_button.png',
                           'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width * 7 / 8 - 300, self.height / 1.5, 300, self.height / 15, 'Назад',
                          'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')

        running = True
        while running:
            with open('assets/info.txt', 'r') as file:
                data = file.read().split(',')
                score2 = int(data[1])

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 50)
            text_surface = font.render("Второй уровень", True, (255, 0, 0))
            text_surface1 = font.render(f'Максимум очков: {score2}', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.width / 2, 300))
            text_rect1 = text_surface1.get_rect(center=(self.width / 2, 350))
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(text_surface1, text_rect1)

            font = pygame.font.Font('assets/Silver.ttf', 150)
            text_surface = font.render("Уровень 2: Небо", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == start:
                    self.fade()
                    pygame.mixer.music.stop()
                    game = Gameplay1(self.width, self.height, self.screen, weapon_selected, self.current_volume)
                    game.start_level1()
                    pygame.mixer.music.play(-1)

                for button in [start, back]:
                    button.check_click(event)

            for button in [start, back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()

    def level2_selection(self):
        with open('assets/info.txt', 'r') as file:
            data = file.read().split(',')
            weapon_selected = int(data[4])
        start = MenuButton(self.width / 8, self.height / 1.5, 300, self.height / 15, 'Начать',
                           'assets/yellow_button.png',
                           'assets/yellow_button_hover.png', 'assets/click.ogg')
        back = MenuButton(self.width * 7 / 8 - 300, self.height / 1.5, 300, self.height / 15, 'Назад',
                          'assets/red_button.png',
                          'assets/red_button_hover.png', 'assets/click.ogg')

        running = True
        while running:
            with open('assets/info.txt', 'r') as file:
                data = file.read().split(',')
                score3 = int(data[2])

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            font = pygame.font.Font('assets/Silver.ttf', 50)
            text_surface = font.render("Третий уровень", True, (255, 0, 0))
            text_surface1 = font.render(f'Максимум очков: {score3}', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.width / 2, 300))
            text_rect1 = text_surface1.get_rect(center=(self.width / 2, 350))
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(text_surface1, text_rect1)

            font = pygame.font.Font('assets/Silver.ttf', 150)
            text_surface = font.render("Уровень 3: Вода", True, (255, 90, 205))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 7.2))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.USEREVENT and event.button == back:
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == start:
                    self.fade()
                    pygame.mixer.music.stop()
                    game = Gameplay2(self.width, self.height, self.screen, weapon_selected, self.current_volume)
                    game.start_level2()
                    pygame.mixer.music.play(-1)

                for button in [start, back]:
                    button.check_click(event)

            for button in [start, back]:
                button.check_hover(pygame.mouse.get_pos())
                button.show(self.screen)
            pygame.display.flip()


if __name__ == '__main__':
    menu = Main_menu()
    menu.main_menu()
