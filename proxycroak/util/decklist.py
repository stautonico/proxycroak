import re


def parse_new_line(line: str):
    elements = line.split(" ")

    # Check if we have a basic energy without a set
    expr = r"^([\d]+) ((?:Basic)?[\w\s]+(?:Energy))(?: \d+)?$"
    matches = re.search(expr, line)

    if matches:
        amnt, card_name = matches.groups()
        set_id = None
        card_num = None
    else:
        # Element 0: Amount
        # Element -2: The set ID
        # Element -1: The card number
        # Every other element combined: The card name

        amnt = elements.pop(0)
        set_id = elements.pop(-2)
        card_num = elements.pop(-1).replace("\r", "")
        card_name = " ".join(elements)

        # TODO: Bullshit hack
        if "tg" in set_id.lower():
            card_num = "TG" + ("0" if int(card_num) < 10 else "") + card_num
        elif "gg" in set_id.lower():
            card_num = "GG" + ("0" if int(card_num) < 10 else "") + card_num
        elif "pr-sw" in set_id.lower():
            card_num = "SWSH" + ("0" if int(card_num) < 10 else "") + card_num

    return {
        "amnt": int(amnt),
        "set_id": set_id,
        "card_num": card_num,
        "card_name": card_name
    }


def parse_old_line(line):
    elements = line.split(" ")

    # Check if we have a basic energy without a set
    expr = r"^\* ([\d]+) ((?:Basic)?[\w\s]+(?:Energy))(?: \d+)?$"
    matches = re.search(expr, line)
    if matches:
        # This is a basic energy without a set
        amnt, card_name = matches.groups()
        set_id = None
        card_num = None
    else:
        # Element 0: Ignore
        # Element 1: Amount
        # Element -2: Set ID
        # Element -1: The card number
        # Every other element combined: The card name
        elements.pop(0)

        # TODO: OLD LINE FORMAT DOESN'T SUPPORT TG

        amnt = elements.pop(0)
        set_id = elements.pop(-2)
        card_num = elements.pop(-1)
        card_name = " ".join(elements)

    return {
        "amnt": int(amnt),
        "set_id": set_id,
        "card_num": card_num,
        "card_name": card_name
    }


def parse_decklist(decklist: str):
    # Strip out any of the "section" lines (Pokemon: n, Trainer: n, Energy: n)
    # TODO: Why doesn't using ^$ work even if multi-line is enabled?
    pattern = r"((?:pok[eé]mon|trainer|energy): ?\d+)"
    matches = re.findall(pattern, decklist, flags=re.IGNORECASE | re.MULTILINE)
    for match in matches:
        decklist = decklist.replace(match, "")

    # TODO: This doesn't work???
    # decklist = re.sub(pattern, "", decklist)
    # print(decklist)

    output = []

    lines = decklist.split("\n")

    # Strip out empty lines
    while "" in lines:
        lines.remove("")

    # TODO: Find a way to do this without a loop :)
    for line in lines:
        if line[0] in ["*", "#"]:
            dlformat = "old"
            break
        elif line[0].isalnum():
            dlformat = "new"
            break
    else:
        # TODO: Find a way to return an error
        return None

    for line in lines:
        # Shouldn't happen but check anyway
        if line != "":
            if dlformat == "old":
                if line[0] == "#" or line[:2] == "**":
                    continue
                elif line[0] == "*":
                    output.append(parse_old_line(line))
                else:
                    # We have an invalid line, ignore it
                    continue
            else:
                if line[0] in "123456789":
                    output.append(parse_new_line(line))

    return output
