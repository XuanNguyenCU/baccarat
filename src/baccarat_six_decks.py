import itertools

# 0 points corresponds to 10/J/Q/K cards
# 1...9 points correspond to their face values
deck = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 0-value cards (10, J, Q, K): 6 decks * 4 suits * 4 such cards = 96
# 1...9-value cards: 6 decks * 4 suits = 24 each
deckFrequency = [96, 24, 24, 24, 24, 24, 24, 24, 24, 24]

# Generate all 6-length permutations (with replacement)
uniqueHands = list(itertools.product(deck, repeat=6))

def add(cardOne, cardTwo):
    return (cardOne + cardTwo) % 10

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
    copyFreq = deckFrequency.copy()
    count = 1
    for c in hand:
        count *= copyFreq[c]
        copyFreq[c] -= 1
    return count

def calculateOdds():
    counts = {'player': 0, 'banker': 0, 'tie': 0}
    for hand in uniqueHands:
        result = outcome(hand)
        count = repCount(hand)
        counts[result] += count
    return counts

def main():
    counts = calculateOdds()
    player_winning_num = counts['player']
    banker_winning_num = counts['banker']
    tie_num = counts['tie']
    total = player_winning_num + banker_winning_num + tie_num

    print("Player wins:", player_winning_num)
    print("Banker wins:", banker_winning_num)
    print("They tie:", tie_num)
    print("The total possibilities are:", total)

    print()
    print(f"Player has a {player_winning_num / total:.4%} chance of winning.")
    print(f"Banker has a {banker_winning_num / total:.4%} chance of winning.")
    print(f"They have a {tie_num / total:.4%} chance of tieing.")


if __name__ == "__main__":
    main()
