#!/usr/bin/env python3


def boxed_print(txt, double=False):
    tl, h, tr, v, bl, br = u"╔═╗║╚╝" if double else u"┌─┐│└┘"
    N = max([len(line) for line in txt.split("\n")])
    print(tl + h * (N + 2) + tr)
    for line in txt.split("\n"):
        print(v + " " + line + " " * (N - len(line) + 1) + v)
    print(bl + h * (N + 2) + br)


def selector(query, *choices):
    if len(choices):
        print("\nSelect %s :" % query)
        for pair in enumerate(choices, 1):
            print("%5d - %s" % pair)

        while True:
            try:
                id = int(input("Selection [1-%d] " % len(choices)))
                if 0 < id <= len(choices):
                    break
            except ValueError:
                pass

            print("Wrong input.")

        return id
    else:
        while True:
            try:
                c = input("%s [y/n] " % query)[0].lower()
                if c in "yn":
                    break
            except IndexError:
                pass

            print("Wrong input.")

        return c == "y"


def main_loop():
    wtype = selector("weapon type", "Simple", "Martial (+d2)")
    wprop = selector(
        "weapon property",
        "Light (-d2)",
        "None",
        "Versatile",
        "Two-handed (+d2)",
    )
    print("")
    throw = selector("Is throwable?")
    reach = selector("Has reach? (-d2)")
    free_finesse = wtype == 1 and wprop in [1, 2] and not reach
    fines = selector("Has finesse? (%s)" % ("free" if free_finesse else "-d2"))
    heavy = selector("Is heavy? (+d2)") if wprop == 4 else False
    dtype = selector(
        "weapon damage type", "Slashing", "Piercing", "Bludgeonning"
    )

    mod = (
        (wtype == 2)
        - (wprop == 1)
        + (wprop == 4)
        - reach
        - (fines and not free_finesse)
        + heavy
    )
    dsize = 6 + 2 * mod
    Ndice = [(d, dsize // d) for d in [12, 10, 8, 6, 4] if dsize % d == 0]
    if len(Ndice) > 1 and dsize:
        i = selector("dice combination", *["%dd%d" % (n, d) for d, n in Ndice])
        dsize, N = Ndice[i - 1]
    else:
        N = 1

    if wprop == 3:
        dvers = N * dsize + 2
        Ndice = [(d, dvers // d) for d in [12, 10, 8, 6, 4] if dvers % d == 0]
        if len(Ndice) > 1:
            i = selector(
                "versatile dice combination",
                *["%dd%d" % (n, d) for d, n in Ndice]
            )
            dvers, Nvers = Ndice[i - 1]
        else:
            Nvers = 1

        versatile = "versatile (%dd%d)" % (Nvers, dvers)
    else:
        versatile = ""

    props = [["light"], [], [versatile], ["two-handed"]][wprop - 1]
    if reach:
        props += ["reach"]
    if fines:
        props += ["finesse"]
    if throw:
        props += ["thrown"]
    if heavy:
        props += ["heavy"]
    propslist = ", ".join(props).capitalize() + "." if props else "None"
    dmgtype = ["slashing", "piercing", "bludgeonning"][dtype - 1]
    cat = "Simple" if wtype == 1 else "Martial"
    dmg = "%dd%d" % (N, dsize) if dsize else "1"
    out = "%s weapon - %s %s - %s" % (cat, dmg, dmgtype, propslist)

    print("")
    boxed_print(out)
    print("")


if __name__ == "__main__":
    boxed_print("Kibbles Weapon builder", double=True)
    while True:
        try:
            main_loop()
        except KeyboardInterrupt:
            break
