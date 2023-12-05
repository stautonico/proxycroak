import re


def parse_new_line(line: str):
    if line[-4:-1] == " PH":
        line = line[:-4] + line[-1]

    elements = line.split(" ")

    # Check if we have a basic energy without a set
    expr = r"^([\d]+) ((?:Basic)?[\w\s]+(?:Energy)) (\d+)?$"
    matches = re.search(expr, line)

    if matches:
        groups = matches.groups()
        if len(groups) == 2:
            amnt, card_name = groups
            card_num = None
        elif len(groups) == 3:
            amnt, card_name, card_num = groups
        else:
            # This should never happen, just in case, log
            pass

        # TODO: Check for set id in basic energy line
        set_id = None
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
        if "tg" in card_num.lower():
            # Remove the "tg"
            card_num = card_num[2:]
            card_num = "TG" + ("0" if int(card_num) < 10 else "") + card_num
        if "gg" in card_num.lower():
            # Remove the "tg"
            card_num = card_num[2:]
            card_num = "GG" + ("0" if int(card_num) < 10 else "") + card_num

        # If we're using PTCGL format (CRZ-GG 6 instead of CRZ GG06), we need to change the card num to include the GG
        if "tg" in set_id.lower():
            card_num = "TG" + ("0" if int(card_num) < 10 else "") + card_num
        elif "gg" in set_id.lower():
            card_num = "GG" + ("0" if int(card_num) < 10 else "") + card_num
        elif "pr-sw" in set_id.lower() and "SWSH" not in card_num:
            card_num = "SWSH" + ("0" if int(card_num) < 10 else "") + card_num

        # TODO: More bullshit hacks
        if set_id.lower() == "hif":
            if int(card_num) > 69:
                # We're in the hidden fates shiny vault
                card_num = "SV" + str(int(card_num) - 69)

        if set_id.lower() == "shf":
            if int(card_num) > 73:
                # We're in the shining fates shiny vault
                # Calculate the padding for this (should be 3 digits)
                card_num = "SV" + str(int(card_num) - 73).zfill(3)
                set_id = "SHF-SV"

    print(f"{amnt} | {set_id} | {card_num} | {card_name}")

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
