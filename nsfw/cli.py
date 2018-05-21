from nsfw import classify

import PIL.Image as Image
import sys


def probs(pct):
    """
    Return a human-readable string representing the probabilities.

    This scheme is shamelessly ripped from CIA's Words of Estimative
    Probability.

    https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/books-and-monographs/sherman-kent-and-the-board-of-national-estimates-collected-essays/6words.html

    100%                Certainty
    93%     +/- ~6%     Almost certain
    75%     +/- ~12%    Probable
    50%     +/- ~10%    Chances about even
    30%     +/- ~10%    Probably not
    7%      +/- ~5%     Almost certainly not
    0%                  Impossibility
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

        print("It is {} that this image is suitable for work.".format(probs(sfw)))
        print("It is {} that this image is *not* suitable for work.".format(probs(nsfw)))
