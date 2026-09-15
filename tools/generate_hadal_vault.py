from pathlib import Path
import hashlib
import re

ROOT = Path("Hadal")
ROOT.mkdir(exist_ok=True)

MASTER = "HADAL - Master Concept"
CORE = "Core Gameplay Loop"
TOWN = "Hollow Shores"

anchors = {
    MASTER: """# HADAL — Master Concept

Hadal is a cooperative ocean-horror game about asymmetric teamwork, exploration, salvage, folklore, psychological pressure, and increasingly incomprehensible deep-sea phenomena.

Players begin in [[Hollow Shores]], a harbor town whose fishing economy is collapsing after the [[Last Seaman]] reportedly went mad and disappeared at sea. Crews of up to five prepare equipment, choose [[Sailor Role]] or [[Diver Role]], travel to an expedition site, recover fish, salvage, resources and artifacts, then return to improve the town and themselves.

The central rule is simple: **the deeper the crew goes, the less understandable the ocean becomes.** Early threats can be explained as weather, animals, equipment failure and folklore. Later threats challenge space, time, memory and perception.

See [[Core Gameplay Loop]], [[Depth Escalation]], [[Ocean Comprehension Curve]], [[Crew Size and Role Selection]], [[Town Financial Collapse]], and the category hubs linked below.
""",
    CORE: """# Core Gameplay Loop

[[Hollow Shores]] → prepare equipment → form a crew → choose [[Sailor Role]] and [[Diver Role]] assignments → travel to an expedition site → divers descend while sailors monitor the surface → gather fish, salvage, resources and artifacts → survive the return trip → sell, donate, research or use recovered materials → upgrade crew and town → attempt deeper expeditions.

The loop intentionally alternates safety and dread. [[Hollow Shores]] should feel familiar enough that every return from the ocean matters.
""",
    TOWN: """# Hollow Shores

Hollow Shores is the struggling harbor town at the center of Hadal. Its fishing industry is failing, money is scarce, and the disappearance of the [[Last Seaman]] hangs over the docks like a warning nobody wants to discuss plainly.

The town is both a hub and a progression system. Recovered resources can reopen businesses, repair infrastructure, unlock research, improve expedition support and reveal buried local history.

See [[Town Financial Collapse]], [[Town Recovery]], [[Last Seaman]], and [[HADAL - Master Concept]].
""",
    "Sailor Role": """# Sailor Role

Sailors remain on or near the vessel while divers descend. Their job is to keep the ship alive, watch the sea, interpret instruments, communicate with divers, manage threats, and decide when an expedition has become too dangerous.

Surface threats include dangerous animals, large debris, storms, [[Sirens]], [[False Debris]], and [[Knocker Fish]]. The sailor should never feel idle; calm periods are for preparation, observation and second-guessing.

See [[Diver Role]], [[Hired Sailor]], [[Visibility Degradation]], and [[Crew Size and Role Selection]].
""",
    "Diver Role": """# Diver Role

Divers descend below the vessel to recover resources, inspect sites, solve environmental problems and survive conditions that become less reliable with depth. Their visibility and certainty degrade before their raw movement ability does.

A diver depends on the surface crew for warnings, navigation context and extraction timing. Communication becomes a mechanic rather than flavor when the environment starts presenting false information.

See [[Sailor Role]], [[Visibility Degradation]], [[Depth Escalation]], and [[Ocean Comprehension Curve]].
""",
    "Crew Size and Role Selection": """# Crew Size and Role Selection

A run supports up to five active players. Every active crew member chooses between [[Sailor Role]] and [[Diver Role]] for that expedition. The role split is intentionally flexible: one sailor and four divers creates different risk than three sailors and two divers.

Players may hire an [[Hired Sailor]], but an NPC substitute performs worse than a coordinated human crew member.
""",
    "Hired Sailor": """# Hired Sailor

A hired sailor is an NPC crew substitute for groups that do not want to leave the surface completely unattended. It can perform routine monitoring and basic emergency actions, but its judgment, reaction time and interpretation of ambiguous threats are deliberately worse than a human player's.

The hire solves a matchmaking problem without erasing the value of the [[Sailor Role]].
""",
    "Sirens": """# Sirens

Sirens are a surface folklore threat. Their influence creates an urge that slowly pulls a sailor toward the edge of the vessel. The player must rapidly resist the urge before being dragged into a vulnerable position or overboard.

The danger should begin subtly: audio contamination, misplaced footsteps, a camera lean and incorrect distance perception before the physical pull becomes obvious.

See [[Sailor Role]] and [[Folklore Logic]].
""",
    "False Debris": """# False Debris

False Debris resembles ordinary floating wreckage at first glance but functions primarily as a warning. Its impossible repetition, wrong buoyancy or deliberate placement signals that something much larger is moving nearby.

It should reward observant sailors who notice patterns before a direct threat arrives.
""",
    "Knocker Fish": """# Knocker Fish

Knocker Fish create deliberate-sounding impacts against a hull. Early encounters can be mistaken for debris or mechanical failure; later patterns mimic knocks, codes, footsteps or crew rhythms.

Their purpose is to weaponize uncertainty on the surface and make sailors question whether a sound came from outside, inside, or below the ship.
""",
    "Last Seaman": """# Last Seaman

The last experienced seaman associated with Hollow Shores reportedly went mad before disappearing into the ocean. The public story is incomplete. His logs, routes, damaged equipment and contradictory sightings become a long-running trail through the game.

He should remain useful as a mystery even if the final answer is never perfectly clean.
""",
    "Town Financial Collapse": """# Town Financial Collapse

Hollow Shores begins in a slow economic collapse. Poor catches, damaged boats, missing crews and fear around older routes have made ordinary fishing unreliable. The player expedition program exists because conventional work is no longer enough.

This gives every recovered crate, fish haul and artifact a mundane value before it acquires a supernatural one.
""",
    "Town Recovery": """# Town Recovery

Town recovery is a communal progression layer. Players can direct money and materials toward docks, shops, navigation aids, research facilities, rescue capability and public spaces. Improvements change both convenience and story presentation.

A healthier town should also become more aware of what the crew is bringing back.
""",
    "Depth Escalation": """# Depth Escalation

Depth is not just difficulty scaling. It is a change in the rules the player believes the world follows. Shallow expeditions emphasize believable danger; mid-depth expeditions mix folklore with physical hazards; deep expeditions introduce geometry, memory and causality that cannot be trusted.

The ocean becomes less understandable farther down.
""",
    "Visibility Degradation": """# Visibility Degradation

Divers lose reliable visual information with depth, weather, sediment, biological activity and supernatural interference. Reduced visibility is strongest when it forces communication rather than simply making the screen darker.

Surface instruments may remain clear even while a diver's direct view becomes unreliable — until the instruments begin disagreeing too.
""",
    "Ocean Comprehension Curve": """# Ocean Comprehension Curve

Hadal's horror curve should move from **dangerous** → **uncanny** → **folkloric** → **impossible** → **incomprehensible**. The player should have time to build explanations, then watch those explanations fail one by one.

See [[Depth Escalation]], [[Visibility Degradation]], and [[HADAL - Master Concept]].
""",
    "Folklore Logic": """# Folklore Logic

Folklore in Hadal is strongest when old stories act like imperfect field manuals. A legend may identify a behavior correctly while being completely wrong about the creature's origin. Local superstition can therefore be mechanically useful without confirming a single mythology as literal truth.
""",
}

