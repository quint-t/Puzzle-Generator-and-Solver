import time
import collections
from typing import Union, Tuple, List, Set, Dict, Iterable, Callable


def format_table(table: List[List[str]]) -> str:
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    return '\n'.join("| " + " | ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)) + " |"
                     for line in table)


def solve_puzzle(table: List[List[str]],
                 relations: Dict[Tuple[int, str], Dict[Tuple[int, str], Union[Callable, Iterable[Callable]]]],
                 *,
                 allow_complex=True,
                 max_solutions: Union[bool, None] = None) -> Tuple[bool, List[List[List[set]]], bool]:

    if max_solutions is not None and max_solutions <= 0:
        return False, [], False

    def update_range(w1: str, w2: str, r1: List[Set[str]], r2: List[Set[str]], cmp: Callable):
        changed = False
        for rn in [r1, r2]:
            for n_col_1, set_of_words_1 in enumerate(rn):
                if len(set_of_words_1) == 1:
                    classified_word = next(iter(set_of_words_1))
                    for n_col_2, set_of_words_2 in enumerate(rn):
                        if n_col_1 != n_col_2 and classified_word in set_of_words_2:
                            set_of_words_2.remove(classified_word)
                            changed = True
            word_to_cols = dict()
            for n_col, set_of_words in enumerate(rn):
                for word in set_of_words:
                    word_to_cols.setdefault(word, set()).add(n_col)
            for word, cols in word_to_cols.items():
                if len(cols) == 1:
                    col_of_classified_word = next(iter(cols))
                    rn[col_of_classified_word] = {word}
                    for n_col_2, set_of_words_2 in enumerate(rn):
                        if col_of_classified_word != n_col_2 and word in set_of_words_2:
                            set_of_words_2.remove(word)
                            changed = True

        new_r1 = [{x for x in xs if x != w1} for xs in r1]
        new_r2 = [{x for x in xs if x != w2} for xs in r2]
        for c1, set1 in enumerate(r1):
            for c2, set2 in enumerate(r2):
                if cmp(c1, c2) and w1 in set1 and w2 in set2:
                    new_r1[c1].add(w1)
                    new_r2[c2].add(w2)
        changed |= r1 != new_r1 or r2 != new_r2
        if changed:
            for rn, new_rn in [(r1, new_r1), (r2, new_r2)]:
                for old, new in zip(rn, new_rn):
                    old.intersection_update(new)
        return changed

    def update_ranges(relations: Dict[Tuple[int, str], Dict[Tuple[int, str], Callable]],
                      ranges: List[List[Set[str]]]):
        changed = False
        for (i, w1), rs in relations.items():
            for (next_i, w2), callable_object in rs.items():
                changed |= update_range(w1, w2, ranges[i], ranges[next_i], callable_object)
        return changed

    new_relations = dict()
    for (i, w1), rs in relations.items():
        for (next_i, w2), w1_w2_relations in rs.items():
            if callable(w1_w2_relations):
                w1_w2_relations = {w1_w2_relations}
            if w1_w2_relations:
                objs = frozenset(w1_w2_relations)
                new_relations.setdefault((i, w1), dict())[(next_i, w2)] = \
                    lambda c1, c2, objs=objs: all(callable_object(c1, c2) for callable_object in objs)
    relations = new_relations

    ranges = [[set(table[i]) for _ in range(len(table[i]))] for i in range(len(table))]
    changed = True
    while changed:
        changed = update_ranges(relations, ranges)

    # check for 'no solutions'
    no_solutions = False
    complex_task = False
    for rng in ranges:
        for rs in rng:
            if len(rs) == 0:
                no_solutions = True
                break
            elif len(rs) > 1:
                complex_task = True
        if no_solutions:
            break
    if no_solutions or not allow_complex:
        return False, [ranges], False  # status of ranges, ranges, is_complex_task
    if not complex_task:
        return True, [ranges], False  # status of ranges, ranges, is_complex_task

    # if complex task, then algorithm will find all possible solutions
    q = collections.deque([ranges])
    possible_solutions = []
    while q:
        current_ranges = q.popleft()

        # check for 'no solutions' and 'solved'
        no_solutions = False
        solved = True
        for rng in current_ranges:
            for rs in rng:
                if len(rs) == 0:
                    no_solutions = True
                    solved = False
                    break
                elif len(rs) > 1:
                    solved = False
            if no_solutions or not solved:
                break
        if no_solutions:
            continue
        if solved:
            if current_ranges not in possible_solutions:
                possible_solutions.append(current_ranges)
                if max_solutions is not None and len(possible_solutions) >= max_solutions:
                    break
            continue

        # generate new ranges
        for n_group, rng in enumerate(current_ranges):
            founded = False
            for n_x, rs in enumerate(rng):
                if len(rs) > 1:
                    founded = True
                    for r in rs:
                        new_ranges = [[x.copy() for x in row] for row in current_ranges]
                        new_ranges[n_group][n_x] = {r}
                        changed = True
                        while changed:
                            changed = update_ranges(relations, new_ranges)
                        q.append(new_ranges)
                    break
            # if one group contained uncertainties, then other groups will be considered in ranges appended in q
            if founded:
                break

    if possible_solutions:
        return True, possible_solutions, True  # status of ranges, ranges, is_complex_task
    else:
        return False, [ranges], True  # status of ranges, ranges, is_complex_task


