# Elo Python Ranking
The elo formula is a method of ranking chess players by calculating relative skill. It has found successful applications in team sports. A python package has been developed to calulate expected probability of victory based on prior skill rankings and update the rankings following a result. 

```python
import elo

league = elo.EloLeague()
league.add_player('John', 1500)
league.add_player('Doe', 1200)

league.game_over(winner_name='John', 
                 loser_name='Doe')

league.print_rankings()

```

