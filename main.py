"""
My Pokemon game.
"""

from random import randint, choice
"""
A Player will be of type user or computer. 
You could have a user play against the computer or 
two players depending on which you instatiate.
You could also have two computer players fight.
"""


class Player():
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.choose_3_pokemon()
        self.choose_attacker()

    def __str__(self):
        return self.name

    def take_a_turn_against(self, other_player):
        print()  # skip a line to make it legible
        self.your_move(other_player)
        if not other_player.game_over():
            other_player.take_a_turn_against(self)
        else:
            show_pokemon()
            print(str(self) + " wins the game.")

    def make_a_move(self, move, other_player):
        if move == 'a':
            print(str(self) + " chooses to attack.")
            self.attack(other_player)

        elif move == 'h':
            print(str(self) + " chooses to heal " + self.attacker_name() + ".")
            self.heal()

        elif move == 's':
            print(str(self) + " chooses to switch Pokemon.")
            self.switch()

        elif move == 'p':
            # showing current Pokemon status. This doesn't cost a turn.
            show_pokemon()
            self.your_move(other_player)

        else:
            # recursively ask for a different move.
            print("I don't know that one.")
            self.your_move(other_player)

    def game_over(self):
        return (self.pokemon[0].dead() and self.pokemon[1].dead()
                and self.pokemon[2].dead())

    # Three different commands a player can choose.
    # attack and heal are redirected to the Pokemon.
    # If attacking Pokemon has been knocked out force a switch.
    # A forced switch stills costs a turn.
    def switch(self):
        self.choose_attacker()
        print(str(self) + " chooses " + self.attacker_name())

    def attack(self, other_player):
        if self.attacker.dead():
            print("Sorry " + str(self) +
                  ", your Pokemon was knocked out. You must switch.")
            self.switch()
        else:
            type = self.choose_attack()
            self.attacker.attack(type, other_player)

    def heal(self):
        if self.attacker.dead():
            print("Sorry " + str(self) +
                  ", your Pokemon was knocked out. You must switch.")
            self.switch()
        else:
            self.attacker.heal(self, 20)

    # redirect damage taken to the active Pokemon
    def fire_damage(self, damage):
        self.attacker.fire_damage(damage)

    def grass_damage(self, damage):
        self.attacker.grass_damage(damage)

    def water_damage(self, damage):
        self.attacker.water_damage(damage)

    # active Pokemon name, just the name.
    def attacker_name(self):
        return self.attacker.attacker_name()


"""
User type players will always ask for choices and commands.
"""


class User(Player):
    def your_move(self, other_player):
        print("Player " + self.name + " your move.")
        move = input("Attack (a), heal (h), switch (s) or Pokemon status (p)?")
        self.make_a_move(move, other_player)

    def choose_3_pokemon(self):
        for i in range(3):
            monster = choose_pokemon(pocket_monsters)
            self.pokemon.append(monster)
            pocket_monsters.remove(monster)

    def choose_attacker(self):
        print("Who will attack?")
        self.attacker = choose_pokemon(self.pokemon)

    def choose_attack(self):
        print("Choose your attack!")
        return choose_attack(self.attacker.attack_types())


"""
Computer players will just randomly take actions.
They might not be intelligent actions, just actions.
"""


class Computer(Player):
    def your_move(self, other_player):
        print("Player " + self.name + " next move.")
        self.make_a_move(choice(['a', 'a', 'a', 'a', 'h', 's']), other_player)

    def choose_3_pokemon(self):
        for i in range(3):
            monster = choice(pocket_monsters)
            self.pokemon.append(monster)
            pocket_monsters.remove(monster)

    def choose_attacker(self):
        self.attacker = choice(self.pokemon)
        if self.attacker.health <= 0:
            self.choose_attacker()

    def choose_attack(self):
        return choice(self.attacker.attack_types())


"""
Pokemon!!! The Pokemon class does almost everything.
Subclasses are of types grass, fire, or water.
Each type has different abilities.
"""


class Pokemon():
    def __init__(self, health, attack_power, name):
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.name = name
        self.init_attacks()

    def __str__(self):
        return (self.name + " (" + self.type + ") with health " +
                str(self.health) + " and attack " + str(self.attack_power) +
                ".")

    # just the name no stats
    def attacker_name(self):
        return self.name

    def attack_types(self):
        return self.attacks

    def dead(self):
        return self.health == 0

    # Pokemon will only heal or attack. Players must switch them.
    def heal(self, player, healing):
        self.health = min(self.health + healing, self.max_health)
        print(str(player) + " heals " + self.attacker_name() + ".")

    def attack(self, attack, other_player):
        print(self.attacker_name() + " attacking " +
              other_player.attacker_name() + " with " + attack.name + ".")
        damage = attack.calculate_damage(self.attack_power)
        self.do_damage_to(other_player, damage)

    # Rock, paper, scissors style of extra damage. Each Pokemon type is
    # stronger against one other type.
    def normal_damage(self, damage):
        self.health = max(self.health - damage, 0)
        print(str(damage) + " damage done to " + self.attacker_name())

    def extra_damage(self, amount):
        damage = round(amount * 1.5)
        self.health = max(self.health - damage, 0)
        print(
            str(damage) + " including extra damage done to " +
            self.attacker_name())

    # default is normal damage for all types of attackers
    def grass_damage(self, amount):
        self.normal_damage(amount)

    def fire_damage(self, amount):
        self.normal_damage(amount)

    def water_damage(self, amount):
        self.normal_damage(amount)


