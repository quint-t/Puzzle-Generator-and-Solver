# Puzzle Generator and Puzzle Solver

The repository contains two **independent** Python files:
1. `generator_example.py` — with an example of generating a puzzle.
2. `solver_example.py` — with an example of solving three puzzles (see below).

Requirements: Python 3.11.

## Puzzle Generator

Generator advantages:
1. Uniform generation.
2. Any number of attributes up to 10.
3. Any number of objects up to 10.
4. 20 levels.
5. Minimization of the number of conditions with setting a timeout for minimization.
6. One solution always.

```commandline
python3 generator_example.py
```

Program possible output (**max level with minimization**, 4 objects with 4 attributes):
```
.:: Puzzle ::.
Beverage: coffee, milk, mirinda, tea
Job: chef, doctor, firefighter, lawyer
Pet: bird, cat, dog, turtle
Transport: bike, boat, motorbike, train
 1. Pet:turtle is not to the right of Beverage:coffee
 2. Pet:cat == Job:lawyer or Pet:cat == Beverage:mirinda, but not both
 3. Job:chef and Beverage:mirinda have different parity positions
 4. Job:lawyer and Beverage:milk have different parity positions
 5. Transport:boat and Job:doctor have different parity positions
 6. Pet:dog is somewhere between Transport:motorbike and Job:doctor
 7. Beverage:tea is not to the left of Job:doctor
 8. Transport:bike is somewhere between Transport:train and Beverage:mirinda
 9. Transport:train is somewhere between Transport:bike and Job:lawyer
10. Pet:turtle == Transport:boat or Pet:turtle == Job:lawyer or both

.:: Answer ::.
|             |   1    |   2    |  3   |      4      |
| Beverage    | coffee | milk   | tea  | mirinda     |
| Job         | lawyer | doctor | chef | firefighter |
| Pet         | turtle | bird   | dog  | cat         |
| Transport   | boat   | train  | bike | motorbike   |
Time: 1.985000 seconds
```

### Explanation of 20 levels with relations

- L1: `A == B`: An object that has attribute A has attribute B.
- L1: `A is on the left of B`: An object with attribute A is **next** to the left of an object with attribute B (A-B).
- L1: `A is on the right of B`: An object with attribute A is **next** to the right of an object with attribute B (B-A).
- L1: `A is on the far left`: An object with attribute A is on the far left (A-...).
- L1: `A is on the far right`: An object with attribute A is on the far right (...-A).
- L1: `A is in the middle`: An object with attribute A is in the middle.
- L2: `A is between B and C`: An object with attribute A is between an object with attribute B, and an object with attribute C (any order: B-A-C, C-A-B).
- L3: `A is on the left or right of B`: An object with attribute A is **next** to the left or right of an object with attribute B (A-B or B-A).
- L3: `A is on the far left or far right`: An object with attribute A is on the far left or far right. (A-... or ...-A)
- L4: `A is in an odd position`: An object with attribute A is in an odd position (odd positions: 1, 3, 5, ...).
- L4: `A is in an even position`: An object with attribute A is in an even position (even positions: 2, 4, 6, ...).
- L5: `A is somewhere to the left of B`: An object with attribute A is **somewhere** to the left of an object with attribute B (any number of intermediates, including 0: A-...-B).
- L5: `A is somewhere to the right of B`: An object with attribute A is **somewhere** to the right of an object with attribute B (any number of intermediates, including 0: B-...-A).
- L6: `A != B`: An object that has attribute A does not have attribute B.
- L7: `A is somewhere between B and C`: An object with attribute A is **somewhere** between an object with attribute B, and an object with attribute C (any number of intermediates, including 0: B-...-A-...-C, C-...-A-...-B).
- L8: `A is not to the left of B`: An object with attribute A is not to the left of an object with attribute B.
- L8: `A is not to the right of B`: An object with attribute A is not to the right of an object with attribute B.
- L9: `A and B have different parity positions`: An object with attribute A and an object with attribute B have different parity positions.
- L9: `A and B have the same parity positions`: An object with attribute A and an object with attribute B have the same parity positions (positions may be the same or different, but the parity is always the same).
- L10: `A == B or A == C, but not both`: An object that has attribute A has attribute B, or an object that has attribute A has attribute C, but not both.
- L10: `A == B or B == C, but not both`: An object that has attribute A has attribute B, or an object that has attribute B has attribute C, but not both.
- L11: `A == B or A == C or both`: An object that has attribute A has attribute B, or an object that has attribute A has attribute C, or both.
- L11: `A == B or B == C or both`: An object that has attribute A has attribute B, or an object that has attribute B has attribute C, or both.
- L12: `A != B or A != C or both`: An object that has attribute A has not attribute B, or an object that has attribute A has not attribute C, or both.
- L12: `A != B or B != C or both`: An object that has attribute A has not attribute B, or an object that has attribute B has not attribute C, or both.
- L13: L12 without `A == B`.
- L14: L13 without `A is on the left of B`, `A is on the right of B`.
- L15: L14 without `A is on the far left`, `A is on the far right`, `A is in the middle`.
- L16: L15 without `A is between B and C`.
- L17: L16 without `A is on the left or right of B`, `A is on the far left or far right`.
- L18: L17 without `A is in an odd position`, `A is in an even position`.
- L19: L18 without `A is somewhere to the left of B`, `A is somewhere to the right of B`.
- L20: L19 without `A != B`.

