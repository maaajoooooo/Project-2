import requests 
import random

#1 Fetch Data
# Input the Pokemon name 
pokemon_name = input("Enter a Pokemon name: ") 

#Make a GET request to the pokeapi 
response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}") 

 # Check if the response is successful 
if response.status_code == 200: 
    # Get the HP and weight from the response JSON 
    hp = response.json()["stats"][0]["base_stat"] 
    weight = response.json()["weight"] 
    
    # Print the results 
    print(f"I choose {pokemon_name.capitalize()}. It`s HP is {hp} and weight is {weight/10} kg.") 
else: 
    # Print an error message if the response is unsuccessful 
    print("Error: Pokemon not found.")

# Make a GET request to the PokeAPI to fetch Pokemon data 
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}" 
response = requests.get(url) 
# If the response is successful (status code 200), fetch the data 
if response.status_code == 200:    
    data = response.json()  

#2b Moves
# Get the first 5 moves of the Pokemon     
moves = data["moves"][:5]

# Print the names of the moves     
print(f"{pokemon_name.capitalize()} has the following moves:")     
for move in moves:
    print(move["move"]["name"]) 

#3b evolution
# Function to get the evolution chain URL of a Pokemon 
def get_evolution_chain_url(pokemon_name):     
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"     
    response = requests.get(url)     
    if response.status_code == 200:         
        species_data = response.json()         
        return species_data["evolution_chain"]["url"]    
    else:
     return None 
     
# Function to get the evolution chain of a Pokemon 
def get_evolution_chain(pokemon_name):     
    evolution_chain_url = get_evolution_chain_url(pokemon_name)     
    if evolution_chain_url is not None:        
         response = requests.get(evolution_chain_url)         
         if response.status_code == 200:             
             evolution_chain = response.json()             
             return evolution_chain    
    return None 
     
# Function to check if a Pokemon can evolve and return its evolution name 
def get_evolution(pokemon_name):     
    evolution_chain = get_evolution_chain(pokemon_name)     
    if evolution_chain is not None:         
        species_data = evolution_chain["chain"]        
        if len(species_data["evolves_to"]) > 0:             
            evolution_name = species_data["evolves_to"][0]["species"]["name"]             
            return evolution_name     
        return "This Pokemon cannot evolve."

evolution = get_evolution(pokemon_name) 
print(f"{pokemon_name.title()} evolves into {evolution.title()}.")

#3c Fight
# Set up opponent Pokemon with random HP and moves
opponent_name = input("Choose your oponent: ")
opponent_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{opponent_name}")
opponent_hp = opponent_response.json()["stats"][0]["base_stat"]
opponent_moves = opponent_response.json()["moves"][:5]

print(f"A wild {opponent_name.capitalize()} appears!")


# If the response is successful (status code 200), fetch the data
if opponent_response.status_code == 200:    
    opponent_data = opponent_response.json()  

# Get the first 5 moves of the opponent    
opponent_moves = [move["move"]["name"] for move in opponent_data["moves"][:5]]
options = ["scratch", "swords-dance", "cut", "take-down", "leer"]

# Choose random moves for both Pokemon
opponent_move = random.choice(opponent_moves)

# Get the HP and weight of the Pokemon
hp = data["stats"][0]["base_stat"]
weight = data["weight"]


# Initialize starting HP for both Pokemon
pokemon_hp = hp
opponent_hp = opponent_data["stats"][0]["base_stat"]

# Start the fight
print(f"{pokemon_name.capitalize()} will now fight {opponent_data['name'].capitalize()}.")

while True:
    # Pokemon attacks opponent
    random_option = random.choice(options)
    damage = random.randint(1, 20)
    opponent_hp -= damage
    print(f"{pokemon_name.capitalize()} attacks {opponent_data['name'].capitalize()} with {random_option}.")
    print(f"{opponent_data['name'].capitalize()} loses {damage}HP. It now has {opponent_hp}HP left.")

    # Check if opponent has fainted
    if opponent_hp <= 0:
        print(f"{pokemon_name.capitalize()} wins!")
        break
   
    # Opponent attacks Pokemon
    damage = random.randint(1, 20)
    pokemon_hp -= damage
    print(f"{opponent_data['name'].capitalize()} attacks {pokemon_name.capitalize()} with {opponent_move}.")
    print (f"{pokemon_name.capitalize()} loses {damage}HP. It now has {pokemon_hp}HP.")
    # Check if Pokemon has fainted
    if pokemon_hp <= 0:
        print(f"{opponent_data['name'].capitalize()} wins!")
        break
