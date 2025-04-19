# Baccarat (6 Decks)

Under the `src` folder, there is a `baccarat_six_decks.py`   file that calculates the probabilities that Banker wins with 6 points, Banker wins with other points, Player wins, and a Tie in the the game Baccarat using six decks.

---

**Table of Contents:**
1. [Overview](#overview)  
2. [Data Structures](#data-structures)  
3. [Helper Functions](#helper-functions)  
4. [\`bankerWinsBreakdown\` Function](#bankerwinsbreakdown-function)  
5. [Final Probabilities](#final-probabilities)  

---

## Overview

This program analyzes Baccarat outcomes using **six decks** of standard playing cards. We define:

- **Card values** in Baccarat: 
  - 10, J, Q, K are collectively considered “0 points.”  
  - Aces and 2–9 have face values 1 through 9, respectively.  
- **Deck frequency**: for 6 decks, there are 
  - \(6 * 4 * 4 = 96\) cards that are 0 points (10/J/Q/K),  
  - \(6 * 4 = 24\) cards for each of 1–9.  

To simulate the dealing of a Baccarat hand, we consider permutations of length 6 (the maximum needed in dealing a full hand with possible third cards). We then count how many representations (ways to deal) each permutation has, based on how many times each value is available in the combined 6 decks.

---

## Data Structures

1. **\`deck\`:**  
   ```python
   deck = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   ```
   - We list each possible card *value* in Baccarat.  
   - \`0\` stands for 10/J/Q/K cards; \`1\` stands for Ace, \`2\` for 2, and so on up to \`9\`.

2. **\`deckFrequency\`:**  
   ```python
   deckFrequency = [96, 24, 24, 24, 24, 24, 24, 24, 24, 24]
   ```
   - An array where the index corresponds to the card’s value and the stored integer is **how many copies** of that value exist in 6 decks.  
   - Specifically:  
     - deckFrequency[0] = 96 (the number of 10/J/Q/K cards).  
     - deckFrequency[1] ... deckFrequency[9] = 24 each (A–9).

3. **\`uniqueHands\`:**  
   ```python
   uniqueHands = list(itertools.product(deck, repeat=6))
   ```
   - Generate **all 6-length permutations (with replacement)** of the values 0..9.  
   - Each element in `uniqueHands` is a tuple of 6 values, e.g. `(0, 3, 7, 0, 0, 2)`.

---

## Helper Functions

### `add(cardOne, cardTwo)` Function

**Explanation**  
1. **`add`** is a helper that sums two card values in **mod 10**.  


### `outcome(hand)` Function

**Explanation**  
1. Extract the cards from the 6-tuple.
    - `c1, c2` → Player’s first two cards,
    - `c4, c5` → Banker’s first two cards,
    - `c3, c6` → Potential third cards for Player (c3) and Banker (c6).
2. Compute initial sums using the helper `add` function (which sums values mod 10).
3. Apply Baccarat’s drawing rules to see if the Player or Banker takes a third card.
4. Compare final sums and return the outcome.


### `repCount(hand)` Function

**Explanation**  
- Because our hand is something like \`(c1, c2, ..., c6)\) *by value*, we must figure out how many actual “real-world” ways can produce that specific combination of values.  
- We copy the list of frequencies (so we don’t mutate the original).  
- For each card value **c** in the hand, we:  
  1. Multiply our running count by the number of remaining copies of **c** (e.g., if c=0, initially there might be 96 available).  
  2. Decrement that copy’s availability by 1.  

By the end of the loop, \`count\` is the total number of ways to draw that exact sequence of values from the shoe.


### `calculate_odds()` Function

**Explanation**  
1. Initialize a dictionary `counts` to track totals for 'player', 'banker', and 'tie'.
2. Iterate through all possible 6-card permutations stored in `uniqueHands`. Each hand is a 6-tuple of values (0 through 9).
3. Use `outcome(hand)` to see who wins the hand: 'player', 'banker', or 'tie'.
4. Use `repCount(hand)` to find out how many real-world combinations correspond to that particular 6-tuple of card values.
5. Accumulate the counts into the `counts` dictionary.
6. Return the dictionary that shows the total number of ways for each final outcome across all 6-card combinations.

### `final_sums(hand)` Function

**Explanation**  
1. We destructure the 6-card “hand” into \`c1..c6\`.  
2. We compute *initial* Player and Banker sums from their first two cards.  
3. We apply Baccarat’s standard drawing rules:  
   - If Player has exactly 6 or 7, the Player does NOT draw a third card. The Banker then draws only if the Banker’s sum is <= 5.  
   - Otherwise, if Player has <= 5 while Banker has < 8, the Player draws a third card. The Banker’s draw depends on the value of the Player’s third card (c3).  
4. The function returns **the final sums** (\`playerSum, bankerSum\`).


---

## `bankerWinsBreakdown` Function

**Explanation**  
1. We use `defaultdict(int)` to map `(bankerSum, playerSum)` → **number of ways**.  
2. For every 6-card combination in \`uniqueHands\`, we:  
   - Get the final sums for Player and Banker using \`final_sums(hand)\`.  
   - If \`bSum > pSum\`, the Banker “wins,” so we increment our dictionary entry by \`repCount(hand)\`.  
3. We sum all the dictionary values to see how many total ways the Banker can win.  
4. Finally, we print it out grouped by Banker’s final sum from 1..9.  
5. The function returns the dictionary for further use or analysis.

---

## Final Probabilities
The program’s final sums can be verified against known theoretical results (also matches the results from https://wizardofodds.com/games/baccarat/calculator/ for the 6 decks composition).  

This is the output when running the program `baccarat_six_decks.py`:

```
Total ways Banker can win: 403,095,751,234,560

=== Banker final point 1 ===
  vs. Player final point 0: 4,264,128,824,832 ways (0.4852%)
  Total ways of Banker winning with 1 point: 4,264,128,824,832 ways (0.4852%)

=== Banker final point 2 ===
  vs. Player final point 0: 4,245,546,825,216 ways (0.4831%)
  vs. Player final point 1: 3,597,643,123,200 ways (0.4093%)
  Total ways of Banker winning with 2 points: 7,843,189,948,416 ways (0.8924%)

=== Banker final point 3 ===
  vs. Player final point 0: 4,733,871,681,024 ways (0.5386%)
  vs. Player final point 1: 4,083,234,977,664 ways (0.4646%)
  vs. Player final point 2: 4,003,057,580,544 ways (0.4555%)
  Total ways of Banker winning with 3 points: 12,820,164,239,232 ways (1.4587%)

=== Banker final point 4 ===
  vs. Player final point 0: 8,079,496,680,960 ways (0.9193%)
  vs. Player final point 1: 7,140,240,693,504 ways (0.8124%)
  vs. Player final point 2: 6,779,319,856,128 ways (0.7714%)
  vs. Player final point 3: 6,707,806,239,744 ways (0.7632%)
  Total ways of Banker winning with 4 points: 28,706,863,470,336 ways (3.2663%)

=== Banker final point 5 ===
  vs. Player final point 0: 8,111,994,292,224 ways (0.9230%)
  vs. Player final point 1: 7,178,458,169,088 ways (0.8168%)
  vs. Player final point 2: 7,546,967,891,712 ways (0.8587%)
  vs. Player final point 3: 7,942,347,168,768 ways (0.9037%)
  vs. Player final point 4: 7,349,105,228,544 ways (0.8362%)
  Total ways of Banker winning with 5 points: 38,128,872,750,336 ways (4.3384%)

=== Banker final point 6 ===
  vs. Player final point 0: 8,534,981,039,616 ways (0.9711%)
  vs. Player final point 1: 7,143,806,230,272 ways (0.8128%)
  vs. Player final point 2: 7,517,113,547,904 ways (0.8553%)
  vs. Player final point 3: 7,911,355,506,048 ways (0.9002%)
  vs. Player final point 4: 8,048,708,547,840 ways (0.9158%)
  vs. Player final point 5: 8,166,265,159,680 ways (0.9292%)
  Total ways of Banker winning with 6 points: 47,322,230,031,360 ways (5.3844%)

=== Banker final point 7 ===
  vs. Player final point 0: 9,500,595,038,208 ways (1.0810%)
  vs. Player final point 1: 8,103,396,984,192 ways (0.9220%)
  vs. Player final point 2: 8,012,593,191,168 ways (0.9117%)
  vs. Player final point 3: 7,952,674,940,928 ways (0.9049%)
  vs. Player final point 4: 8,089,432,326,144 ways (0.9204%)
  vs. Player final point 5: 8,207,240,161,536 ways (0.9338%)
  vs. Player final point 6: 17,742,879,436,032 ways (2.0188%)
  Total ways of Banker winning with 7 points: 67,608,812,078,208 ways (7.6927%)

=== Banker final point 8 ===
  vs. Player final point 0: 14,936,001,431,040 ways (1.6995%)
  vs. Player final point 1: 10,163,184,406,272 ways (1.1564%)
  vs. Player final point 2: 10,050,313,865,472 ways (1.1436%)
  vs. Player final point 3: 10,005,826,558,464 ways (1.1385%)
  vs. Player final point 4: 10,124,265,517,056 ways (1.1520%)
  vs. Player final point 5: 10,260,972,986,112 ways (1.1675%)
  vs. Player final point 6: 13,700,396,749,824 ways (1.5589%)
  vs. Player final point 7: 13,904,546,379,264 ways (1.5821%)
  Total ways of Banker winning with 8 points: 93,145,507,893,504 ways (10.5983%)

=== Banker final point 9 ===
  vs. Player final point 0: 15,000,473,136,384 ways (1.7068%)
  vs. Player final point 1: 10,204,053,873,408 ways (1.1610%)
  vs. Player final point 2: 10,091,313,287,424 ways (1.1482%)
  vs. Player final point 3: 10,047,103,983,360 ways (1.1432%)
  vs. Player final point 4: 10,164,870,715,392 ways (1.1566%)
  vs. Player final point 5: 10,308,608,006,400 ways (1.1729%)
  vs. Player final point 6: 13,755,518,161,920 ways (1.5651%)
  vs. Player final point 7: 13,961,821,697,280 ways (1.5886%)
  vs. Player final point 8: 9,722,219,136,768 ways (1.1062%)
  Total ways of Banker winning with 9 points: 103,255,981,998,336 ways (11.7487%)

Total ways Player can win: 392,220,492,728,832
Total ways for a tie: 83,552,962,932,288
Total overall possibilities: 878,869,206,895,680

Player has a 44.6279% chance of winning.
Banker has a 45.8653% chance of winning.
They have a 9.5069% chance of tieing.
```