CATEGORIES = [
    ("01 Hollow Shores Locations","town-location",["Salt","Gull","Lantern","Rust","Black","Old","Tide","North"],["Pier","Alley","Warehouse","Yard","Slip"],"physical places inside Hollow Shores that make the town feel lived-in and economically strained"),
    ("02 Town Businesses","business",["Anchor","Brine","Mariner","Candle","Net","Harpoon","Gull","Copper"],["Market","Workshop","Cafe","Exchange","Office"],"businesses that convert expedition success into practical recovery and social change"),
    ("03 Town Infrastructure","infrastructure",["East","West","Storm","Old","Lower","Upper","Iron","Stone"],["Breakwater","Pump","Crane","Beacon","Drain"],"infrastructure whose condition affects preparation, safety, navigation or atmosphere"),
    ("04 NPCs","npc",["Mara","Elias","Nora","Silas","Ada","Jonah","Miriam","Calder"],["Vale","Rook","Morrow","Quill","Voss"],"Hollow Shores residents with routines, biases, personal stakes and imperfect knowledge of the sea"),
    ("05 Factions","faction",["Harbor","Deep","Old","Lantern","Salt","Black","Tide","Wake"],["Union","Circle","Watch","Society","Compact"],"groups competing over safety, money, research, tradition and access to recovered material"),
    ("06 Sailor Systems","sailor-system",["Watch","Bearing","Hull","Signal","Deck","Threat","Radio","Recovery"],["Routine","Protocol","Check","Cycle","Procedure"],"surface gameplay tasks that keep sailors active and make their judgment matter"),
    ("07 Diver Systems","diver-system",["Pressure","Breath","Tether","Light","Depth","Grip","Signal","Orientation"],["Routine","State","Check","Cycle","Procedure"],"underwater mechanics that turn descent into teamwork rather than a solo scavenging minigame"),
    ("08 Ship Systems","ship-system",["Primary","Backup","Storm","Deep","Emergency","Port","Starboard","Central"],["Radar","Winch","Pump","Sonar","Generator"],"ship machinery sailors monitor, repair, reroute and distrust under pressure"),
    ("09 Ship Upgrades","ship-upgrade",["Reinforced","Quiet","Long-Range","Pressure-Sealed","Stormproof","Twin","Research","Salvage"],["Hull","Array","Winch","Locker","Console"],"persistent upgrades that change expedition capability without removing uncertainty"),
    ("10 Diving Equipment","diving-equipment",["Abyssal","Compact","Emergency","Survey","Salvage","Pressure","Coldwater","Long-Dive"],["Mask","Tank","Lamp","Tether","Harness"],"diver tools whose strengths create tradeoffs in weight, noise, endurance and information"),
    ("11 Surface Equipment","surface-equipment",["Deck","Storm","Signal","Rescue","Harbor","Longwatch","Emergency","Survey"],["Flare","Hook","Lamp","Scope","Kit"],"sailor tools for observation, rescue, deterrence and crisis response"),
    ("12 Ocean Regions","ocean-region",["Ashen","Blindwater","Glass","Grave","Whisper","Iron","Pale","Black"],["Shelf","Reach","Trench","Basin","Current"],"large marine regions with distinct ecology, navigation rules and horror language"),
    ("13 Dive Sites","dive-site",["Drowned","Sunken","Broken","Silent","Flooded","Lost","Collapsed","Buried"],["Chapel","Rig","Station","Wreck","Observatory"],"specific expedition destinations that combine resources, hazards and environmental storytelling"),
    ("14 Natural Creatures","natural-creature",["Lanternjaw","Glassfin","Redeye","Needleback","Gravelmouth","Longarm","Palecrest","Hooktail"],["Grazer","Stalker","Ray","Shark","Squid"],"plausibly biological sea life that anchors early danger before the impossible becomes undeniable"),
    ("15 Folklore Creatures","folklore-creature",["Bell-Widow","Salt Bride","Net Father","Drowned Piper","Lantern Wife","Wake Child","Black Sailor","Tide Saint"],["Omen","Hunter","Caller","Watcher","Mimic"],"entities filtered through local stories, rituals and contradictory eyewitness accounts"),
    ("16 Cosmic Entities","cosmic-entity",["Listening","Unturned","Hollow","Nameless","Sleepless","Below","Folded","Last"],["Presence","Choir","Mouth","Shape","Horizon"],"late-game phenomena that attack assumptions about scale, identity, distance and cause"),
    ("17 Hazards","hazard",["Silt","Pressure","Current","Cable","Thermal","Chemical","Acoustic","Structural"],["Burst","Trap","Shear","Pocket","Failure"],"non-creature dangers that make every site risky even before supernatural escalation"),
    ("18 Weather","weather",["Knife","White","Black","Warm","Dead","Glass","Iron","Red"],["Fog","Squall","Rain","Wind","Sea"],"surface conditions that change visibility, handling, communication and threat readability"),
    ("19 Ocean Events","ocean-event",["Midnight","Sudden","False","Silent","Red","Long","Empty","Double"],["Tide","Calm","Migration","Knocking","Bloom"],"run-level events that temporarily change the ocean's behavior and force plan changes"),
    ("20 Resources","resource",["Black","Blue","Ghost","Iron","Salt","Glass","Red","Pale"],["Coral","Kelp","Resin","Pearl","Oil"],"materials gathered for sale, crafting, town recovery, research and morally questionable experiments"),
    ("21 Salvage","salvage",["Waterlogged","Crushed","Sealed","Burned","Barnacled","Military","Research","Unknown"],["Crate","Locker","Engine","Case","Beacon"],"recoverable human-made objects that tell small stories and create inventory decisions"),
    ("22 Artifacts","artifact",["Saint's","Widow's","Diver's","Seaman's","Hollow","Black","Bone","Tide"],["Compass","Bell","Coin","Lens","Key"],"rare objects whose mechanical usefulness is inseparable from disturbing provenance"),
    ("23 Economy","economy",["Fish","Salvage","Artifact","Fuel","Repair","Research","Insurance","Town"],["Price","Demand","Debt","Contract","Fund"],"economic rules that keep mundane pressure relevant beside supernatural stakes"),
    ("24 Progression","progression",["Crew","Diver","Sailor","Ship","Town","Research","Reputation","Depth"],["Rank","Milestone","Unlock","Track","Threshold"],"long-term progression that broadens choices instead of simply flattening danger"),
    ("25 Quests","quest",["Missing","Broken","Last","Silent","Black","Drowned","Unpaid","Forbidden"],["Delivery","Search","Recovery","Survey","Favor"],"missions grounded in local needs that gradually pull players toward stranger explanations"),
    ("26 Expeditions","expedition",["Shallow","Storm","Night","Long","Restricted","Emergency","Research","Salvage"],["Run","Route","Dive","Sweep","Operation"],"repeatable expedition formats with different risk, role pressure and extraction priorities"),
    ("27 Lore Records","lore-record",["Harbor","Seaman","Research","Coastguard","Church","Union","Diver","Unknown"],["Log","Ledger","Tape","Report","Letter"],"documents and recordings that reveal history through disagreement rather than exposition dumps"),
    ("28 Rumors","rumor",["Dockside","Children's","Old Crew","Fisherman's","Researcher","Drunk","Widow's","Radio"],["Warning","Story","Claim","Joke","Confession"],"small pieces of uncertain information that may foreshadow mechanics, lie, or become true later"),
    ("29 Audio Cues","audio",["Distant","Hull","Radio","Deep","Wet","Metal","Human","Impossible"],["Knock","Tone","Breath","Whistle","Pulse"],"sound motifs that carry actionable information while also undermining trust in that information"),
    ("30 Visual Motifs","visual",["Red","Black","Pale","Blue","Rust","Wet","White","Gold"],["Thread","Light","Eye","Spire","Reflection"],"recurring visual language used to build recognition before explicit explanation"),
    ("31 UI Systems","ui",["Dive","Sailor","Crew","Ship","Town","Research","Threat","Inventory"],["Panel","Overlay","Meter","Map","Prompt"],"interface systems designed to communicate pressure without making uncertainty disappear"),
    ("32 Roblox Implementation","roblox",["Server","Client","Streaming","Physics","Audio","Lighting","Network","Save"],["System","Controller","Manager","Service","Prototype"],"practical Roblox implementation notes for performance, replication, architecture and prototyping"),
    ("33 Environmental Storytelling","environmental-story",["Abandoned","Flooded","Scratched","Repaired","Burned","Sealed","Dragged","Collapsed"],["Room","Locker","Door","Wall","Shrine"],"small environmental details that imply human events without stopping play for exposition"),
    ("34 Research and Science","research",["Pressure","Biology","Acoustic","Artifact","Cognitive","Geology","Signal","Anomaly"],["Study","Trial","Model","Sample","Theory"],"research systems that turn recovered evidence into partial understanding and new risks"),
    ("35 Status Effects","status",["Nitrogen","Cold","Panic","Vertigo","Siren","Pressure","Darkness","Signal"],["Stress","Sickness","Distortion","Exposure","Lock"],"temporary conditions that alter decisions, perception or coordination rather than only draining health"),
    ("36 Town Upgrades","town-upgrade",["Restored","Expanded","Reinforced","Powered","Public","Emergency","Research","Harbor"],["Dock","Clinic","Workshop","Beacon","Office"],"visible town improvements that convert expedition loot into a changing home base"),
]