""" Grass type Pokemon has leaf attacks and is weak to fire damage."""


class GrassType(Pokemon):
    type = 'grass'

    def init_attacks(self):
        self.attacks = [
            Attack("Leaf Storm", 150, 33),
            Attack("Mega Drain", 50, 100),
            Attack("Razor Leaf", 100, 50)
        ]

    # Grass Pokemon always do grass damage
    def do_damage_to(self, other_player, amount):
        other_player.grass_damage(amount)

    # Override default to do extra damage if fire attacks me
    def fire_damage(self, amount):
        self.extra_damage(amount)


"""Water type Pokemon has water attacks and is weak to fire damage."""


class WaterType(Pokemon):
    type = 'water'

    def init_attacks(self):
        self.attacks = [
            Attack("Surf", 100, 50),
            Attack("Bubble", 50, 100),
            Attack("Hydro Pump", 200, 25)
        ]

    # Water Pokemon always do water damage
    def do_damage_to(self, other_player, amount):
        other_player.water_damage(amount)

    # Override default to do extra damage if grass attacks me
    def grass_damage(self, amount):
        self.extra_damage(amount)


"""Fire type Pokemon has fire attacks and is weak to water damage."""


class FireType(Pokemon):
    type = 'fire'

    def init_attacks(self):
        self.attacks = [
            Attack("Ember", 50, 100),
            Attack("Fire Punch", 70, 70),
            Attack("Flame Wheel", 100, 50)
        ]

    # Fire Pokemon always do fire damage
    def do_damage_to(self, other_player, amount):
        other_player.fire_damage(amount)

    # Override default to do extra damage if water attacks me
    def water_damage(self, amount):
        self.extra_damage(amount)


"""
We are going to make objects to represent attacks. 
Damage calculations and hit/miss are done here.
"""


class Attack():
    """Attacks do the damage calculation."""
    def __init__(self, name, power, accuracy):
        self.name = name
        self.power_percent = power
        self.accuracy = accuracy

    def __str__(self):
        return (self.name + " with " + str(self.power_percent) +
                "% of attack power and " + str(self.accuracy) +
                "% chance to hit.")

    def calculate_damage(self, attack_power):
        if randint(1, 100) <= self.accuracy:
            max_damage = round(attack_power * self.power_percent / 100)
            return randint(1, max_damage)
        else:
            # Ha Ha missed me
            return 0


"""
User interface functions. 
Choose a pokemon. Choose an attack.
"""


def choose_pokemon(pokemon):
    """Choose one of several Pokemon."""
    index = 1
    print("Enter the number for your pokemon choice.")
    for monster in pokemon:
        print(str(index) + ". " + str(monster))
        index = index + 1
    index = int(input("Choose? "))
    if index < 1 or index > len(pokemon):
        print("Not a valid number.")
        return choose_pokemon(pokemon)
    elif pokemon[index - 1].dead():
        print("That Pokemon is already knocked out, choose another.")
        return choose_pokemon(pokemon)
    else:
        return pokemon[index - 1]


def choose_attack(attacks):
    """Choose one of three attacks."""
    index = 1
    print("Enter the number for your attack choice.")
    for attack in attacks:
        print(str(index) + ". " + str(attack))
        index = index + 1
    index = int(input("Choose? "))
    if index < 1 or index > len(attacks):
        print("Not a valid number.")
        return choose_attack(attacks)
    else:
        return attacks[index - 1]


# a fourth command is to show the current status
def show_pokemon():
    show_title()
    print(str(user) + " attacking with " + user.attacker_name())
    print("Pokemon are:")
    for monster in user.pokemon:
        print("   " + str(monster))
    print()
    print(str(computer) + " attacking with " + computer.attacker_name())
    print("Pokemon are:")
    for monster in computer.pokemon:
        print("   " + str(monster))
    print()


def show_pikachu():
    """Some ASCII art."""
    print("""
`;-.          ___,
  `.`\_...._/`.-"`
    \        /      ,
    /()   () \    .' `-._
   |)  .    ()\  /   _.'
   \  -'-     ,; '. <
    ;.__     ,;|   > \\
   / ,    / ,  |.-'.-'
  (_/    (_/ ,;|.<`
    \    ,     ;-`
     >   \    /
    (_,-'`> .'
         (_,'
""")


def show_title():
    print("""
                                  ,'\\
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|
          """)


"""
Call start_game to initialize and get the players taking turns.
Right now we are set up for one user and one computer player.
You can change that if you want.
"""


def start_game():
    """Start the Pokemon game."""
    global pocket_monsters, user, computer
    show_pikachu()
    pocket_monsters = [
        GrassType(60, 40, 'Bulbasaur'),
        GrassType(40, 60, 'Bellsprout'),
        GrassType(50, 50, 'Oddish'),
        FireType(30, 70, 'Charmainder'),
        FireType(50, 50, 'Ninetails'),
        FireType(40, 60, 'Ponyta'),
        WaterType(80, 20, 'Squirtle'),
        WaterType(70, 30, 'Psyduck'),
        WaterType(50, 50, 'Poliwag')
    ]

    #user = Computer(input("Your name? "))
    user = Computer("Pikachu")
    computer = Computer("Lysandre")
    user.take_a_turn_against(computer)


# Get this game started.
start_game()
