"""
Pool of 100 authentic, engaging gaming video titles for ASK Gaming YouTube Studio cards.
"""

GAMING_TITLES_POOL = [
    # Anno 1800 & Strategy / City Builders (matching uploaded assets)
    "Building a 200,000 Inhabitant Metropolis! Anno 1800 Timelapse",
    "The Most Efficient Harbor Setup You've Ever Seen (Anno 1800)",
    "Hardcore Mode: Turning a Desert Island into a Mega Empire",
    "Ultimate Trade Route Automation Guide (100% Efficiency)",
    "100 Hours in Anno 1800: From Wooden Huts to Skyscrapers",
    "My Industrial Empire Hit Max Efficiency! Full Tour",
    "Can We Survive the Naval Blockade? Hardcore Island Defense",
    "Building the World Fair Monument from Scratch (Full Guide)",
    "How to Manage 500+ Ships Without Going Insane",
    "The Perfect Farm Layout for Infinite Production & Supply",
    "Max Population Challenge: 500k Citizens on One Island!",
    "Massive Drydock Shipyard Built in Hardcore Mode",
    "I Spent 24 Hours Optimizing Electricity Grid Layouts",
    "Conquering the Entire New World in 50 Days",
    "The Ultimate Tourist Paradise Island Build",
    "From Bankruptcy to 100 Million Coins in Anno 1800",
    "Steamship Fleet vs Pirate Armada: Epic Naval Battle",
    "Building the Greenest Eco City in Strategy History",
    "Is This the Most Satisfying City Builder Layout Ever?",
    "Rebuilding London in 1800: Master Plan Timelapse",

    # GTA & Open World Action
    "GTA 6 Map Secrets: 15 Hidden Locations You Completely Missed",
    "I Bought Every Supercar in GTA Online (2026 Edition)",
    "Surviving a 5-Star Police Chase with Only a Bicycle",
    "The Most Insane Stunt Jump in GTA History",
    "GTA 6 Leaks Breakdown: New Weapons & Physics Engine",
    "Testing Every Heist Method: What Pays the Most?",
    "Driving Across the Entire Map Without Damaging My Car",
    "100 Players Hide and Seek in Los Santos",
    "We Recreated Fast & Furious in GTA 5!",
    "Busting 25 Myths in GTA Online (It Actually Worked?!)",

    # FPS & Tactical Shooters (Valorant, CS2, CoD, Apex)
    "Unbeaten 15 Win Streak to Radiant Rank (Full Solo Queue)",
    "Zero Recoil Meta Weapon Class Setup After Update",
    "Insane 1v4 Last Second Clutch in Championship Match",
    "I 1v1'd the #1 Ranked Player in the World",
    "Top 10 Secret Peeks and Lineups Nobody is Using",
    "From Iron to Immortal in 30 Days (Rank Up Journey)",
    "Testing the New Sniper Rifle: Is It Completely Broken?",
    "Settings That Made My Aim 10x More Accurate",
    "They Thought I Was Cheating with This 1v5 Ace!",
    "The Worst Teammates vs The Best Opponents (Ranked Comedy)",
    "Why Every Pro is Using This Secret Keybind",
    "Clutching with 1 HP Left to Win the Tournament!",
    "Secret Smoke Lineups That Guarantee You Win Every Round",
    "Using Only Pistols to Hit Diamond Rank Challenge",
    "The Ultimate Aim Training Routine (10 Minutes a Day)",

    # Minecraft & Survival
    "I Survived 100 Days in Ultra Hardcore Minecraft",
    "Building a Mega Cyberpunk City in Survival Mode",
    "Finding the Rarest Structure in Minecraft (0.0001% Chance)",
    "I Trapped 100 Players in a Giant Maze",
    "Automating Every Single Item in Minecraft Survival",
    "Minecraft but the World Expands Every 60 Seconds",
    "I Built an Underground Vault that Cannot Be Destroyed",
    "1,000 Days in Hardcore Minecraft: The Ultimate World Tour",
    "Beating Minecraft without Taking Any Damage",
    "The Most Beautiful Nether Base You Have Ever Seen",

    # Souls-like & RPGs (Elden Ring, Black Myth, Witcher, Cyberpunk)
    "Beating the Hardest Boss with Level 1 Gear Only",
    "The Most Overpowered Build in the Entire Game",
    "Secret Boss Hidden Behind 3 Invisible Walls!",
    "100% Completionist Guide: Every Weapon & Armor",
    "Can You Beat the Game Using Only Magic Spells?",
    "I Broke the Game with This Infinite Damage Glitch",
    "Exploring the Creepiest Dungeon in the Game",
    "Top 5 Most Emotional Gaming Endings of All Time",
    "Every Secret Location You Missed in the DLC",
    "Is This the Hardest Difficulty Ever Made in Gaming?",

    # Horror & Story Games (featuring ASK Horror archives)
    "ASK Horror: The Secret Truth Archive Revealed",
    "This Horror Game Made Me Turn Off My Computer",
    "We Explored the Abandoned Asylum at Midnight",
    "The Scariest Easter Egg Hidden in Plain Sight",
    "Don't Play This Game Alone in the Dark! (Nightmare Mode)",
    "Solving the 10-Year-Old Gaming Mystery (Solved at Last)",
    "Escaping the Haunted Bunker on Nightmare Difficulty",
    "The Real Story Behind the Creepiest Game Monster",
    "I Survived the Horror Entity for 24 Hours",
    "Uncovering the Darkest Secret in Gaming History",

    # Racing & Simulator Games
    "Drifting Down Akina Mountain at 200 MPH (Assetto Corsa)",
    "I Spent $5,000 on a Sim Racing Rig to Test This",
    "Can a Gamer Drive a Real F1 Car? Full Test",
    "Surviving the Deadliest Flight Sim Storm (Turbulence Max)",
    "Building the Most Realistic Train Route in the World",
    "The Ultimate Realistic Mod Pack for Forza Horizon",
    "Nürburgring Lap Record Broken by 3 Seconds!",
    "Testing 0 to 400 KPH on Every Hypercar in the Game",
    "Realistic Truck Simulator: 2,000 Mile Cargo Delivery",
    "Building a Dream Garage from 0 Credits",

    # Esports & Challenge Videos
    "Spending 24 Hours in VR without Taking the Headset Off",
    "I Gave a Noob Pro Equipment: Did They Get Better?",
    "The $10,000 Gaming Tournament Finals (Down to 1 Point!)",
    "Playing with Inverted Controls for an Entire Week",
    "We Built a Real Life Video Game Map in the Desert",
    "Can You Beat the Game in Under 15 Minutes? (Speedrun)",
    "I Played Against AI Bot on Impossible Mode",
    "Reacting to My First Ever YouTube Gaming Video (Cringe)",
    "The Evolution of Graphics from 1995 to 2026",
    "Top 10 Greatest Comebacks in Esports History",
    "I Spent 100 Hours Building a Functional Roller Coaster",
    "Beating the Impossible Parkour Map Without Dying",
    "The Ultimate Hardcore City Defense: Anno 1800 Masterclass",
    "Finding the Secret Easter Egg Game Developers Hid for 15 Years",
    "Can We Survive the Final Wave? Hardcore Survival Strategy"
]

def get_random_cards(count: int = 3, exclude_titles: list = None) -> list:
    """Returns random gaming card items with titles, times, and metrics."""
    import random
    exclude = set(exclude_titles or [])
    available = [t for t in GAMING_TITLES_POOL if t not in exclude]
    if len(available) < count:
        available = GAMING_TITLES_POOL
    selected_titles = random.sample(available, count)
    return selected_titles
