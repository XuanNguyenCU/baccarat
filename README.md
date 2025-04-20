# Baccarat (6 Decks)

Under the `src` folder, there is a `baccarat.py` file that calculates the probabilities that Banker wins with 6 points, Banker wins with other points, Player wins, and a Tie in the game Baccarat for N-deck shoes (default 6 decks)

---

**Table of Contents:**
1. [Overview](#overview)  
2. [Data Structures](#data-structures)  
3. [Helper Functions](#helper-functions)  
4. [Final Probabilities](#final-probabilities)  

---

## Authors

- Jerick Liu (@jerickliu)
- Omar Khattab (@okhat1)
- Xuan Nguyen (@XuanNguyenCU)

---

## Overview

This program performs an **exact-enumeration** of all possible Baccarat hands in a **six-deck shoe**. It computes:

- Player win  
- Banker win (with total = 6)  
- Banker win (with total ≠ 6)  
- Tie  

Drawing rules and card frequencies are modeled precisely according to standard Baccarat.

---

## Data Structures

1. **`BANKER_DRAW_MAP`**  
   A constant mapping from a Banker’s two-card total (0–9) to the set of Player third-card values that will cause the Banker to draw.

2. **`Shoe` dataclass**  
   Represents the composition of the shoe.  
   - `num_decks`: number of 52-card decks.  
   - `frequencies` property: returns a 10-tuple of counts for card values 0–9.

3. **Calculator Attributes**  
   - `deck`: tuple of card values, `tuple(range(10))`.  
   - `deck_frequency`: obtained from `shoe.frequencies`, the counts for each value.  
   - `counts`: dict tracking totals for `'player'`, `'banker'`, and `'tie'`.  
   - `banker_breakdown`: defaultdict mapping `(banker_sum, player_sum)` → number of ways.  
   - `total`: grand total of all valid sequences examined.

---

## Helper Functions

### `_count_permutations_of_hand(hand)`  
Calculates ordered ways to draw a specific 6-card tuple from the shoe using `math.perm` for each distinct card value, with results cached via `@lru_cache`.

```python
# Counts ordered draws for a given hand tuple
def _count_permutations_of_hand(self, hand: Tuple[int, ...]) -> int:
    ...
```
  
### `run_calculations()`  
1. Enumerates all 6-tuples via `itertools.product(deck, repeat=6)`  
2. For each hand:  
   - Compute `ways` = `_count_permutations_of_hand(hand)`  
   - Skip if `ways == 0`  
   - Apply Baccarat drawing rules (mod 10 arithmetic + `BANKER_DRAW_MAP`)  
   - Update `self.counts` and `self.banker_breakdown`  
3. Store grand total in `self.total`.

```python
def run_calculations(self) -> None:
    ...
```

### `print_results()`  
Prints:  
- Detailed Banker wins breakdown by final Banker total and losing Player totals.  
- Grand totals of Banker wins, Player wins, ties, and overall sequences.  
- Relative probabilities, including sub‑breakdown for Banker total = 6 vs. other.

```python
def print_results(self) -> None:
    ...
```

### `main()`  
Instantiates `Shoe(num_decks=6)` and `BaccaratCalculator`, runs calculations, and prints results.

```python
if __name__ == "__main__":
    main()
```

---

## Final Probabilities

The program’s final sums can be verified against known theoretical results (also matches the results from https://wizardofodds.com/games/baccarat/calculator/ for the 6 decks composition).  

This is the output when running the program `baccarat.py`:  

```
=== Banker final point 1 ===
  vs. Player final point 0: 4,264,128,824,832 ways (0.4852%)
  Total ways of Banker winning with 1 points: 4,264,128,824,832 ways (0.4852%)

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

With a shoe of 6...
Total ways Banker can win:    403,095,751,234,560
Total ways Player can win:    392,220,492,728,832
Total ways for a tie:         83,552,962,932,288
Total overall possibilities:  878,869,206,895,680

P(Player):                      44.6279%.
P(Banker):                      45.8653%.
  ↳ of which P(Banker @6):        5.3844%
  ↳ of which P(Banker @other):    40.4808%
P(Tie):                         9.5069%.
```