def solve_einstein_riddle():
    print("Einstein's Riddle")
    task = ' ' * 4 + """
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
    """.strip()
    print('Task:')
    print(task)

    classified_objects = [
        ['Englishman', 'Swede', 'Dane', 'Norwegian', 'German'],
        ['red', 'green', 'white', 'yellow', 'blue'],
        ['dogs', 'birds', 'cats', 'horses', 'fishes'],
        ['tea', 'coffee', 'milk', 'bier', 'water'],
        ['Pall Mall', 'Dunhill', 'Blend', 'Blue Masters', 'Prince']
    ]
    center = len(classified_objects[0]) // 2
    rules_for_relations = [
        ({'neighbor', 'next'}, lambda c1, c2: c1 == c2 - 1 or c1 == c2 + 1),
        ('first', lambda c1, c2: c1 == c2 and c2 == 0),
        ('center', lambda c1, c2, center=center: c1 == center and c2 == center),
        ('left', lambda c1, c2: c1 == c2 - 1),
        ({'live', 'keep', 'drink', 'smoke'}, lambda c1, c2: c1 == c2),
    ]

    relations = dict()
    for line in task.splitlines(keepends=False):
        founded_objects = []
        for n_group, group in enumerate(classified_objects):
            for item in group:
                if item in line:
                    founded_objects.append((line.index(item), n_group, item))
        founded_objects.sort()
        founded_relations = set()
        for relations_strings, callable_object in rules_for_relations:
            if type(relations_strings) is not set:
                relations_strings = {relations_strings}
            for relation_string in relations_strings:
                if relation_string in line:
                    founded_relations.add(callable_object)
                    break
            if founded_relations:
                break
        if len(founded_objects) == 2:
            token1, token2 = founded_objects
            relations.setdefault(token1[1:], dict())[token2[1:]] = founded_relations
        elif len(founded_objects) == 1:
            token1 = founded_objects[0]
            relations.setdefault(token1[1:], dict())[token1[1:]] = founded_relations

    t1 = time.perf_counter()
    status, solutions, complex_status = solve_puzzle(classified_objects, relations)
    t2 = time.perf_counter()
    for solution in solutions:
        print('Solution status: ', status and 'SOLVED' or 'NO SOLUTION', ', ',
              complex_status and 'COMPLEX TASK' or 'NORMAL TASK',
              f' [{(t2 - t1):.6f} sec.]', sep='')
        if status:
            solution = [[next(iter(x)) for x in row] for row in solution]
            print(format_table(solution))
        else:
            print(solution)


def solve_zebra_puzzle():
    print("Zebra Puzzle")
    task = ' ' * 4 + """
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
    """.strip()
    print('Task:')
    print(task)

    classified_objects = [
        ['Englishman', 'Spaniard', 'Ukrainian', 'Norwegian', 'Japanese'],
        ['red', 'green', 'ivory', 'yellow', 'blue'],
        ['dog', 'snails', 'fox', 'horse', 'zebra'],
        ['Coffee', 'tea', 'Milk', 'orange juice', 'water'],
        ['Old Gold', 'Kools', 'Chesterfields', 'Lucky Strike', 'Parliaments']
    ]
    center = len(classified_objects[0]) // 2
    rules_for_relations = [
        ('first', lambda c1, c2: c1 == c2 and c2 == 0),
        ('middle', lambda c1, c2, center=center: c1 == center and c2 == center),
        ('next', lambda c1, c2: c1 == c2 - 1 or c1 == c2 + 1),
        ('right', lambda c1, c2: c1 == c2 + 1),
        ({'live', 'own', 'drink', 'drunk', 'smoke'}, lambda c1, c2: c1 == c2),
    ]

    relations = dict()
    for line in task.splitlines(keepends=False):
        founded_objects = []
        for n_group, group in enumerate(classified_objects):
            for item in group:
                if item in line:
                    founded_objects.append((line.index(item), n_group, item))
        founded_objects.sort()
        founded_relations = set()
        for relations_strings, callable_object in rules_for_relations:
            if type(relations_strings) is not set:
                relations_strings = {relations_strings}
            for relation_string in relations_strings:
                if relation_string in line:
                    founded_relations.add(callable_object)
                    break
            if founded_relations:
                break
        if len(founded_objects) == 2:
            token1, token2 = founded_objects
            relations.setdefault(token1[1:], dict())[token2[1:]] = founded_relations
        elif len(founded_objects) == 1:
            token1 = founded_objects[0]
            relations.setdefault(token1[1:], dict())[token1[1:]] = founded_relations

    t1 = time.perf_counter()
    status, solutions, complex_status = solve_puzzle(classified_objects, relations)
    t2 = time.perf_counter()
    for solution in solutions:
        print('Solution status: ', status and 'SOLVED' or 'NO SOLUTION', ', ',
              complex_status and 'COMPLEX TASK' or 'NORMAL TASK',
              f' [{(t2 - t1):.6f} sec.]', sep='')
        if status:
            solution = [[next(iter(x)) for x in row] for row in solution]
            print(format_table(solution))
        else:
            print(solution)


