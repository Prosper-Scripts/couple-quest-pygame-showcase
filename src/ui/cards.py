import pygame

from config import PANEL, SHADOW, TEXT


class Card:
    def __init__(self, rect: pygame.Rect, title: str, body: str) -> None:
        self.rect = rect
        self.title = title
        self.body = body

    def draw(self, screen: pygame.Surface, title_font: pygame.font.Font, body_font: pygame.font.Font) -> None:
        shadow_rect = self.rect.move(8, 8)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=24)
        pygame.draw.rect(screen, PANEL, self.rect, border_radius=24)

        title_surface = title_font.render(self.title, True, TEXT)
        screen.blit(title_surface, (self.rect.x + 32, self.rect.y + 24))

        lines = []
        paragraphs = self.body.splitlines() or [self.body]
        for index, paragraph in enumerate(paragraphs):
            lines.extend(self._wrap_text(paragraph, body_font, self.rect.width - 64))
            if index < len(paragraphs) - 1:
                lines.append("")
        for index, line in enumerate(lines):
            body_surface = body_font.render(line, True, TEXT)
            screen.blit(body_surface, (self.rect.x + 32, self.rect.y + 78 + (index * 34)))

    @staticmethod
    def _wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        if not text:
            return [""]

        words = text.split()
        if not words:
            return [""]
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = f"{current_line} {word}"
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines
