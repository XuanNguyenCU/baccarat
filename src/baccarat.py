"""
baccarat.py

Exact-enumeration Baccarat odds calculator for N-deck shoes (6 in particular for now).

Usage:
    python3 baccarat.py
"""


import itertools
from dataclasses import dataclass
from functools import lru_cache
from math import perm
from collections import defaultdict
from typing import Tuple, Dict

# Mapping: banker_sum ⇒ set of "player third card values" that make banker draw
#
# Card values are Baccarat point values (0 = 10/J/Q/K, 1‑9 = ace‑nine).
# set(range(10))  means "draw for ANY possible third card".
# Empty set       means "NEVER draw" (banker must stand).
#
# Reference ("common draw rules" used in casinos world‑wide):
#   Banker total 0‑2 : always draw
#                3   : draw unless player's 3rd card is 8
#                4   : draw if player's 3rd card is 2‑7
#                5   : draw if player's 3rd card is 4‑7
#                6   : draw if player's 3rd card is 6‑7
#                7   : always stand
#                8‑9 : "natural" - Both hands stand immediately
BANKER_DRAW_MAP = {
    0: set(range(10)),        # 0 ⇒ banker total 0 → always draws (any player card 0‑9)
    1: set(range(10)),        # 1 ⇒ same: banker total 1 → always draws
    2: set(range(10)),        # 2 ⇒ same: banker total 2 → always draws

    # 3 ⇒ banker draws UNLESS the player's 3rd card is an 8
    3: {0, 1, 2, 3, 4, 5, 6, 7, 9},   # (every card except 8)

    # 4 ⇒ banker draws only if player's 3rd card is 2‑7 (inclusive)
    4: {2, 3, 4, 5, 6, 7},

    # 5 ⇒ banker draws only if player's 3rd card is 4‑7
    5: {4, 5, 6, 7},

    # 6 ⇒ banker draws only if player's 3rd card is 6 or 7
    6: {6, 7},

    # 7-9 ⇒ banker always stands (never draws)
    7: set(),                 # empty set → no card value triggers a draw
    8: set(),
    9: set(),
}


@dataclass(frozen=True)
class Shoe:
    """
    Represents a Baccarat shoe composed of one or more standard 52-card decks.

    :param num_decks: Number of 52-card decks in the shoe.
    :property frequencies: A 10-tuple giving the count of each Baccarat card value in the shoe:
        - Index 0: Number of zero-point cards (10, J, Q, K) = num_decks x 4 suits x 4 ranks.
        - Indices 1-9: Number of 1-through-9 point cards = num_decks x 4 suits each.
    """
    num_decks: int

    @property
    def frequencies(self) -> Tuple[int, ...]:
        # 0‐value cards: 4 ranks × 4 suits × decks
        zeroes = self.num_decks * 4 * 4  # For 6 decks, this is equal to 96
        others = self.num_decks * 4      # For 6 decks, this is equal to 24
        return (zeroes,) + tuple(others for _ in range(9))
    

