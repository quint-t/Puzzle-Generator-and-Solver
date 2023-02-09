import time
import collections
from typing import Union, Tuple, List, Set, Callable


def format_table(table: List[List[str]]) -> str:
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    return '\n'.join("| " + " | ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)) + " |"
                     for line in table)


def update_range(wns: List[str], rns: List[List[Set[str]]], cmp: Callable):
    changed = False
    for rn in rns:
        classified_words = set()
        for n_col, set_of_words in enumerate(rn):
            if len(set_of_words) == 1:
                classified_words.add(next(iter(set_of_words)))
        word_to_cols = dict()
        for n_col, set_of_words in enumerate(rn):
            if len(set_of_words) != 1:
                prev_length = len(set_of_words)
                set_of_words.difference_update(classified_words)
                changed |= prev_length != len(set_of_words)
                for word in set_of_words:
                    word_to_cols.setdefault(word, set()).add(n_col)
        for word, cols in word_to_cols.items():
            if len(cols) == 1:
                x = rn[next(iter(cols))]
                if len(x) != 1:
                    x.clear()
                    x.add(word)
                    changed = True

    new_rns = [[{x for x in xs if x != wn} for xs in rn] for wn, rn in zip(wns, rns)]
    pairs = []
    for wn, rn in zip(wns, rns):
        new_pairs = []
        break_condition = True
        for cn, setn in enumerate(rn):
            if wn in setn:
                break_condition = False
                if not pairs:
                    pairs = [[]]
                for v in pairs:
                    new_pairs.append([*v, cn])
        pairs = new_pairs
        if break_condition:
            break
    for pair in pairs:
        if cmp(*pair):
            for nrn, cn, wn in zip(new_rns, pair, wns):
                nrn[cn].add(wn)
    changed |= any(rn != new_rn for rn, new_rn in zip(rns, new_rns))
    if changed:
        for rn, new_rn in zip(rns, new_rns):
            for old, new in zip(rn, new_rn):
                old.intersection_update(new)
    return changed


def update_ranges(relations: List[Tuple[List[int], List[str], Callable, ...]],
                  ranges: List[List[Set[str]]]):
    changed = False
    for ins, wns, callable_object, *_ in relations:
        changed |= update_range(wns, [ranges[i] for i in ins], callable_object)
    return changed


def solve_puzzle(table: List[List[str]],
                 relations: List[Union[Tuple[List[int], List[str], Union[Callable, Set[Callable], List[Callable]]],
                                       Tuple[List[int], List[str], Union[Callable, Set[Callable], List[Callable]], ...]]],
                 *,
                 allow_complex=True,
                 max_solutions: Union[bool, None] = None) -> Tuple[bool, List[List[List[set]]], bool]:

    if max_solutions is not None and max_solutions <= 0:
        return False, [], False

    new_relations = list()
    for ins, wns, callable_object, *other in relations:
        if callable(callable_object):
            callable_object = {callable_object}
        if callable_object:
            objs = frozenset(callable_object)
            new_relations.append((ins, wns,
                                  lambda *c, objs=objs: all(callable_object(*c) for callable_object in objs),
                                  *other))
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
        ('first', lambda c1: c1 == 0),
        ('center', lambda c1, center=center: c1 == center),
        ('left', lambda c1, c2: c1 == c2 - 1),
        ({'live', 'keep', 'drink', 'smoke'}, lambda c1, c2: c1 == c2),
    ]

    relations = list()
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
        if founded_objects:
            relations.append(([token[1] for token in founded_objects],
                              [token[2] for token in founded_objects],
                              founded_relations))

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
        ('first', lambda c1: c1 == 0),
        ('middle', lambda c1, center=center: c1 == center),
        ('next', lambda c1, c2: c1 == c2 - 1 or c1 == c2 + 1),
        ('right', lambda c1, c2: c1 == c2 + 1),
        ({'live', 'own', 'drink', 'drunk', 'smoke'}, lambda c1, c2: c1 == c2),
    ]

    relations = list()
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
        if founded_objects:
            relations.append(([token[1] for token in founded_objects],
                              [token[2] for token in founded_objects],
                              founded_relations))

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
        ('ends', lambda c1: c1 == 0 or c1 == end),
        ('somewhere to the left', lambda c1, c2: c1 < c2),
        ('somewhere to the right', lambda c1, c2: c1 > c2),
        ('left', lambda c1, c2: c1 == c2 - 1),
        ('right', lambda c1, c2: c1 == c2 + 1),
        ('between', lambda c1, c2, c3: c2 < c1 < c3 or c3 < c1 < c2),
        ({'is', 'weighs'}, lambda c1, c2: c1 == c2),
    ]

    relations = list()
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
        if founded_objects:
            relations.append(([token[1] for token in founded_objects],
                              [token[2] for token in founded_objects],
                              founded_relations))

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