SEVERITY = ["low but persistent", "moderate", "high under bad conditions", "rare but severe", "deceptively minor"]
DETECTION = ["visual observation", "radio behavior", "sonar or instrument drift", "sound pattern recognition", "crew comparison of conflicting evidence"]
COUNTER = ["slow down and verify", "split responsibilities", "retreat before escalation", "spend a limited tool charge", "communicate a confirmation phrase", "change route rather than fight"]
REWARD = ["money and town recovery", "research value", "safer future routes", "rare crafting material", "new dialogue and rumors", "equipment access"]
SENSORY = ["a low metallic vibration", "light scattering that looks slightly delayed", "a smell of wet iron", "radio static with a human cadence", "sediment moving against the current", "a brief absence of ordinary ocean noise"]
TWISTS = ["its first explanation is usually mundane", "experienced crews notice it earlier but may overreact", "it becomes more dangerous when players stop communicating", "it is easier to survive than to correctly understand", "it can leave evidence that persists back in town", "its behavior subtly changes after deeper expeditions"]


def safe(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '-', name).strip()


def pick(seq, seed, offset=0):
    h = int(hashlib.sha1(f"{seed}:{offset}".encode()).hexdigest()[:8], 16)
    return seq[h % len(seq)]


def link(name):
    return f"[[{name}]]"


