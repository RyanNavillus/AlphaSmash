# Using AlphaRank to Rank Smash Pros
**I am not claiming that these are the definitive ranks for this year, I am simply hoping to introduce the community to an exciting new tool that came out of game theory research recently**
**Please do NOT use this tool for seeding without fully understanding the method or at least consulting me.**

This is a simple script that uses DeepMind's [Alpha-Rank algorithm](https://arxiv.org/abs/1903.01373) to rank the top 10 Super Smash Bros Melee players for 2022 (so far). (Fair warning: this paper is extremely complicated, I've attempted to explain the core concepts in this README).

When you evaluate head-to-head matchups, you intuitively value certain head-to-heads more than others. An advantage over the #1 best player is obviously more important than the 50th best player. However, this ranking becomes cyclic if you also decide who is 1st or 50th based on the same head-to-head heuristic (with a huge branching factor equal to the number of players).

Alpha-Rank is a new game-theoretic evaluation metric for ranking players in a game. Game-theoretic evaluation tools use game-theory (hence the name) to measure players by taking into account *non-transitivity*. Non-transitivity refers to the possibility that player A > B and B > C and yet C > A. The simplest example of this is the game rock paper scissors, which is entirely non-transitive. 

Most metrics (like those based on tournament placements) assume that games are roughly transitive. For example, they assume that if player A places higher than player B in a tournament, then player A is better than player B. This is not necessarily true, and in fact player A can lose to B and still win the tournament in a double elimination bracket. This happens every time someone wins from the losers bracket, and many other times throughout every tournament.

Alpha-Rank creates a meta-game of players and uses all of the head-to-head counts between players to determine who is the best. It measures each player's "value" according to who they can beat in a head-to-head, weighted according to their opponent's value (also calculated in the same way from head-to-heads). (i.e. beating Hugs86 gives you less value than beating Zain). Also, since Alpha-Rank analyzes overall winrates, it has no recency bias.


# Usage
To rank smash players using data.csv, you can use the command:
```
python3 alpha_smash.py
```

To visualize a sweep over the alpha hyperparameter and the dynamics of the metagame with n players you can use the following options:

```
python3 alpha_smash.py --alphasweep --n_network 10
```

For more info, use:
```
python3 alpha_smash.py --help
```


# How to Interpret the Results
Imagine that you are having a competition with another person, and you each get to choose one smash pro as your champion. Let's say you play this game over and over. How would you decide who to pick? You could always choose the player with the highest overall head-to-head winrate (Leffen). However, if your opponent picked Mango, you would lose, because Mango wins that head-to-head in 2022. Therefore, there's a meta-game of choosing strong players, but also varying your choice enough to avoid being predictable. Clearly some players are stronger (IBDW wins more head-to-heads than Axe), but each player can win some matchups. 
The value in parentheses in the rankings below represents the percent of time that a particular player would be selected by the optimal strategy for this game. The players are ranked in order of who has the highest value, in essence, who is picked the most often in this imaginary meta-game.

**Note: The bottom 20-30 players are included because of their effect on the top players, but the rankings assigned to them by Alpha-Rank are inherently less accurate due to the nature of Alpha-Rank and smash competition (high-level players interact more than low-level players). Please don't read too closely into the lower ranks. We would need to include more players to accurately rank them.**

**TL;DR** If you could choose one pro to fight for you, Alpha-Rank measures how often you should pick each player. This is based on their head-to-head winrates weighted according to the strength of the opponent in each head-to-head.


# RESULTS: 2022 Ranking (So Far)
```
Player          Rank         Score
------          ----         -----

Zain            1            0.1057
iBDW            2            0.1055
aMSa            3            0.0979
Jmook           4            0.0892
Mang0           5            0.0713
Hungrybox       6            0.0648
Plup            7            0.0391
SluG            8            0.0346
Leffen          9            0.0337
S2J             10           0.0323
moky            11           0.0318
Fiction         12           0.0314
Axe             13           0.0239
Joshman         14           0.0227
lloD            15           0.0169
Pipsqueak       16           0.0151
Krudo           17           0.0136
KoDoRiN         18           0.0128
null            19           0.0127
Ginger          20           0.0119
Aklo            21           0.0105
SFAT            22           0.0100
n0ne            23           0.0084
Lucky           24           0.0079
Polish          25           0.0067
2saint          26           0.0065
Spark           27           0.0056
Soonsay         28           0.0055
Magi            29           0.0054
Salt            30           0.0053
Zuppy           30           0.0053
Mekk            31           0.0047
The SWOOPER     32           0.0045
bobby big ballz 33           0.0044
Jflex           33           0.0044
Wizzrobe        34           0.0037
Suf             35           0.0036
Bbatts          36           0.0034
Zamu            37           0.0032
Skerzo          38           0.0030
Ben             38           0.0030
Smashdaddy      39           0.0023
KJH             40           0.0021
Frenzy          41           0.0017
Medz            42           0.0016
Aura            43           0.0013
Panda           43           0.0013
Professor Pro   44           0.0011
Albert          45           0.0009
Swift           46           0.0008
Solobattle      46           0.0008
Chem            47           0.0007
Faceroll        47           0.0007
Kalamazhu       47           0.0007
Eddy Mexico     48           0.0006
Logan           49           0.0005
Colbol          49           0.0005
Trif            49           0.0005
Gahtzu          50           0.0004
Ice             51           0.0000
Nicki           51           0.0000
```

