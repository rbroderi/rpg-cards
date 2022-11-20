from __future__ import annotations
import json
import csv
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

SCRIPT_ROOT = Path(__file__).parent

BLANK_BODY: list[str] = []
for _ in range(17):
    BLANK_BODY.append(
        "description |___________________________________________________________|"
    )


class Property(Enum):
    Finesse = "Use your choice of Strength or Dexterity modifier for attack and damage."
    Light = (
        "When you attack while dual wielding light weapons, you may use a bonus action"
        " to attack with your off hand."
    )
    Thrown = "You can throw the weapon to make a ranged attack with the given range."
    Heavy = "Unless you have the required strength, your speed is reduced by 10 feet."
    Heavy_Weapon = (
        "Small creatures have disadvantage on attack rolls with heavy weapons."
    )
    Cumbersome = "You have disadvantage on Dexterity (Stealth) checks."
    Don = (
        "This is the time it takes to put on armor. You benefit from the armor's AC"
        " only if you take the full time to don the suit of armor."
    )
    Doff = (
        "This is the time it takes to take off armor. If you have help, reduce this"
        " time by half."
    )
    Ammunition = (
        "Each time you make a ranged attack with the weapon, use one piece of"
        " ammunition (loading requires a free hand). You can recover half your expended"
        " ammunition by taking a minute to search."
    )
    Loading = (
        "You can fire only one piece of ammunition from it regardless of the number of"
        " attacks you can normally make."
    )
    Range = (
        "The first number is normal range and the second is the weapon's long range."
        " Beyond normal range, you have disadvantage."
    )
    Reach = (
        "This weapon adds 5 feet to your reach when you attack with it, as well as when"
        " determining your reach for opportunity attacks with it."
    )
    Special = (
        "A weapon with the special property has unusual rules governing its use,"
        " explained in the weapon's description (see “Special Weapons” later in this"
        " section)."
    )
    Two_Handed = "This weapon requires two hands when you attack with it."
    Versatile = (
        "This weapon can be used with one or two hands. A damage value in parentheses"
        " appears with the property-the damage when the weapon is used with two hands"
        " to make a melee attack."
    )
    Martial = "Require more specialized training to use this weapon effectively."
    Simple = "Most can use with proficiency."


class Don_Doff(Enum):
    light = ("1 minute", "1 minute")
    medium = ("5 minutes", "1 minute")
    heavy = ("10 minutes", "5 minutes")
    shield = ("1 action", "1 action")


class Damage_Type(Enum):
    bludgeoning = "bludgeoning"
    slashing = "slashing"
    piercing = "piercing"
    unknown = "-"


# with Path(SCRIPT_ROOT / "rpg_cards.json").open("r", encoding="utf8") as file:
#     for line in file:
#         print(line.rstrip())

# Opening JSON file


