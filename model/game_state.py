import settings as s
from model.game_status import GameStatus
from model.game_speed import GameSpeed
from model.boosters.booster import Booster
from model.boosters.booster_gold import BoosterGold
from model.boosters.booster_attack import BoosterAttack
from model.boosters.booster_range import BoosterRange
from model.boosters.booster_speed import BoosterSpeed


class GameState:
    def __init__(self):
        self.gold = s.STARTING_GOLD
        self.lives = s.STARTING_LIVES
        self.wave = 0
        self.score = 0
        self.status = GameStatus.PLAYING
        self.unit_cost = s.UNIT_COST
        self.speed = GameSpeed.NORMAL
        self.moves_remaining = s.MAX_MOVES_PER_LEVEL
        self.elapsed_time = 0.0
        self.boosters = [
            BoosterGold(),
            BoosterRange(),
            BoosterAttack(),
            BoosterSpeed(),
        ]

    def get_booster(self, indice: int) -> Booster:
        """Retourne le booster à l'indice dans la liste des boosters"""
        return self.boosters[indice]

    def deactivate_wave_boosters(self):
        """Appelée en fin de vague pour retirer les effets des boosters en cours"""
        for booster in self.boosters:
            if booster.active:
                booster.desactivate()

    @property
    def game_over(self) -> bool:
        return self.status == GameStatus.GAME_OVER

    @property
    def victory(self) -> bool:
        return self.status == GameStatus.VICTORY

    @property
    def menu(self) -> bool:
        return self.status == GameStatus.MENU

    @property
    def playing(self) -> bool:
        return self.status == GameStatus.PLAYING

    @property
    def info(self) -> bool:
        return self.status == GameStatus.INFO

    def use_move(self) -> bool:
        """Consomme un déplacement. Retourne True si le déplacement est autorisé"""
        if self.moves_remaining <= 0:
            return False
        self.moves_remaining -= 1
        return True

    def add_gold(self, amount: int) -> None:
        self.gold += amount

    def spend_gold(self, amount: int) -> bool:
        """Tente de dépenser de l'or. Retourne True si le paiement a réussi"""
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

    def increment_unit_cost(self) -> None:
        """Augmente le coût d'achat d'une unité après chaque achat"""
        self.unit_cost += s.UNIT_COST_INCREMENT

    def lose_life(self, amount: int = 1) -> None:
        """Retire des vies. Déclenche le game over si on tombe à zéro"""
        self.lives -= amount
        if self.lives <= 0:
            self.status = GameStatus.GAME_OVER

    def add_score(self, amount: int) -> None:
        self.score += amount

    def next_wave(self) -> None:
        self.wave += 1

    def change_speed(self) -> None:
        """Change la vitesse de la partie selon le cycle défini"""
        self.speed = self.speed.change()

    def toggle_menu(self) -> None:
        """Bascule entre PLAYING et MENU"""
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.MENU
        elif self.status == GameStatus.MENU:
            self.status = GameStatus.PLAYING

    def toggle_info(self) -> None:
        """Bascule entre PLAYING et INFO"""
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.INFO
        elif self.status == GameStatus.INFO:
            self.status = GameStatus.PLAYING

    def set_victory(self) -> None:
        self.status = GameStatus.VICTORY

    def __repr__(self) -> str:
        return (
            f"GameState(gold={self.gold}, lives={self.lives}, "
            f"wave={self.wave}, score={self.score}, status={self.status.name})"
        )
