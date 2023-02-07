# Einstein's Riddle, Zebra Puzzle and Blood Donation Puzzle Solver

## Einstein's Riddle
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
Solution status: SOLVED, NORMAL TASK [0.002554 sec.]
| Norwegian | Dane   | Englishman | German | Swede        |
| yellow    | blue   | red        | green  | white        |
| cats      | horses | birds      | fishes | dogs         |
| water     | tea    | milk       | coffee | bier         |
| Dunhill   | Blend  | Pall Mall  | Prince | Blue Masters |
```

## Zebra Puzzle
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
Solution status: SOLVED, COMPLEX TASK [0.010846 sec.]
| Norwegian | Ukrainian     | Englishman | Spaniard     | Japanese    |
| yellow    | blue          | red        | ivory        | green       |
| fox       | horse         | snails     | dog          | zebra       |
| water     | tea           | Milk       | orange juice | Coffee      |
| Kools     | Chesterfields | Old Gold   | Lucky Strike | Parliaments |
```

## Blood Donation Puzzle
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
Solution status: SOLVED, COMPLEX TASK [0.020552 sec.]
| B-      | O-      | AB+         | A+      | B+       |
| Black   | green   | purple      | blue    | red      |
| Brooke  | Nichole | Andrea      | Meghan  | Kathleen |
| 45      | 35      | 30          | 25      | 40       |
| 130     | 160     | 120         | 150     | 140      |
| Actress | Chef    | Policewoman | Florist | Engineer |
```
