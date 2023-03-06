import memory.main
from memory.main import (
    get_current_turn,
    get_turn_by_index,
    get_active_battle_formation,
    battle_menu_cursor,
    battle_cursor_2,
    battle_cursor_3,
    turn_ready,
    battle_target_id,
    battle_line_target,
    battle_target_active,
    enemy_targetted,
    main_battle_menu,
    other_battle_menu,
    interior_battle_menu,
    super_interior_battle_menu,
    name_from_number,
    get_enemy_current_hp
)
from avina_event.trigger import new_event
from avina_speech.tts import speak


def perform_battle():
    describe_battle()
    last_turn = get_current_turn()
    while not battle_complete():
        curr_turn = get_current_turn()
        if turn_ready():
            last_turn = curr_turn
            actor = name_from_number(curr_turn)
            if curr_turn >= 7:
                actor = "Aeon"
            speak(f"{actor}'s turn is ready.")
            while turn_ready():
                pass  # Fill this in later.
        elif last_turn != curr_turn and curr_turn >= 20:
            last_turn = curr_turn
            speak("Enemy is taking their turn.")
            
    speak("Battle end")

def describe_battle():
    party_lineup = get_active_battle_formation()
    for i in range(len(party_lineup)):
        party_lineup[i] = name_from_number(party_lineup[i])
    party_names = ""
    for i in range(len(party_lineup)):
        if i == 2:
            party_names += " and "
        party_names += f"{party_lineup[i]}, "
    speak(f"Your active party consists of: {party_names}")
    if len(get_enemy_current_hp()) == 1:
        speak(f"You see one enemy.")
    else:
        speak(f"You see {len(get_enemy_current_hp())} enemies.")
    
    

def battle_complete():
    if memory.main.battle_complete():
        return True
    if new_event() == "story":
        return True
    return False
