# Python Library for Foot Ball World Cup ScoreCard


![football-world-cup-2018](https://user-images.githubusercontent.com/435616/212528883-c69c0461-d632-49c9-af9b-97589bbf7251.jpg)



[Source-Wikimedia](https://www.publicdomainpictures.net/en/view-image.php?image=257160&picture=football-world-cup-2018)

# What is this Library

You are working in a sports data company, and we would like you to develop a new Live Football ##World Cup Scoreboard library (or frontend application) that shows all the ongoing matches and their ##scores.

you can install this library using pip which downloads the package from [PyPi](https://pypi.org/project/scorecardlib/). 


### The scoreboard supports the following operations:

1. Start a new game, assuming initial score 0 – 0 and adding it the scoreboard.
This should capture following parameters:
  a. Home team
  b. Away team
2. Update score. This should receive a pair of absolute scores: home team score and away team score.

3. Finish game currently in progress. This removes a match from the scoreboard.

4. Get a summary of games in progress ordered by their total score. The games with the same total score will be returned ordered by the most recently started match in the scoreboard.

## This library contains two classes called Game and ScoreBoard. Below is how the classes look like - 

_Game class:_

**Properties:** home team, away team, home team score, away team score, start time, end time

**Methods:** update_score, finish_game, total_Score, get_scores

_Scoreboard class_:

**Properties:** list of Match objects

**Methods:** start_game, update_score, check_if_match_ongoing, get_game_score, finish_game, get_games_summary

     
 ## Unit Tests
 
 This library was developed using test driven approach where tests were thought out properly. Moreover, these tests utilize the sample data given below.
 
 Sample games can be inserted in the scoreboard based on below sequence. 
 
      a. Mexico 0 - Canada 5
      b. Spain 10 - Brazil 2
      c. Germany 2 - France 2
      d. Uruguay 6 - Italy 6
      e. Argentina 3 - Australia 1
      
  Summary should be generated as per below:
  
       1. Uruguay 6 - Italy 6
       2. Spain 10 - Brazil 2
       3. Mexico 0 - Canada 5
       4. Argentina 3 - Australia 1
       5. Germany 2 - France 2
      

## How to install the library 

#### pip install scorecardlib  

or 

- Clone this library locally on your machine using https://github.com/vivekfe/scorecardlib.git

- Navigate to newly created folder on your machine using command line or powershell. You should be able to see a file named Pyproject.toml

- Since all the configurations already exists, please run **poetry install** to install the virtual environment.

- Open the project using Pycharm and run all the tests to see if the project is working correctly.

## Some examples on running the library

```
from scorecardlib.scoreboard import Scoreboard
leaderboard = Scoreboard()
home_team = "Germany"
away_team = "France"
leaderboard.start_game(home_team, away_team)
leaderboard.update_score(home_team, away_team, 10, 5)
print(leaderboard.games[match_key].home_score)
print(leaderboard.games[match_key].away_score)

```