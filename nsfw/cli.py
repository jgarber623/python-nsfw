from nsfw import classify
from PIL import Image
import sys


def probs(pct):
    """
    return a human readable string representing the probabilities.

    This scheme is shamelessly ripped from CIA's Words of Estimative
    Probability.

    https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/books-and-monographs/sherman-kent-and-the-board-of-national-estimates-collected-essays/6words.html

    100%    Certainty
    93%	give or take about 6%	Almost certain
    75%	give or take about 12%	Probable
    50%	give or take about 10%	Chances about even
    30%	give or take about 10%	Probably not
    7%	give or take about 5%	Almost certainly not
    0%      Impossibility
    """
    pct = int(pct * 100)

    if pct == 100:
        return "certain"

    if pct > 87:
        return "almost certain"

    if pct > 63:
        return "probable"

    if pct > 40:
        return "about even"

    if pct > 20:
        return "probably not"

    if pct > 2:
        return "almost certainly not"

    return "an impossibility"


def check():
    """
    """

    files = sys.argv[1:]
    if not files:
        print("""\
Usage:

    nsfwcheck files...

""")
        return

    for path in files:
        image = Image.open(path)
        sfw, nsfw = classify(image)

        print("It is {} that this image is safe for work".format(probs(sfw)))
        print("It is {} that this image is *not* safe for work".format(probs(nsfw)))