class BaccaratCalculator:
    """
    Encapsulates logic for computing Player/Banker/Tie odds and 
    the breakdown of Banker-winning outcomes in Baccarat.
    """

    def __init__(self, shoe: Shoe) -> None:
        """
        :param shoe: A Shoe instance defining how many of each Baccarat value (0-9) are in the shoe.
                     Used to weight each 6-card sequence by its exact permutation count.
        """
        self.shoe = shoe

        # 0 points corresponds to 10/J/Q/K
        # 1..9 points correspond to their face values
        self.deck = tuple(range(10))

        # Frequencies in a 6-deck shoe:
        #   - 0-value cards (10, J, Q, K): 6 decks * 4 suits * 4 ranks = 96
        #   - Each of 1..9: 6 decks * 4 suits = 24 each
        self.deck_frequency = shoe.frequencies
        
        # Final tallies of how often each outcome occurs
        self.counts: Dict[str, int] = {'player': 0, 'banker': 0, 'tie': 0}

        # For banker-winning hands, store how many ways to end up with
        # (banker_sum, player_sum)
        self.banker_breakdown: Dict[Tuple[int, int], int] = defaultdict(int)

        # Total ways all outcomes can occur
        self.total = 0
    
    @lru_cache(maxsize=None)
    def _count_permutations_of_hand(self, hand: Tuple[int, ...]) -> int:
        """
        Given a 6-card tuple (hand), return how many distinct ways
        one can draw those cards in that exact order from the shoe.

        Theory recap:
        - A Baccarat shoe is a multiset (e.g. 96 zero-value cards, 24 ones, …)
        - If a particular value i appears kᵢ times in the proposed 6-card sequence
          and the shoe still contains nᵢ copies, then there are

                P(nᵢ, kᵢ) = nᵢ! / (nᵢ - kᵢ)!

          ordered ways to draw those kᵢ cards.
        - Because draws of different ranks are independent, the total #ways is the
          product of P(nᵢ, kᵢ) over all ten ranks
            
        Process:
          1. Count how many times each card value i appears (hand_freq[i]).
          2. Check if hand_freq[i] <= deck_frequency[i]. If not, it's invalid (0).
          3. Multiply P(deck_frequency[i], hand_freq[i]) across all i.
        """
        hand_freq = [0] * 10
        
        # Count frequency of each card value in the hand
        for c in hand:
            hand_freq[c] += 1
        
        ways = 1

        # Multiply permutations for each card value
        for i in range(10):

            # Check if kᵢ (cards of rank i in this sequence) > nᵢ (remaining in the shoe)
            if hand_freq[i] > self.deck_frequency[i]:
                return 0  # Not enough copies in the shoe, exit early
            
            # Multiply by P(nᵢ, kᵢ).  When kᵢ is 0 the factor is 1.
            ways *= perm(self.deck_frequency[i], hand_freq[i])
        
        return ways

    def run_calculations(self) -> None:
        """
        Enumerate all possible 6-card permutations (with replacement) from
        the shoe, apply Baccarat drawing rules, and accumulate:

        - self.counts: total ways the final result is 'player', 'banker', or 'tie'.
        - self.banker_breakdown[(b_sum, p_sum)]:
            for banker-winners only, how many ways the Banker ends on b_sum and 
            the Player on p_sum (p_sum < b_sum).
        - self.total: grand total of all valid sequences examined.
        """

        deck = self.deck
        counts = self.counts
        breakdown = self.banker_breakdown
        
        # every 6‑tuple of card values
        for hand in itertools.product(deck, repeat=6):
            # Compute how many ways this exact 6-card sequence can occur
            ways = self._count_permutations_of_hand(hand)
            if ways == 0:
                # Invalid sequence given the deck frequencies
                continue

            # Compute final sums
            c1, c2, c3, c4, c5, c6 = hand
            
            # Two‑card totals (mod‑10) before any draws
            player_sum = (c1 + c2) % 10
            banker_sum = (c4 + c5) % 10

            # Begin standard drawing rules:

            # Player stands if 6 or 7
            if player_sum in (6, 7):
                # Banker draws if sum <= 5
                if banker_sum <= 5:
                    banker_sum = (banker_sum + c6) % 10
            # Otherwise if player_sum <= 5 and banker_sum < 8, player draws c3
            elif player_sum <= 5 and banker_sum < 8:
                player_sum = (player_sum + c3) % 10

                # Banker draw rules, using the mapping for speed
                # only bother if banker_sum <= 6
                if banker_sum <= 6 and c3 in BANKER_DRAW_MAP[banker_sum]:
                    banker_sum = (banker_sum + c6) % 10

            # Determine outcome
            if player_sum > banker_sum:
                counts['player'] += ways
            elif banker_sum > player_sum:
                counts['banker'] += ways
                breakdown[(banker_sum, player_sum)] += ways
            else:
                counts['tie'] += ways

        # Store grand total for later probability reporting
        self.total = counts['player'] + counts['banker'] + counts['tie']

    def print_results(self) -> None:
        """
        Print outcomes, probabilities, and a breakdown of banker wins only!

        Output format:
        1. For each possible final Banker total 1-9:
            - List every Player total that loses to that Banker total.
            - Show how many weighted sequences produce that score line and
            what fraction of all sequences that represents.

        2. Grand totals of:
            • Banker wins
            • Player wins
            • Ties
            • Overall number of sequences examined

        3. Corresponding probabilities (relative frequencies).
        """
        b_wins = self.counts['banker']
        p_wins = self.counts['player']
        ties = self.counts['tie']
        total = self.total

        # Print banker wins breakdown by banker sum
        for b_sum in range(1, 10):  # Banker totals 1‑9 (0 cannot win)
            total_for_b_sum = 0

            # Only player totals STRICTLY LESS than banker_total can be losses
            for p_sum in range(b_sum):
                total_for_b_sum += self.banker_breakdown[(b_sum, p_sum)]
            
            if total_for_b_sum > 0:
                print(f"=== Banker final point {b_sum} ===")
                sub_total = 0
                for p_sum in range(b_sum):
                    cnt = self.banker_breakdown[(b_sum, p_sum)]
                    
                    if cnt > 0:  # skip rows that never occur
                        sub_total += cnt
                        print(f"  vs. Player final point {p_sum}: {cnt:,} ways ({cnt/total:.4%})")

                pct = sub_total / total
                print(f"  Total ways of Banker winning with {b_sum} points: {sub_total:,} ways ({pct:.4%})\n")

        # Grand totals
        print(f"With a shoe of {self.shoe.num_decks}...")
        print(f"Total ways Banker can win:    {b_wins:,}")
        print(f"Total ways Player can win:    {p_wins:,}")
        print(f"Total ways for a tie:         {ties:,}")
        print(f"Total overall possibilities:  {total:,}\n")

        # Probabilities
        banker6 = sum(self.banker_breakdown[(6, p)] for p in range(6))
        banker_other = self.counts['banker'] - banker6

        print(f"P(Player):                      {p_wins / total:.4%}.")
        print(f"P(Banker):                      {b_wins / total:.4%}.")
        print(f"  ↳ of which P(Banker @6):        {banker6 / total:.4%}")
        print(f"  ↳ of which P(Banker @other):    {banker_other / total:.4%}")
        print(f"P(Tie):                         {ties / total:.4%}.\n")


def main():
    """
    Instantiate the BaccaratCalculator with default 6-deck frequencies and
    run the calculations, then print the results.
    """
    shoe = Shoe(num_decks=6)
    calc = BaccaratCalculator(shoe)

    calc.run_calculations()
    calc.print_results()

if __name__ == "__main__":
    main()
