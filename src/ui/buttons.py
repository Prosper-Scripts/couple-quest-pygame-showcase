import pygame

from config import ACCENT, ACCENT_DARK, MUTED, PANEL_ALT, TEXT


class Button:
    def __init__(self, label: str, rect: pygame.Rect, subtle: bool = False) -> None:
        self.label = label
        self.rect = rect
        self.subtle = subtle
        self.hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        draw_rect = self.rect.copy()
        if self.hovered:
            pulse = 1 + (0.02 * ((pygame.time.get_ticks() % 800) / 800))
            width = int(self.rect.width * pulse)
            height = int(self.rect.height * pulse)
            draw_rect = pygame.Rect(0, 0, width, height)
            draw_rect.center = self.rect.center

        if self.subtle:
            fill = PANEL_ALT if self.hovered else (255, 245, 240)
            text_color = MUTED
        else:
            fill = ACCENT_DARK if self.hovered else ACCENT
            text_color = (255, 248, 245)

        pygame.draw.rect(screen, fill, draw_rect, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), draw_rect, 2, border_radius=18)
        label_surface = font.render(self.label, True, text_color if self.subtle else text_color)
        label_rect = label_surface.get_rect(center=draw_rect.center)
        screen.blit(label_surface, label_rect)