def get_json() -> dict[str, Any]:
    with Path(SCRIPT_ROOT / "rpg_cards.json").open("r", encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


def get_db() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    with Path(SCRIPT_ROOT / "db.csv").open("r", encoding="utf8") as csv_file:
        # reading the csv file using DictReader
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            if reader.fieldnames is not None:
                output.append(dict(row))
            else:
                raise ValueError("no field names")
    return output


def main() -> None:
    ...


@dataclass
class Fill:
    amount: int

    def __str__(self) -> str:
        return f"fill | {self.amount}"


@dataclass
class Card:
    title: str
    icon: str
    top_text: list[str]
    body_text: list[str] = field(default_factory=lambda: ["-"])
    color: str = "dimgray"
    title_size: int = 10
    subtitle: str = "-"
    cost: str = "-"
    weight: str = "-"
    weapon_dmg: str = "-"
    weapon_dmg_type: Damage_Type = Damage_Type.unknown

    def to_dict(self) -> dict[str, Any]:
        if self.subtitle != "-":
            contents = [
                f"subtitle | {self.subtitle} | ( {self.cost})",
            ]
        else:
            contents = [
                f"subtitle | ______________________________________ | ( ______ )",
            ]
        if self.weight != "-":
            contents.append(f"subtitle | Weight: {self.weight}lb")
        else:
            contents.append(f"subtitle | Weight: ______lb")
        contents.append("rule")
        contents.extend(self.top_text)
        contents.append("text | ")
        contents.append("rule")
        if self.body_text == ["-"]:
            contents.extend(BLANK_BODY)
        else:
            contents.extend(self.body_text)
        return {
            "count": 1,
            "color": self.color,
            "title": self.title,
            "title_size": self.title_size,
            "icon": self.icon,
            "contents": contents,
            "tags": [self.title],
        }

    def __str__(self) -> str:
        return str(self.to_dict())


def process_db_to_cards(db: list[dict[str, Any]]) -> list[Card]:
    cards: list[Card] = []
    for entry in db:
        top_text: list[str] = []
        subtitle: str = "-"
        properties: list[str] = ["text | "]
        icon = entry["icon"]
        body_text = ["-"]
        if "ac" in entry:
            ac = entry["ac"]
        else:
            ac = "_______"
        if entry["type"] == "Weapon":
            # if blank template
            if entry["name"] == "Weapon":
                top_text = [
                    "property | Damage | _________________",
                    "property | Type | Bludgeoning ☐ / Piercing ☐ / Slashing ☐",
                    "property | Properties | _______________________________________",
                    "property | Ranged | ☐ ( ______ / ______ )",
                ]
                # not a blank template
            else:
                if "simple" in entry["properties"]:
                    subtitle = "Simple Weapon"
                if "martial" in entry["properties"]:
                    subtitle = "Martial Weapon"
                top_text = [
                    f"property | Damage | {entry['weapon_dmg']}",
                    f"property | Type | {entry['weapon_dmg_type'].title()}",
                ]
                if entry["name"] != "-":
                    for prop in entry["properties"].split(","):
                        prop = prop.strip()
                        if prop in ("simple", "martial"):
                            continue
                        prop = prop.title()
                        prop = prop.replace("-", "_")
                        top_text.append(f"property | {prop.replace('_', ' ')} |")
                        if "Range" in prop:
                            prop_e = "Range"
                        else:
                            prop_e = prop.title()
                        properties.append(
                            f"property | {prop.replace('_', ' ')} | "
                            + Property[f"{prop_e}"].value
                        )
                        body_text = ["NONE"]
        elif entry["type"] == "Armor":
            if entry["armor_type"] == "Light Armor":
                properties.append(
                    "property | Don | "
                    + Don_Doff.light.value[0]
                    + " &mdash; "
                    + Property.Don.value
                )
                properties.append(
                    "property | Doff | "
                    + Don_Doff.light.value[1]
                    + " &mdash; "
                    + Property.Doff.value
                )
            elif entry["armor_type"] == "Medium Armor":
                properties.append(
                    "property | Don | "
                    + Don_Doff.medium.value[0]
                    + " &mdash; "
                    + Property.Don.value
                )
                properties.append(
                    "property | Doff | "
                    + Don_Doff.medium.value[1]
                    + " &mdash; "
                    + Property.Doff.value
                )
            elif entry["armor_type"] == "Heavy Armor":
                properties.append(
                    "property | Don | " + Don_Doff.heavy.value[0] + Property.Don.value
                )
                properties.append(
                    "property | Doff | " + Don_Doff.heavy.value[1] + Property.Doff.value
                )
            # if blank template
            if entry["description"] == "-":
                top_text = [
                    f"property | AC | _______",
                    "property | Heavy | ☐ | Strength required | ☐ _______",
                    "property | Stealth | Disadvantage ☐",
                ]
            # not a template
            else:
                top_text = [f"property | AC | {ac}"]
                if entry["armor_strength"] != "-":
                    top_text.append(
                        "property | Heavy | | Strength required | "
                        f" {entry['armor_strength']}"
                    )
                    properties.append("property | Heavy | " + Property.Heavy.value)
                if "cumbersome" in entry["properties"]:
                    top_text.append(f"property | Cumbersome |")
                    properties.append(
                        "property | Cumbersome | " + Property.Cumbersome.value
                    )
                subtitle = entry["armor_type"]
        elif entry["type"] == "Shield":
            top_text = [f"property | AC | {ac}"]
            subtitle = ""
        elif entry["type"] == "Tool":
            if entry["name"] != "Tool":
                subtitle = ""
            else:
                top_text = [
                    "property | Properties | _______________________________________",
                    "property | Properties | _______________________________________",
                ]
        elif entry["type"] == "Item":
            if entry["name"] != "Item":
                entry["description"] = " "
                subtitle = ""
            else:
                top_text = [
                    "property | Properties | _______________________________________",
                    "property | Properties | _______________________________________",
                    "property | Properties | _______________________________________",
                    "property | Properties | _______________________________________",
                ]
        else:
            raise ValueError(f"could not find matching icon for: {entry['type']}")
        if body_text == ["NONE"]:
            body_text = properties
        elif entry["description"] == "-":
            body_text = ["-"]
        else:
            body_text = ["text | " + "<em>" + entry["description"] + "</em>"]
            body_text.extend(properties)
        cards.append(
            Card(
                title=entry["name"],
                icon=icon,
                top_text=top_text,
                body_text=body_text,
                subtitle=subtitle,
                cost=entry["cost"],
                weight=entry["weight"],
            )
        )

    return cards


if __name__ == "__main__":
    cards: list[dict[str, Any]] = []
    for card in process_db_to_cards(get_db()):
        cards.append(card.to_dict())
    # Serializing json
    json_object = json.dumps(cards, indent=4, ensure_ascii=False)
    with Path(SCRIPT_ROOT / "test.json").open("w", encoding="utf8") as file:
        file.write(json_object)

    # main()
