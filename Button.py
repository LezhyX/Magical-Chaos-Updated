import pygame


class MenuButton:
    def __init__(self, x, y, width, height, text, image_path, hover_path=None, sound_path=None, clicked_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_path:
            self.hover_image = pygame.image.load(hover_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))
        if clicked_path:
            self.clicked_image = pygame.image.load(clicked_path)
            self.clicked_image = pygame.transform.scale(self.clicked_image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.hovered = False

    def set_pos(self, x):
        self.x = x
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def show(self, screen):
        if self.hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font('assets/Silver.ttf', 56)
        text_surface = font.render(self.text, True, (106, 90, 205))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.sound:
                self.sound.play()

            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
