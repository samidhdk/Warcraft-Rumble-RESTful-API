<h1 align="center">Unofficial Warcraft Rumble RESTful API</h1>

![title](Images/wcrumbleuoapi.jpg)

This is the unofficial Warcraft Rumble RESTful API. This project aims to deliver the basics of [Warcraft Rumble](https://warcraftrumble.blizzard.com) until [Blizzard](https://www.blizzard.com) releases their own.

All objects are returned as a JSON.

You can access the FastAPI Docs at: https://warcraftrumblejson.com/docs


--- 


## Units

Every unit has the following attributes and data types: 

| Field  | Type |
|---|---|
| id | int |
| cost | int |
| name | string |
| faction | string |
| type | string |
| description | string |
| traits | string array |
| talents | string array |
| stats | Object |

A unit is represented as: 

```json
{
    "id": 1,
    "cost": 6,
    "name": "Abomination",
    "faction": "Undead",
    "type": "Troop",
    "description": "This Tanky mass of flesh and steel will Hook ranged enemies, drawing them into his Cleave attack.",
    "traits": [
        "Tank",
        "Hook",
        "Melee",
        "AoE"
    ],
    "talents": [
        "Noxius Presence: Poison nearby enemies every 3 seconds.",
        "Cannonball: On deploy and at 50 % health, stun nearby enemies for 5 seconds.",
        "Fresh Meat: After hooking a target, deal double damage on the next attack."
    ],
    "stats": {
        "Area Damage": 170,
        "Health": 3400,
        "DPS": 68,
        "Attack Speed": 2.5,
        "Speed": "Slow"
    }
}
```

---

# Units Endpoints

All of the following endpoints live under `/units/`

## **/units/**

Retrieves a JSON file containing information about all available units.

## **/units/{id}**

Retrieves a JSON file containing information about the specified unit.

` id options: 1 - 71 `

## /units/faction/{unit_faction}

Retrieves a JSON file containing information about all units belonging to the specified faction.

**Unit faction options:**
- Alliance
- Beast
- Blackrock
- Horde
- Undead

## /units/type/{unit_type}

Retrieves a JSON file containing information about all units of the specified type.

**Unit type options:**
- leader
- spell
- troop

## /units/cost/{unit_cost}

` unit_cost options: 1 - 6 `

Retrieves a JSON file containing information about all units with the specified cost.

## **/units/traits/{unit_trait}**

Retrieves a JSON file containing information about all units with the specified trait.

(Units only have their base traits. What this means is: some units can obtain new traits if they are upgraded, for example, Cairne Bloodhoof gets the "Rebirth" trait when he has the "Reincarnation" talent. So from 4 traits, goes to 5. The database contains the **non-upgraded** units)

**Unit trait options:**
- Ambush
- AoE
- Armored
- Attack Root
- Attack Stun
- Bloodlust
- Bombard
- Cannibalize
- Carrion
- Charge
- Cheap Shot
- Cycle
- Dismounts
- Elemental
- Fast
- Fiery Weapon Enchant
- Flying
- Frost
- Fury
- Hatching
- Haunt
- Healer
- Heal Squadmate
- Healer
- Hook
- Longshot
- Melee
- Miner
- Percent Damage
- Poisonous
- Possession
- Ranged
- Rebirth
- Resistant
- Revive
- Siege Damage
- Siege Specialist
- Stealth
- One-Target
- Squad
- Stealth
- Summoner
- Tank
- Unbound
- Vulnerable

Additionally, you can include up to three additional "subtraits" for a more detailed query to retrieve all units possessing these traits.

You must use the following structure: ` /units/traits/{unit_trait}?s1={subtrait1}&s2={subtrait2}&s3={subtrait3} `



Example:  ` /units/traits/Tank?s1=Melee&s2=Fast&s3=Elemental `

Will return: 

``` json
{
    "id": 5,
    "cost": 4,
    "name": "Baron Rivendare",
    "faction": "Undead",
    "type": "Leader",
    "description": "Bane of the Scarlet Crusade.",
    "traits": [
        "Tank",
        "Armored",
        "Elemental",
        "Fast",
        "Melee",
        "One-Target"
    ],
    "talents": [
        "Death Pact: Periodically sacrifice a nearby Skeleton to be Healed.",
        "Skeletal Frenzy: Nearby allied Skeletons gain Bloodlust.",
        "Chill Of The Grave: Summon Skeletal Mages instead of Warriors."
    ],
    "stats": {
        "Damage": 190,
        "Health": 1040,
        "DPS": 112,
        "Attack Speed": 1.7,
        "Speed": "Fast"
    }
}
```

## /units/talents/{unit_id}

Retrieves a JSON string list with the 3 talents of the unit.

` id options: 1 - 71 `

## /units/stats/{unit_id}

Retrieves a JSON Object with the stats of the unit.

` id options: 1 - 71 `

Table of stats and it type:

| Stat            |   Type | Exclusive of       |
|-----------------|-------:|--------------------|
| Area Damage     | int    |                    |
| Attack Speed(*) | float  |                    |
| Bear DPS        | int    | Mountaineer        |
| Bear Dmg        | int    | Mountaineer        |
| Bear Health     | int    | Mountaineer        |
| Crash Damage    | int    | S.A.F.E Pilot      |
| DPS             | int    |                    |
| Damage          | int    |                    |
| Duration        | int    |                    |
| Dwarf DPS       | int    | Mountaineer        |
| Dwarf Dmg       | int    | Mountaineer        |
| Dwarf Health    | int    | Mountaineer        |
| Dwarf Range     | float  | Mountaineer        |
| Fan Damage      | int    | Maiev Shadowsong   |
| Gyth DPS        | int    | Rend Blackhand     |
| Gyth Dmg        | int    | Rend Blackhand     |
| Gyth Health     | int    | Rend Blackhand     |
| Gyth Range      | int    | Rend Blackhand     |
| Healing         | int    |                    |
| Health          | int    |                    |
| Left DPS        | int    | Chimaera           |
| Left Damage     | int    | Chimaera           |
| Lvl Advantage   | string |                    |
| Percent DPS     | int    | Charlga Razorflank |
| Percent Dmg     | int    | Execute            |
| Radius          | int    |                    |
| Range(*)        | float  |                    |
| Rend DPS        | int    | Rend Blackhand     |
| Rend Dmg        | int    | Rend Blackhand     |
| Rend Health     | int    | Rend Blackhand     |
| Rend Range      | int    | Rend Blackhand     |
| Right DPS       | int    | Chimaera           |
| Right Damage    | int    | Chimaera           |
| Speed           | string |                    |

(\*) Both **Attack Speed** and **Range** can have an integer value, depending on the unit. Since there is at least one unit with a float value, the type is considered as such.


# Future Updates and Feedback

This RESTful API is very likely to be updated in the future.

All the units from Season 2 onwards will be added at the end of the JSON and not alphabetically.

If you have any suggestion, feel free to contact me.

# Disclaimer

This RESTful API **is not** affiliated with or endorsed by Activision Blizzard, Inc.
