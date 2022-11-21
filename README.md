# Using AlphaRank to rank Smash pros
This is a simple script that uses DeepMind's [AlphaRank algorithm](https://arxiv.org/abs/1903.01373) to rank the top 10 Super Smash Bros Melee players for 2022 (so far). (Fair warning: this paper is extremely complicated, I've attempted to explain the core concepts in this README).

AlphaRank is a new game-theoretic evaluation metric for ranking players in a game. Game-theoretic evaluation tools use game-theory (hence the name) to measure players by taking into account *non-transitivity*. Non-transitivity refers to the possibility that player A > B and B > C and yet C > A. The best example of this is the game rock paper scissors, which is entirely non-transitive. 

Most other metrics assume that games are roughly transitive. For example, they assume that if player A places higher than player B in a tournament, then player A is better than player B. This is not necessarily true, and in fact player A can lose to B and still win the tournament in a double elimination bracket. This happens every time someone makes a losers run.

AlphaRank creates a meta-game of players and uses all of the head-to-head counts between players to determine who is the best. It measures each player's "value" according to who they can beat in a head-to-head, weighted according to their opponent's value. (i.e. beating Hugs86 gives you less value than beating Zain). 


# How to interpret the results
Imagine that you are having a competition with another person, and you each get to choose one smash pro as your champion. Let's say you play this game over and over. How would you decide who to pick? You could always choose the player with the highest overall head-to-head winrate (Leffen). However, if your opponent picked Mango, you would lose, because Mango wins that head-to-head in 2022. Therefore, there's a meta-game of choosing strong players, but also varying your choice enough to avoid being predictable. Clearly some players are stronger (IBDW wins more head-to-heads than Axe), but each player can win some matchups. The value in parentheses represents the percent of time that a particular player would be selected in the optimal strategy for this game. The players are ranked in order of who has the highest value, in essence, who is picked the most often in this imaginary meta-game.


# 2022 (up to Apex 2022) Ranking

1. Amsa (0.234)
2. IBDW (0.200)
3. Mango (0.131)
4. Leffen (0.106)
5. Plup (0.085)
6. Jmook (0.062)
7. Hbox (0.015)
8. Wizzrobe (0.008)
9. Axe (0.001)

# Data collection
Thanks to ASAP_Hari on twitch for collecting most of the data that I used. The winrates used in this project come from liquipedia. I used data from offline-only supermajor, major, and invitational tournaments held Jan 1 - November 21, 2022 (including Apex 2022).

# Winrate calculation