def write_note(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

# Core anchors
core_dir = ROOT / "00 Core"
for name, body in anchors.items():
    write_note(core_dir / f"{safe(name)}.md", f"---\ntype: core\ntags: [hadal, core]\n---\n\n{body}")

# Precompute all generated titles so every note can cross-link deterministically.
category_titles = []
for label, tag, prefixes, nouns, focus in CATEGORIES:
    titles = [f"{p} {n} — {label[3:]}" for p in prefixes for n in nouns]
    category_titles.append(titles)

# Main category hubs + detail notes.
for ci, (label, tag, prefixes, nouns, focus) in enumerate(CATEGORIES):
    folder = ROOT / label
    titles = category_titles[ci]
    hub_name = f"{label[3:]} Hub"
    hub_links = "\n".join(f"- {link(t)}" for t in titles)
    hub = f"""---
type: hub
category: {tag}
tags: [hadal, hub, {tag}]
---

# {hub_name}

This hub covers {focus}.

Connected upward to {link(MASTER)}, {link(CORE)}, and {link(TOWN)}.

## Notes
{hub_links}
"""
    write_note(folder / f"{safe(hub_name)}.md", hub)

    for i, title in enumerate(titles):
        prev_title = titles[(i - 1) % len(titles)]
        next_title = titles[(i + 1) % len(titles)]
        cross1 = category_titles[(ci + 1) % len(CATEGORIES)][i % 40]
        cross2 = category_titles[(ci + 7) % len(CATEGORIES)][(i * 3) % 40]
        cross3 = category_titles[(ci + 17) % len(CATEGORIES)][(i * 7) % 40]
        scale = "major" if i % 11 == 0 else ("medium" if i % 4 == 0 else "small")
        sev = pick(SEVERITY, title, 1)
        detect = pick(DETECTION, title, 2)
        counter = pick(COUNTER, title, 3)
        reward = pick(REWARD, title, 4)
        sensory = pick(SENSORY, title, 5)
        twist = pick(TWISTS, title, 6)

        body = f"""---
type: hadal-detail
category: {tag}
scope: {scale}
tags: [hadal, {tag}, scope-{scale}]
---

# {title}

**Concept:** {title} is a {scale} Hadal detail within the {label[3:]} category. It exists to support {focus}.

## Gameplay role
Its baseline pressure is **{sev}**. Players most reliably identify or understand it through **{detect}**. The intended response is usually to **{counter}**, rather than treating every problem as combat.

## Sensory identity
A recurring tell is {sensory}. {twist.capitalize()}.

## Progression value
Interacting with, surviving, repairing, studying or exploiting this detail can contribute to **{reward}**. Deeper versions should connect back to {link('Depth Escalation')} and become less certain rather than simply gaining more health.

## Connections
- Parent: {link(hub_name)}
- Core loop: {link(CORE)}
- Home base: {link(TOWN)}
- Nearby concept: {link(prev_title)}
- Nearby concept: {link(next_title)}
- Cross-system connection: {link(cross1)}
- Cross-system connection: {link(cross2)}
- Cross-system connection: {link(cross3)}
"""
        write_note(folder / f"{safe(title)}.md", body)

# Master map of content
hub_names = [f"{label[3:]} Hub" for label, *_ in CATEGORIES]
master_hubs = "\n".join(f"- {link(h)}" for h in hub_names)
root_text = f"""---
type: moc
tags: [hadal, moc]
---

# Hadal Vault Map

Start with {link(MASTER)} and {link(CORE)}.

## Core anchors
""" + "\n".join(f"- {link(k)}" for k in anchors) + f"""

## Category hubs
{master_hubs}

## Graph design
Every generated detail links to its category hub, adjacent concepts, core anchors and multiple notes in other categories. The result is one connected knowledge graph rather than isolated idea dumps.
"""
write_note(ROOT / "Hadal Vault Map.md", root_text)

count = len(anchors) + len(CATEGORIES) + sum(len(x) for x in category_titles) + 1
write_note(ROOT / "VAULT BUILD INFO.md", f"""# Vault Build Info

Generated Hadal knowledge graph.

- Core anchor notes: {len(anchors)}
- Category hubs: {len(CATEGORIES)}
- Detail notes: {sum(len(x) for x in category_titles)}
- Total Hadal notes created by this generator: {count}
- Main map: {link('Hadal Vault Map')}

The generated notes are intentionally tagged by category so Obsidian Graph Groups can color them later without editing individual files.
""")

print(f"Generated {count} interconnected Hadal notes under {ROOT}")
