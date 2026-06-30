# the payoff matrix is organized as a dictionary 
# tuples pairs of capture and transport/storage projects as keys and dictionary as values
# dictionary matches capture and t/s to a list showing matrix values (top left -> top right -> bottom left -> bottom right)
PAYOFF_MATRIX = {
    ("c1", "ts1") : {"c": {"both_commit": 100, "commit_alone": -100, "free_ride": 0, "non_commit": 0 },
                     "ts": {"both_commit": 100, "commit_alone": -100, "free_ride": 0, "non_commit": 0 }},
    
    ("c2", "ts2") : {"c": {"both_commit": 100, "commit_alone": -100, "free_ride": 0, "non_commit": 0 },
                     "ts": {"both_commit": 100, "commit_alone": -100, "free_ride": 0, "non_commit": 0 }},

    ("c3", "ts3") : {"c": {"both_commit": 100, "commit_alone": -10, "free_ride": 0, "non_commit": 0 },
                     "ts": {"both_commit": 400, "commit_alone": -1000, "free_ride": 0, "non_commit": 0 }},
}

def deadlock(matrix = PAYOFF_MATRIX):
    """
    Identifies pairings that will end up in deadlock using Harsanyi and Selten's product of deviation losses solution
    to a multi-equilibria 2-player coordination game. Uses constants stored in the PAYOFF MATRIX
    
    Return:
        Dictionary of form {(project pair): pass/deadlocked} to feed into the DAG

    """
    is_deadlock = {}
    for (c, ts) in matrix.keys():
        # extract vals from the payoff matrix
        c_both_commit = matrix[(c, ts)]["c"]["both_commit"]
        c_commit_alone = matrix[(c, ts)]["c"]["commit_alone"]
        c_free_ride = matrix[(c, ts)]["c"]["free_ride"]
        c_non_commit = matrix[(c, ts)]["c"]["non_commit"]

        ts_both_commit = matrix[(c, ts)]["ts"]["both_commit"]
        ts_commit_alone = matrix[(c, ts)]["ts"]["commit_alone"]
        ts_free_ride = matrix[(c, ts)]["ts"]["free_ride"]
        ts_non_commit = matrix[(c, ts)]["ts"]["non_commit"]

        # checks if it's a valid 2-person coordination game (stag hunt)
        if not ((c_both_commit > c_non_commit) 
            and (ts_both_commit > ts_non_commit)
            and (c_commit_alone < c_non_commit)
            and (ts_commit_alone < ts_non_commit)
        ):
            is_deadlock[(c, ts)] = "NA"
            continue
        
        # calculating risk dominance
        # product of commit deviation losses = (A-B)(a-c)
        com_dev = (c_both_commit - c_free_ride)*(ts_both_commit - ts_free_ride)

        # product of wait deviation losses = (D-C)(d-b)
        wait_dev = (c_non_commit - c_commit_alone)*(ts_non_commit - ts_commit_alone)

        # label project pair as "pass" or "deadlocked" based on product of deviation losses
        if com_dev > wait_dev:
            is_deadlock[(c, ts)] = "pass"
        else:
            is_deadlock[(c, ts)] = "deadlocked"
    
    return is_deadlock
        
print(deadlock())


def percentage_deadlocked(matrix = PAYOFF_MATRIX):
    """
    Calculates percentage of projects that are deadlocked 

    Args:
        PAYOFF_MATRIX
    
    Return:
        Percentage of projects that are deadlocked
    
    """
    count = 0
    total = 0
    dict = deadlock(matrix)

    for (c, ts) in dict.keys():
        total += 1
        if dict[(c, ts)] == 'deadlocked':
            count += 1
    
    return count/total
        
print(percentage_deadlocked())




