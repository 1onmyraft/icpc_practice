"""Fast recognition drill: clue -> pick the technique (1-4). Wrong answers explain why
and point to the notebook section.

  python3 recognizer/drill.py              20 cards, your weakest first
  python3 recognizer/drill.py 40           40 cards
  python3 recognizer/drill.py --tag graphs only one category
  python3 recognizer/drill.py --list       print every card (good for memorizing)

Tags: complexity, graphs, dp, greedy, "data structures", strings, math, geometry, procedure
Misses are saved in recognizer/drill_stats.json on your computer only.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = [dict(zip(("tag", "clue", "answer", "why", "where"), c))
         for c in json.load(open(os.path.join(HERE, "triggers.json")))]
STATS = os.path.join(HERE, "drill_stats.json")


def load_stats():
    try:
        with open(STATS) as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {}


def save_stats(s):
    with open(STATS, "w") as f:
        json.dump(s, f, indent=1)


def options_for(card, pool):
    others = list({c["answer"] for c in pool if c["answer"] != card["answer"]})
    same_tag = list({c["answer"] for c in pool if c["tag"] == card["tag"] and c["answer"] != card["answer"]})
    picks = random.sample(same_tag, min(2, len(same_tag)))          # harder: 2 from the same topic
    rest = [o for o in others if o not in picks]
    picks += random.sample(rest, 3 - len(picks))
    opts = picks + [card["answer"]]
    random.shuffle(opts)
    return opts


def ask(card, pool):
    opts = options_for(card, pool)
    print("\n" + "-" * 60)
    print("[%s]  %s" % (card["tag"], card["clue"]))
    for i, o in enumerate(opts, 1):
        print("  %d) %s" % (i, o))
    while True:
        a = input("> ").strip()
        if a in ("1", "2", "3", "4"):
            break
        if a.lower() in ("q", "quit"):
            return None
        print("Type 1-4, or q to stop.")
    if opts[int(a) - 1] == card["answer"]:
        print("Correct.")
        return True
    print("Wrong. Answer: %s" % card["answer"])
    print("Why: %s" % card["why"])
    print("Notebook: %s" % card["where"])
    return False


def main(argv):
    if "--list" in argv:
        for c in CARDS:
            print("[%s] %s\n    -> %s  (%s)" % (c["tag"], c["clue"], c["answer"], c["where"]))
        return
    n, tag = 20, None
    args = list(argv)
    if "--tag" in args:
        i = args.index("--tag")
        tag = args[i + 1]
        del args[i:i + 2]
    if args:
        n = int(args[0])
    pool = [c for c in CARDS if not tag or c["tag"] == tag]
    if not pool:
        print("No cards with that tag.")
        return
    stats = load_stats()
    # weakest first: most misses, then never seen, then random
    pool_sorted = sorted(pool, key=lambda c: (-stats.get(c["clue"], {}).get("miss", 0),
                                              stats.get(c["clue"], {}).get("seen", 0),
                                              random.random()))
    queue = pool_sorted[:n]
    random.shuffle(queue)
    right = asked = 0
    while queue:
        card = queue.pop(0)
        res = ask(card, CARDS)
        if res is None:
            break
        st = stats.setdefault(card["clue"], {"seen": 0, "miss": 0})
        st["seen"] += 1
        asked += 1
        if res:
            right += 1
            st["miss"] = max(0, st["miss"] - 1)
        else:
            st["miss"] += 1
            queue.insert(min(3, len(queue)), card)   # comes back in a few cards
    save_stats(stats)
    print("\n%d / %d right." % (right, asked))


if __name__ == "__main__":
    main(sys.argv[1:])
