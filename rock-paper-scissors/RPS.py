# RPS.py

BEATS = {"R": "P", "P": "S", "S": "R"}


def player(prev_play, state={}):
    # New match: prev_play is empty, so reset the state
    if prev_play == "":
        state.clear()
        state.update(
            opp=[],              # opponent's moves
            mine=[],             # my moves
            patterns={},         # counts of opponent sequences of length n+1
            my_pairs={},         # counts of my 2-move sequences (what abbey tracks)
            scores=[0, 0],       # how well each strategy would have done
            last_moves=None,     # what each strategy proposed last round
        )
        prev_play = "R"

    s = state
    s["opp"].append(prev_play)

    # Score each strategy against the move the opponent actually made
    if s["last_moves"] is not None:
        for i, move in enumerate(s["last_moves"]):
            if move == BEATS[prev_play]:
                s["scores"][i] += 1
            elif BEATS[move] == prev_play:
                s["scores"][i] -= 1

    # Strategy 0: predict the opponent from its last n moves
    n = 4
    opp = s["opp"]
    if len(opp) > n:
        seq = "".join(opp[-(n + 1):])
        s["patterns"][seq] = s["patterns"].get(seq, 0) + 1
    last = "".join(opp[-n:])
    counts = {m: s["patterns"].get(last + m, 0) for m in "RPS"}
    move0 = BEATS[max(counts, key=counts.get)]

    # Strategy 1: predict what the opponent thinks I will play
    # (like abbey: most frequent follow-up of my last move), then counter its counter
    mine = s["mine"]
    if mine:
        my_last = mine[-1]
        follow = {m: s["my_pairs"].get(my_last + m, 0) for m in "RPS"}
        my_predicted = max(follow, key=follow.get)
    else:
        my_predicted = "R"
    move1 = BEATS[BEATS[my_predicted]]

    s["last_moves"] = (move0, move1)
    move = move0 if s["scores"][0] >= s["scores"][1] else move1

    # Update my own history
    if mine:
        pair = mine[-1] + move
        s["my_pairs"][pair] = s["my_pairs"].get(pair, 0) + 1
    mine.append(move)

    return move