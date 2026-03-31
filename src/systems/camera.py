"""
Sistema de câmera que segue os jogadores.
"""
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """
    Câmera que centraliza entre os dois jogadores,
    com limites do mapa.
    """

    def __init__(self, map_width, map_height):
        self.map_w   = map_width
        self.map_h   = map_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, players):
        """Centraliza a câmera entre os jogadores ativos."""
        alive = [p for p in players if p.alive]
        if not alive:
            return

        # Centro entre os jogadores
        cx = sum(p.rect.centerx for p in alive) // len(alive)
        cy = sum(p.rect.centery for p in alive) // len(alive)

        # Offset para centralizar na tela
        ox = cx - SCREEN_WIDTH  // 2
        oy = cy - SCREEN_HEIGHT // 2

        # Limita aos limites do mapa
        ox = max(0, min(ox, self.map_w - SCREEN_WIDTH))
        oy = max(0, min(oy, self.map_h - SCREEN_HEIGHT))

        # Suavização
        self.offset_x += (ox - self.offset_x) * 0.12
        self.offset_y += (oy - self.offset_y) * 0.12

    def apply(self, rect):
        """Retorna rect ajustado para a câmera."""
        return rect.move(-int(self.offset_x), -int(self.offset_y))

    def get_offset(self):
        return (int(self.offset_x), int(self.offset_y))