# Interesting Findings
* Zain and IBDW are effectively tied for Rank 1. Either of them could easily edge out #1 by winning the upcoming tournaments.
* The top 6 players are clearly separated from the rest. Zain, IBDW, aMSa, JMook, Mang0, and HungryBox have significantly more value than Plup, the next highest player.
* While top 6 is clearly above the rest, each player in that tier has a noticeable drop in value from the previous rank, indicating a high level of confidence in the ordering of top 6.
* The next 5 players (rank 7 - 12) Plup, Slug, Leffen, S2J and Fiction are all close to each other, and noticeably higher valued than rank 13 and below. We see a clear Top 6 tier and Top 12 tier in these results.
* The rankings become less well definined the farther down the list we go. There are far more ties below rank 30. I recommend not reading into ranks below 30 too much, as they are clearly less accurate.
* I included Ice and Nicki because they have 0 tournament sets this year (according to my data) to demonstrate that the attendance bonus causes these players to be ranked last.
* It is possible for top players to win so many matchups that weaker players have a value of 0.0 in the meta-game. The fact that all players (aside from Nikki and Ice who have 0 attendance) have some value in the meta-game is a good sign for the health of the game.


# Data Collection
The data used for these calculations can be found here: [https://docs.google.com/spreadsheets/d/1e08K2EzNQWR3Q4T5ZWVd2bP53nEg_rBqUf_Clj0muHc/](https://docs.google.com/spreadsheets/d/1e08K2EzNQWR3Q4T5ZWVd2bP53nEg_rBqUf_Clj0muHc/)

Data includes all offline super major, major, invitational and tournaments that occurred so far in 2022 (up to and including Apex 2022).


# Matchup Value Calculation
To use Alpha-Rank, you need to assign a value to each matchup. I implemented two methods, linear and scalar weighting. These results use linear weighting, but scalar does not result in noticeably different rankings. Using the linear method, each matchup is assigned the value equal to the players wins - minus their losses. For example, Mango - IBDW is a 5-1 matchup. Mango gets the value 4 for this matchup while IBDW gets the value -4.

# Attendance Bonus
Without any modification, the value calculation above heavily favors low attendance because a 0-0 record against a top player is better than a losing record. To account for this, all 0-0 matchups are assigned a value based on the relative attendance of each player.
For any matchup without data, we set the value to $(s_A - s_B) / (s_A + s_B)$ where $s_A$ and $s_B$ are the number of sets played this year by player A and B respectively.
E.g. For $s_A = 10$ and $s_B = 0$, the bonus is 1, for $ s_A = s_B = 10$, the bonus is 0.
Since this only applies to unplayed matchups, it is not possible for players to inflate their value against anyone they have played this year by simply attending more tournaments.


# Alpha Hyperparameter Sweep
Alpha-Rank has one hyperparameter, alpha. This controls how many levels of couterplay there are in the meta-game. Think of this as how many steps ahead you imagine in Rock Paper Scissors (i.e. He thinks I think that he thinks that I think that he's going to choose Paper, so I'll choose Rock). At an infinite planning horizon, there is a fixed point that represents the distribution of players in a meta game with infinite adaptation (the "true" meta-game). Using smaller alpha values gives you a meta-game with less "planning-ahead". Here is a sweep over the values of alpha which shows how the distribution changes as you increase alpha. We always use the highest possible value of alpha for actual rankings.

![Alpha sweep](https://github.com/RyanNavillus/AlphaSmash/blob/main/Smash_sweep.png)

Interestingly Mango appears to beat many players in the uniform meta-game. However, as the distribution shifts to favor Amsa, Mango's value decreases because that's a losing matchup for him. The same is true for Leffen and Zain to a lesser degree. Likewise Plup becomes more popular of a choice as Amsa's value increases because of his 1-0 record against Amsa.


# Equillibrium Network
The following network shows the rate at which you would switch to a partiular player when facing off against another player. For example, the arrow pointing from Mang0 to aMSa labeled 50 (the max value) indicates that if you are currently choosing Mang0 as your champion, then you would switch to choosing aMSa as fast as possible. We only visualize the top 12 here for visual clarity, and as noted above, top 12 appears to be in a separate tier above the rest according to Alpha-Rank.

![Alpha Network](https://github.com/RyanNavillus/AlphaSmash/blob/main/Smash_network.png)

This shows you where players are getting value and losing value in the meta-game. For example, IBDW is getting value from most players because he has much more favorable head to heads. However, he loses some value Moky, Leffen, and Mang0 because he has losing records against them.

This also gives you a good intuition for how Alpha-Rank works. Value flows into players from their strong matchups and out from their weak matchups. If you consider all of these matchups at once, eventually this reaches an equillibrium where each people choose each node as their strategy a certain percent of the time, and there's a certain flow rate between each node.


# Testing Hypothetical Results
You can modify data.csv and re-run AlphaSmash to test hypothetical results. For example, how would JMook be ranked if he had an even matchup against HBox? What if Mang0 wins the Smash World Tour Championshipsi, beating Amsa, Zain, and Fiction? What if Leffen never lost to Lovage in 2017?
