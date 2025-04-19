import itertools
from collections import defaultdict

# 0 points corresponds to 10/J/Q/K cards
# 1...9 points correspond to their face values
deck = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 0-value cards (10, J, Q, K): 6 decks * 4 suits * 4 such cards = 96
# 1...9-value cards: 6 decks * 4 suits = 24 each
deckFrequency = [96, 24, 24, 24, 24, 24, 24, 24, 24, 24]

# Generate all 6-length permutations (with replacement)
uniqueHands = list(itertools.product(deck, repeat=6))


# Adding points
def add(cardOne, cardTwo):
    return (cardOne + cardTwo) % 10


# Determining who wins or if a tie occurs
def outcome(hand):
    c1, c2, c3, c4, c5, c6 = hand
    playerSum = add(c1, c2)
    bankerSum = add(c4, c5)

    # Player rule
    if playerSum == 6 or playerSum == 7:
        if bankerSum <= 5:
            bankerSum = add(bankerSum, c6)

    elif playerSum <= 5 and bankerSum < 8:
        playerSum = add(playerSum, c3)

        # Banker rule
        if bankerSum <= 2:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 3 and c3 in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 4 and c3 in [2, 3, 4, 5, 6, 7]:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 5 and c3 in [4, 5, 6, 7]:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 6 and c3 in [6, 7]:
            bankerSum = add(bankerSum, c6)

    if playerSum > bankerSum:
        return 'player'
    
    elif bankerSum > playerSum:
        return 'banker'
    
    return 'tie'


def repCount(hand):
    """
    Given a 6-card value tuple (e.g. (0, 3, 7, 2, 8, 9)),
    returns how many distinct ways there are to draw that exact sequence of values from the shoe.
    """
    copyFreq = deckFrequency.copy()
    count = 1
    for c in hand:
        count *= copyFreq[c]
        copyFreq[c] -= 1
    return count


# Determining the total number of ways for Player winning, Banker winning, and tie
def calculate_odds():
    counts = {'player': 0, 'banker': 0, 'tie': 0}
    for hand in uniqueHands:
        result = outcome(hand)
        count = repCount(hand)
        counts[result] += count
    return counts


def final_sums(hand):
    """
    Given a 6-card hand (c1..c6),
    return (final_player_sum, final_banker_sum) under standard Baccarat drawing rules.
    """
    c1, c2, c3, c4, c5, c6 = hand

    # Initial 2-card sums
    playerSum = add(c1, c2)
    bankerSum = add(c4, c5)

    # Determine who draws 3rd card
    if playerSum == 6 or playerSum == 7:

        # Player stands on 6/7
        if bankerSum <= 5:
            bankerSum = add(bankerSum, c6)

    elif playerSum <= 5 and bankerSum < 8:

        # Player draws third card
        playerSum = add(playerSum, c3)

        # Apply Banker’s draw rules
        if bankerSum <= 2:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 3 and c3 in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 4 and c3 in [2, 3, 4, 5, 6, 7]:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 5 and c3 in [4, 5, 6, 7]:
            bankerSum = add(bankerSum, c6)
        elif bankerSum == 6 and c3 in [6, 7]:
            bankerSum = add(bankerSum, c6)
    return (playerSum, bankerSum)


def bankerWinsBreakdown():
    """
    Returns a dictionary keyed by (bankerSum, playerSum) with the number of ways the Banker can end up with that final sum
    while beating the Player's sum (bankerSum > playerSum).

    Also prints a summary of the total ways the Banker can win, grouped by Banker’s final sum.
    """
    breakdown = defaultdict(int)
    counts = calculate_odds()
    total = sum(counts.values())

    for hand in uniqueHands:
        pSum, bSum = final_sums(hand)
        if bSum > pSum:
            breakdown[(bSum, pSum)] += repCount(hand)

    total_banker_wins = sum(breakdown.values())
    print(f"Total ways Banker can win: {total_banker_wins:,}")

    # For each final Banker sum, print a sub-list
    for bSum in range(1,10):
        # Gather all pSum < bSum
        sum_for_bSum = 0
        for pSum in range(bSum):
            sum_for_bSum += breakdown[(bSum, pSum)]
        if sum_for_bSum > 0:
            print(f"\n=== Banker final point {bSum} ===")
            tcount = 0
            for pSum in range(bSum):
                count = breakdown[(bSum, pSum)]
                if count > 0:
                    tcount += count
                    print(f"  vs. Player final point {pSum}: {count:,} ways ({count / total:.4%})")
            print(f"  Total ways of Banker winning with {bSum} points: {tcount:,} ways ({tcount / total:.4%})")
    return breakdown


def main():
    bankerWinsBreakdown()
    counts = calculate_odds()
    player_winning_num = counts['player']
    banker_winning_num = counts['banker']
    tie_num = counts['tie']
    total = sum(counts.values())
    print()
    print(f"Total ways Player can win: {player_winning_num:,}")
    print(f"Total ways for a tie: {tie_num:,}")
    print(f"Total overall possibilities: {total:,}")
    print()
    print(f"Player has a {player_winning_num / total:.4%} chance of winning.")
    print(f"Banker has a {banker_winning_num / total:.4%} chance of winning.")
    print(f"They have a {tie_num / total:.4%} chance of tieing.")


if __name__ == "__main__":
    main()
