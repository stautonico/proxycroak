DATABASE_VENDORS = ["sqlite", "mysql"]
ENVIRONMENTS = ["development", "testing", "production", "beta", "tools"]

# In theory, we should only need newer sets (SVI+) since all the rest have ptcgo codes
SET_IDS = {
    "SVI": "sv1",
    "PAL": "sv2",
    "OBF": "sv3",
    "MEW": "sv3pt5",
    "PAR": "sv4",
    "PAF": "sv4pt5",

    # Exceptions for GG and TGs
    "BRS-TG": "swsh9tg",
    "ASR-TG": "swsh10tg",
    "LOR-TG": "swsh11tg",
    "SIT-TG": "swsh12tg",
    "CRZ-GG": "swsh12pt5gg",

    # Exceptions for Shiny Vaults
    "HIF-SV": "sma",
    "SHF-SV": "swsh45sv",
}

CARD_TEXT_REPLACEMENTS = {
    "When you play this Pokémon from your hand onto your Bench during your turn": "When you play this from your hand to Bench on your turn",
    "You may play only 1 Supporter card during your turn (before your attack).": "[SUPP]",
    "You can play only one Supporter card each turn. When you play this card, put it next to your Active Pokémon. When your turn ends, discard this card.": "[SUPP]",
    "Attach a Pokémon Tool to 1 of your Pokémon that doesn't already have a Pokémon Tool attached to it.": "[TOOL]",
    "to 1 of your Pokémon that doesn't have a Pokémon Tool attached to it.": "as a [TOOL].",
    "You may play as many Item cards as you like during your turn (before your attack).": "[ITEM]",
    "This card stays in play when you play it. Discard this card if another Stadium card comes into play. If another card with the same name is in play, you can't play this card.": "[STAD]",
    "This card stays in play when you play it. Discard this card if another Stadium card comes into play.": "[STAD]",
    "(You can't use more than 1 GX attack in a game.)": "<strong>(GX-ATK)</strong>",
    "◇ (Prism Star) Rule: You can't have more than 1 ◇ card with the same name in your deck. If a ◇ card would go to the discard pile, put it in the Lost Zone instead.": "[PRISM]",
    "Once during your turn (before your attack)": "Once before ATK",
    "This damage isn't affected by Weakness or Resistance": "Don't apply W&R",
    "(Don't apply Weakness and Resistance for Benched Pokémon.)": "",
    "(before applying Weakness and Resistance)": "(before W&R)",
    "(after applying Weakness and Resistance)": "(before W&R)",
    "Shuffle your deck afterward": "Then shuffle",
    "shuffle your deck afterward": "then shuffle",
    "This attack does": "Do",
    "this attack does": "do",
    "Shuffle the other cards back into": "Shuffle the rest in",
    "Pokémon Tool": "Tool",
    "Stadium": "Stad",
    "Supporter": "Supp",
    "Rocket's Secret Machine": "RSM",
    "Technical Machine": "TM",
    "Asleep": "SLP",
    "Confused": "CNF",
    "Poisoned": "PSN",
    "Burned": "BRN",
    "Paralyzed": "PAR",
    "Lost Zone": "LZ",
    "your hand": "y-h",
    "your opponent's hand": "y-opp-h",
    "each player's hand": "e-pl-h",
    "his or her hand": "t-h",
    "your deck": "y-d",
    "your turn": "y-turn",
    "your opponent's deck": "y-opp-d",
    "your opponent's turn": "y-opp-turn",
    "each player's deck": "e-pl-d",
    "his or her deck": "t-d",
    "your discard pile": "y-dp",
    "your opponent's discard pile": "y-opp-dp",
    "each player's discard pile": "e-pl-dp",
    "his or her discard pile": "t-dp",
    "each player": "e-pl",
    "he or she": "(s)he",
    "his or her": "their",
    "all cards attached to it": "all cards attached",
    "damage counters": "dmgc",
    "damage counter": "dmgc",
    "damage": "dmg",
    "opponent": "opp",
    "Special Condition": "SpeCon",
    "Energy": "NRG",
    "Weakness": "WKN",
    "Resistance": "RES",
    "Retreat Cost": "RC",
    "Active Pokémon": "APKM",
    "Benched Pokémon": "BPKM",
    "Defending Pokémon": "DPKM",
    "Pokémon": "PKM",
    "Ultra Beast": "UB",
    "Prize cards": "Prizes",
    "Prize card": "Prize"
}


def minify_card_text(text):
    for orig, rep in CARD_TEXT_REPLACEMENTS.items():
        text = text.replace(orig, rep)

    return text


def lookup_set_code_by_id(set_id):
    for key, val in SET_IDS.items():
        if val == set_id:
            return key

    return None