def solve_blood_donation_puzzle():
    print("Blood Donation Puzzle")
    task = ' ' * 4 + """
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
        """.strip()
    print('Task:')
    print(task)

    classified_objects = [
        [' A+', ' AB+', ' B+', ' B-', ' O-'],
        [' Black ', ' blue ', ' green ', ' purple ', ' red '],
        ['Andrea', 'Brooke', 'Kathleen', 'Meghan', 'Nichole'],
        [' 25', ' 30', ' 35', ' 40', ' 45'],
        [' 120', ' 130', ' 140', ' 150', ' 160'],
        ['Actress', 'Chef', 'Engineer', 'Florist', 'Policewoman']
    ]
    task = task.replace('youngest', '25').replace('oldest', '45')
    end = len(classified_objects[0]) - 1
    rules_for_relations = [
        ('next', lambda c1, c2: c1 == c2 - 1 or c1 == c2 + 1),
        ('ends', lambda c1, c2: c1 == 0 and c2 == 0 or c1 == end and c2 == end),
        ('somewhere to the left', lambda c1, c2: c1 < c2),
        ('somewhere to the right', lambda c1, c2: c1 > c2),
        ('left', lambda c1, c2: c1 == c2 - 1),
        ('right', lambda c1, c2: c1 == c2 + 1),
        ('between', (lambda c1, c2: c1 > c2, lambda c1, c2: c1 < c2)),
        ({'is', 'weighs'}, lambda c1, c2: c1 == c2),
    ]

    relations = dict()
    for line in task.splitlines(keepends=False):
        founded_objects = []
        for n_group, group in enumerate(classified_objects):
            for item in group:
                if item in line:
                    founded_objects.append((line.index(item), n_group, item))
        founded_objects.sort()
        founded_relations = set()
        for relations_strings, callable_object in rules_for_relations:
            if type(relations_strings) is not set:
                relations_strings = {relations_strings}
            for relation_string in relations_strings:
                if relation_string in line:
                    founded_relations.add(callable_object)
                    break
            if founded_relations:
                break
        if len(founded_objects) == 3:  # 'between' case
            token1, token2, token3 = founded_objects
            f1, f2 = next(iter(founded_relations))
            relations.setdefault(token1[1:], dict())[token2[1:]] = f1
            relations.setdefault(token1[1:], dict())[token3[1:]] = f2
        elif len(founded_objects) == 2:
            token1, token2 = founded_objects
            relations.setdefault(token1[1:], dict())[token2[1:]] = founded_relations
        elif len(founded_objects) == 1:
            token1 = founded_objects[0]
            relations.setdefault(token1[1:], dict())[token1[1:]] = founded_relations

    t1 = time.perf_counter()
    status, solutions, complex_status = solve_puzzle(classified_objects, relations)
    t2 = time.perf_counter()
    for solution in solutions:
        print('Solution status: ', status and 'SOLVED' or 'NO SOLUTION', ', ',
              complex_status and 'COMPLEX TASK' or 'NORMAL TASK',
              f' [{(t2 - t1):.6f} sec.]', sep='')
        if status:
            solution = [[next(iter(x)).strip() for x in row] for row in solution]
            print(format_table(solution))
        else:
            print(solution)


if __name__ == "__main__":
    print('=' * 42)
    solve_einstein_riddle()
    print('=' * 42)
    solve_zebra_puzzle()
    print('=' * 42)
    solve_blood_donation_puzzle()
    print('=' * 42)
