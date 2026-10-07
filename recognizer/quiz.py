"""Technique recognizer: free recall first, then reveal, then rate yourself.

  python3 recognizer/quiz.py quiz [N] [--tag TAG]   review due cards
  python3 recognizer/quiz.py add                    add a card from a problem you just met
  python3 recognizer/quiz.py stats                  how many cards per box / tag

Progress is stored in recognizer/progress.json (box 0..4 and due date).
"""
import json
import os
import random
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "deck.json")
PROGRESS = os.path.join(HERE, "progress.json")
INTERVALS = [0, 1, 3, 7, 14]    # days until a card in this box returns


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=1)


def due_cards(deck, progress, tag, today):
    out = []
    for c in deck:
        if tag and c["tag"] != tag:
            continue
        p = progress.get(c["id"])
        if p is None or date.fromisoformat(p["due"]) <= today:
            out.append(c)
    return out


def rate(progress, card, grade, today):
    p = progress.get(card["id"], {"box": 0})
    if grade == "y":
        p["box"] = min(p["box"] + 1, len(INTERVALS) - 1)
    elif grade == "n":
        p["box"] = 0
    p["due"] = (today + timedelta(days=INTERVALS[p["box"]])).isoformat()
    progress[card["id"]] = p


def quiz(argv, today=None):
    today = today or date.today()
    n, tag = 10, None
    args = list(argv)
    if "--tag" in args:
        i = args.index("--tag")
        tag = args[i + 1]
        del args[i:i + 2]
    if args:
        n = int(args[0])

    deck, progress = load(DECK, []), load(PROGRESS, {})
    cards = due_cards(deck, progress, tag, today)
    random.shuffle(cards)
    cards = cards[:n]
    if not cards:
        print("Nothing due. Come back tomorrow or add cards.")
        return
    right = 0
    for c in cards:
        print("\n[%s] %s" % (c["source"], c["text"]))
        if c["constraints"]:
            print("Constraints:", c["constraints"])
        input("What technique or key idea? (type it, then Enter) ")
        print("Technique:", c["technique"])
        print("Idea:", c["idea"])
        if c["pitfalls"]:
            print("Pitfalls:", c["pitfalls"])
        g = ""
        while g not in ("y", "n", "s"):
            g = input("Did you get it? y / n / s(skip) ").strip().lower()[:1]
        if g == "y":
            right += 1
        rate(progress, c, g, today)
    save(PROGRESS, progress)
    print("\n%d / %d recognized." % (right, len(cards)))


def add():
    deck = load(DECK, [])
    card = {"id": "user-%d" % (len(deck) + 1)}
    for key in ("source", "tag", "text", "constraints", "technique", "idea", "pitfalls"):
        card[key] = input(key + ": ").strip()
    deck.append(card)
    save(DECK, deck)
    print("Added", card["id"])


def stats():
    deck, progress = load(DECK, []), load(PROGRESS, {})
    by_tag = {}
    for c in deck:
        by_tag[c["tag"]] = by_tag.get(c["tag"], 0) + 1
    print("cards:", len(deck))
    for t, k in sorted(by_tag.items()):
        print("  %-15s %d" % (t, k))
    boxes = [0] * len(INTERVALS)
    for c in deck:
        boxes[progress.get(c["id"], {"box": 0})["box"]] += 1
    print("by box (0 = new/missed ... 4 = well known):", boxes)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "quiz"
    if cmd == "quiz":
        quiz(sys.argv[2:])
    elif cmd == "add":
        add()
    elif cmd == "stats":
        stats()
    else:
        print(__doc__)