## Einstein's Riddle, Zebra Puzzle and Blood Donation Puzzle Solver

Advantages of the solver:
1. No need for third party libraries.
2. The rules that the solver follows are given from outside.
3. Determining the complexity of the input puzzle: normal and complex (more difficult).

```commandline
python3 solver_example.py
```

### Einstein's Riddle
1. The Englishman lives in the red house.
2. The Swede keeps dogs.
3. The Dane drinks tea.
4. The green house is just to the left of the white one.
5. The owner of the green house drinks coffee.
6. The Pall Mall smoker keeps birds.
7. The owner of the yellow house smokes Dunhills.
8. The man in the center house drinks milk.
9. The Norwegian lives in the first house.
10. The Blend smoker has a neighbor who keeps cats.
11. The man who smokes Blue Masters drinks bier.
12. The man who keeps horses lives next to the Dunhill smoker.
13. The German smokes Prince.
14. The Norwegian lives next to the blue house.
15. The Blend smoker has a neighbor who drinks water.  
**Who keeps fish?**  
([Karttunen, Lauri. "Einstein's Puzzle"](https://web.stanford.edu/~laurik/fsmbook/examples/Einstein%27sPuzzle.html))

Program output:
```
Solution status: SOLVED, NORMAL TASK [0.001658 sec.]
| Norwegian | Dane   | Englishman | German | Swede        |
| yellow    | blue   | red        | green  | white        |
| cats      | horses | birds      | fishes | dogs         |
| water     | tea    | milk       | coffee | bier         |
| Dunhill   | Blend  | Pall Mall  | Prince | Blue Masters |
```

### Zebra Puzzle
1. There are five houses.
2. The Englishman lives in the red house.
3. The Spaniard owns the dog.
4. Coffee is drunk in the green house.
5. The Ukrainian drinks tea.
6. The green house is immediately to the right of the ivory house.
7. The Old Gold smoker owns snails.
8. Kools are smoked in the yellow house.
9. Milk is drunk in the middle house.
10. The Norwegian lives in the first house.
11. The man who smokes Chesterfields lives in the house next to the man with the fox.
12. Kools are smoked in the house next to the house where the horse is kept.
13. The Lucky Strike smoker drinks orange juice.
14. The Japanese smokes Parliaments.
15. The Norwegian lives next to the blue house.  
**Who drinks water? Who owns zebra?**  
(Life International, December 17, 1962)

Program output:
```
Solution status: SOLVED, COMPLEX TASK [0.005176 sec.]
| Norwegian | Ukrainian     | Englishman | Spaniard     | Japanese    |
| yellow    | blue          | red        | ivory        | green       |
| fox       | horse         | snails     | dog          | zebra       |
| water     | tea           | Milk       | orange juice | Coffee      |
| Kools     | Chesterfields | Old Gold   | Lucky Strike | Parliaments |
```

### Blood Donation Puzzle
1. The A+ donor is next to the B+ donor.
2. Brooke is at one of the ends.
3. The woman wearing a Black shirt is somewhere to the left of the 150 lb woman.
4. The Actress is next to the Chef.
5. Kathleen is 40 years old.
6. The Florist is somewhere to the right of the woman wearing the purple shirt.
7. The oldest year-old donor weighs 130 lb.
8. Brooke is next to Nichole.
9. The 35-year-old woman is exactly to the left of the 30-year-old woman.
10. The 120 lb donor is somewhere between the the O- donor and the 150 lb donor, in that order.
11. Kathleen is at one of the ends.
12. The woman wearing the purple shirt is somewhere to the right of the woman wearing the green shirt.
13. The B+ donor weighs 140 lb.
14. The youngest woman is next to the 30-year-old woman.
15. The woman considered AB+ universal recipient is exactly to the left of the A+ donor.
16. Meghan is somewhere to the right of the woman wearing the purple shirt.
17. The woman wearing the green shirt is somewhere between the Actress and the woman wearing the red shirt, in that order.
18. At one of the ends is the 130 lb woman.
19. The O- universal donor is 35 years old.
20. The Florist is somewhere between the Actress and the Engineer, in that order.
21. The woman wearing the blue shirt is somewhere to the left of the woman wearing the red shirt.
22. The AB+ donor is next to the youngest woman.  
**Whose blood type is B-? What color shirt is worn by the person weighing 160 lb?**  
**How many years old is Andrea? Which unit is the Policewoman?**  

Program output:
```
Solution status: SOLVED, COMPLEX TASK [0.010827 sec.]
| B-      | O-      | AB+         | A+      | B+       |
| Black   | green   | purple      | blue    | red      |
| Brooke  | Nichole | Andrea      | Meghan  | Kathleen |
| 45      | 35      | 30          | 25      | 40       |
| 130     | 160     | 120         | 150     | 140      |
| Actress | Chef    | Policewoman | Florist | Engineer |
```
