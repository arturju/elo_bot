"""
Simple ELO Rating System
https://www.geeksforgeeks.org/elo-rating-algorithm/

Rn = Ro + K*(S - Se)
where:
Rn = new rating
Ro = old rating
K  = constant (max point transfer)
S  = score
Se = expected score

"""
import csv
import datetime
import logging
import operator
import pathlib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants #
BASE_PATH = pathlib.Path.cwd()
PADDING = 15


class Player(object):
    def __init__(self, name: str, rating: int = 1500.0000):
        self.name = name.lower()
        self.rating = rating

        all_files = [str(x) for x in BASE_PATH.iterdir()]
        is_player_exist = any([self.name in item for item in all_files])
        if is_player_exist:
            logger.error("A player by this name already exists. Pick a different name")
            raise OSError
        else:
            self.player_file = BASE_PATH.joinpath(f"{self.name}.csv")
            self.player_file.touch()
            with open(self.player_file, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                logger.debug(f"Writing headers to {self.player_file}")
                csv_writer.writerow(['date', 'time', 'rating'])
            self.save_player_record()

    def __str__(self):
        return f"{self.name}".ljust(PADDING) + f"| {self.rating}"

    def __repr__(self):
        return f"Player(name='{self.name}', rating={self.rating})"

    def save_player_record(self):
        date_time = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S").split(',')
        line = [date_time[0], date_time[1], self.rating]
        with open(self.player_file, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            logger.debug(f"Writing {self.name} rating data to file...")
            csv_writer.writerow(line)

    def update_player_rating(self, new_rating):
        self.rating = new_rating
        self.save_player_record()


class EloLeague(object):
    def __init__(self, k: int = 30):
        # TODO load existing data if available?
        self.players = {}
        self.k = k

    def add_player(self, name: str, rating: int = 1500):
        self.players.update({name.lower(): Player(name=name, rating=rating)})
        logger.info(f"Added {name.lower()} to player's list. Rating is {rating}")

    @staticmethod
    def expected_result(p1_rating: float, p2_rating: float) -> float:
        """Calculates probability of p1 winning. Basic Elo formula
        :param p1_rating: (float) Player1 rating
        :param p2_rating: (float) Player2 rating
        :return: (float) Probability of P1 winning, (P1+P2=1)
        """
        p1_win_exponent = (p2_rating - p1_rating) / 400
        p1_win = 1 / (1 + 10.0 ** p1_win_exponent)
        return p1_win

    def game_over(self, winner_name: str, loser_name: str):
        """Performs point swap between two players"""
        p1_name = winner_name.lower().replace(' ', '')
        p2_name = loser_name.lower().replace(' ', '')
        try:
            p1_rating = self.players[p1_name].rating
            p2_rating = self.players[p2_name].rating
            prob_p1_win = self.expected_result(p1_rating, p2_rating)
            prob_p2_win = 1 - prob_p1_win
            new_p1_rating = round(p1_rating + self.k * (1 - prob_p1_win), 4)
            new_p2_rating = round(p2_rating + self.k * (0 - prob_p2_win), 4)
            self.players[p1_name].update_player_rating(new_rating=new_p1_rating)
            self.players[p2_name].update_player_rating(new_rating=new_p2_rating)
            logger.info(f"New rating {p1_name}:{new_p1_rating}, {p2_name}:{new_p2_rating}")
        except KeyError:
            logger.warning(f"{p1_name} or {p2_name} does not exist. Add user with add_player()")

    def print_rankings(self):
        """Prints ratings dictionary in highest to lowest"""
        sorted_league = sorted(self.players.values(), key=operator.attrgetter('rating'), reverse=True)
        print("Player Name".ljust(PADDING), "| Ranking ")
        for player in sorted_league:
            print(player)

