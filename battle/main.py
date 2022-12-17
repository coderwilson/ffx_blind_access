import logging

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import battle.utils
import logs
import memory.main
import vars
import xbox
from memory.main import s32
from players import (
    Auron,
    Bahamut,
    CurrentPlayer,
    Kimahri,
    Lulu,
    Rikku,
    Tidus,
    Valefor,
    Wakka,
    Yuna,
)
from players.rikku import omnis_items

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)


def _navigate_to_position(position, battle_cursor=memory.main.battle_cursor_2):
    while battle_cursor() == 255:
        pass
    if battle_cursor() != position:
        logger.debug(f"Wrong position targeted {battle_cursor() % 2}, {position % 2}")
        while battle_cursor() % 2 != position % 2:
            if battle_cursor() < position:
                xbox.tap_right()
            else:
                xbox.tap_left()
        while battle_cursor() != position:
            logger.debug(f"Battle_cursor: {battle_cursor()}")
            if battle_cursor() > position:
                xbox.tap_up()
            else:
                xbox.tap_down()


def tap_targeting():
    logger.debug(
        f"In Tap Targeting. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
    )
    while (not memory.main.main_battle_menu()) and memory.main.battle_active():
        xbox.tap_b()
    logger.debug(
        f"Done. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
    )


def use_skill(position: int = 0, target: int = 20):
    logger.debug(f"Using skill in position: {position}")
    while memory.main.battle_menu_cursor() != 19:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 19:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(position)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if target != 20 and memory.main.get_enemy_current_hp()[target - 20] != 0:
        direction = "l"
        while memory.main.battle_target_id() != target:
            if direction == "l":
                xbox.tap_left()
                if memory.main.battle_target_id() < 20:
                    xbox.tap_right()
                    direction = "d"
            else:
                xbox.tap_down()
                if memory.main.battle_target_id() < 20:
                    xbox.tap_up()
                    direction = "l"
    tap_targeting()


def use_special(position, target: int = 20, direction: int = "u"):
    logger.debug(f"Using skill in position: {position}")
    while memory.main.battle_menu_cursor() != 20:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(position)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    if memory.main.battle_target_id() != target:
        while memory.main.battle_target_id() != target:
            if direction == "r":
                xbox.tap_right()
                if memory.main.battle_target_id() < 20:
                    xbox.tap_left()
                    direction = "u"
            else:
                xbox.tap_up()
                if memory.main.battle_target_id() < 20:
                    xbox.tap_down()
                    direction = "r"
    tap_targeting()


def remedy(character: int, direction: str):
    logger.debug("Remedy")
    if memory.main.get_throw_items_slot(15) < 250:
        itemnum = 15
    else:
        itemnum = -1
    if itemnum > 0:
        _use_healing_item(character, direction, itemnum)
        return 1
    else:
        logger.debug("No restorative items available")
        return 0


def revive(item_num=6, report_for_rng=False):
    logger.debug("Using Phoenix Down")
    if memory.main.get_throw_items_slot(item_num) > 250:
        CurrentPlayer().attack()
        return
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 1:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    item_pos = memory.main.get_throw_items_slot(item_num)
    _navigate_to_position(item_pos)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    tap_targeting()


def revive_target(item_num=6, target=0):
    direction = "l"
    logger.debug("Using Phoenix Down")
    if memory.main.get_throw_items_slot(item_num) > 250:
        flee_all()
        return
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 1:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    item_pos = memory.main.get_throw_items_slot(item_num)
    _navigate_to_position(item_pos)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    # Select target - default to Tidus
    if memory.main.battle_target_id() != 0:
        while memory.main.battle_target_id() != 0:
            if direction == "l":
                xbox.tap_left()
                if memory.main.battle_target_id() >= 20:
                    xbox.tap_right()
                    direction = "u"
            else:
                xbox.tap_up()
                if memory.main.battle_target_id() >= 20:
                    xbox.tap_down()
                    direction = "l"
    tap_targeting()


def revive_all():
    revive(item_num=7)


def _print_confused_state():
    logger.debug("Confused states:")
    logger.debug(f"Yuna confusion: {memory.main.state_confused(1)}")
    logger.debug(f"Tidus confusion: {memory.main.state_confused(0)}")
    logger.debug(f"Kimahri confusion: {memory.main.state_confused(3)}")
    logger.debug(f"Auron confusion: {memory.main.state_confused(2)}")
    logger.debug(f"Lulu confusion: {memory.main.state_confused(5)}")



def escape_with_xp():
    rikku_item = False
    if memory.main.get_item_slot(39) > 200:
        flee_all()
    else:
        while not memory.main.turn_ready():
            pass
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                if Tidus.is_turn():
                    if not rikku_item:
                        Tidus.swap_battle_armor(ability=[0x8028])
                        screen.await_turn()
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().attack()
                elif Rikku.is_turn():
                    if not rikku_item:
                        use_item(memory.main.get_use_items_slot(39))
                        rikku_item = True
                    else:
                        CurrentPlayer().defend()
                elif Auron.is_turn():
                    CurrentPlayer().attack()
                else:
                    buddy_swap(Tidus)
    wrap_up()


def fullheal(target: int, direction: str):
    logger.info("Full Heal function")
    if memory.main.get_throw_items_slot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif memory.main.get_throw_items_slot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif memory.main.get_throw_items_slot(3) < 255:
        itemnum = 3
        itemname = "Mega-Potion"
        target = 255
    else:
        itemnum = -1
        itemname = "noitemfound"

    if itemnum >= 0:
        logger.debug(f"Using item: {itemname}")
        _use_healing_item(target, direction, itemnum)
        return 1
    else:
        logger.warning("No restorative items available")
        return 0


def use_item(slot: int, direction="none", target=255, rikku_flee=False):
    logger.debug("Using items via the Use command")
    logger.debug(f"Item slot: {slot}")
    logger.debug(f"Direction: {direction}")
    while not memory.main.main_battle_menu():
        pass
    logger.debug("Mark 1, turn is active.")
    while memory.main.battle_menu_cursor() != 20:
        if not Rikku.is_turn() and not Kimahri.is_turn():
            return
        if memory.main.battle_menu_cursor() in [0, 19]:
            xbox.tap_down()
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.main_battle_menu():
        xbox.tap_b()
    if rikku_flee:
        logger.debug("Mark 2, selecting 'Use' command in position 2")
    else:
        logger.debug("Mark 2, selecting 'Use' command in position 1")
    if rikku_flee:
        _navigate_to_position(2)
    else:
        logger.debug("Mark 2, selecting 'Use' command in position 1")
        _navigate_to_position(1)
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    logger.debug("Mark 3, navigating to item slot")
    _navigate_to_position(slot, memory.main.battle_cursor_3)
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    if target != 255:
        try:
            logger.debug("Targetting based on character number")
            if target >= 20 and memory.main.get_enemy_current_hp()[target - 20] != 0:
                direction = "l"
                while memory.main.battle_target_id() != target:
                    if memory.main.battle_target_id() < 20:
                        xbox.tap_right()
                        direction = "u"
                    elif direction == "u":
                        xbox.tap_up()
                    else:
                        xbox.tap_left()
            elif target < 20 and target != 0:
                direction = "l"
                while memory.main.battle_target_id() != target:
                    if memory.main.battle_target_id() >= 20:
                        xbox.tap_right()
                        direction = "u"
                    elif direction == "u":
                        xbox.tap_up()
                    else:
                        xbox.tap_left()
            elif target == 0:
                direction = "l"
                while memory.main.battle_target_id() != 0:
                    if memory.main.battle_target_id() >= 20:
                        xbox.tap_right()
                        direction = "u"
                    elif direction == "u":
                        xbox.tap_up()
                    else:
                        xbox.tap_left()

            tap_targeting()
        except Exception:
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
    elif direction == "none":
        logger.debug("No direction variation")
        tap_targeting()
    else:
        logger.debug(f"Direction variation: {direction}")
        if direction == "left":
            xbox.tap_left()
        elif direction == "right":
            xbox.tap_right()
        elif direction == "up":
            xbox.tap_up()
        elif direction == "down":
            xbox.tap_down()
        tap_targeting()

def cheer():
    logger.debug("Cheer command")
    while memory.main.battle_menu_cursor() != 20:
        if not Tidus.is_turn():
            return
        if memory.main.battle_menu_cursor() == 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(1)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    tap_targeting()


def seymour_spell(target_face=True):
    logger.debug("Seymour casting tier 2 spell")
    num = 21  # Should be the enemy number for the head
    if not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
        screen.await_turn()

    while memory.main.battle_menu_cursor() != 21:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.main_battle_menu():
        xbox.tap_b()  # Black magic
    logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
    _navigate_to_position(5)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    if (
        target_face and memory.main.get_enemy_current_hp()[1] != 0
    ):  # Target head if alive.
        while memory.main.battle_target_id() != num:
            xbox.tap_left()

    tap_targeting()


def _use_healing_item(num=None, direction="l", item_id=0):
    logger.debug(f"Healing character, {num}")
    direction = direction.lower()
    while not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 1:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    while not memory.main.other_battle_menu():
        pass
    logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
    logger.debug(
        f"get_throw_items_slot({item_id}): {memory.main.get_throw_items_slot(item_id)}"
    )
    _navigate_to_position(memory.main.get_throw_items_slot(item_id))
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if num is not None:
        while memory.main.battle_target_id() != num:
            if direction == "l":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_right()
                    direction = "u"
                else:
                    xbox.tap_left()
            elif direction == "r":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong character targeted.")
                    xbox.tap_left()
                    direction = "d"
                else:
                    xbox.tap_right()
            elif direction == "u":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong character targeted.")
                    xbox.tap_down()
                    direction = "l"
                else:
                    xbox.tap_up()
            elif direction == "d":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong character targeted.")
                    xbox.tap_up()
                    direction = "r"
                else:
                    xbox.tap_down()
    tap_targeting()


def use_potion_character(num, direction):
    logger.debug(f"Healing character, {num}")
    _use_healing_item(num=num, direction=direction, item_id=0)


def attack(direction="none"):
    logger.debug("Attack")
    direction = direction.lower()
    if not memory.main.turn_ready():
        while not memory.main.turn_ready():
            pass
    while memory.main.main_battle_menu():
        if not memory.main.battle_menu_cursor() in [0, 203, 210, 216]:
            logger.debug(f"Battle Menu Cursor: {memory.main.battle_menu_cursor()}")
            xbox.tap_up()
        elif screen.battle_complete():
            return
        else:
            xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if direction == "right":
        xbox.tap_right()
    if direction == "r2":
        xbox.tap_right()
        xbox.tap_right()
    if direction == "r3":
        xbox.tap_right()
        xbox.tap_right()
        xbox.tap_right()
    if direction == "up":
        xbox.tap_up()
    if direction == "down":
        xbox.tap_down()
    tap_targeting()


def _steal(direction=None):
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    while memory.main.battle_menu_cursor() != 20:
        if Rikku.is_turn():
            Rikku.navigate_to_battle_menu(20)
        elif Kimahri.is_turn():
            Kimahri.navigate_to_battle_menu(20)
        else:
            return
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(0)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the Steal
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    if direction == "down":
        xbox.tap_down()
    elif direction == "up":
        xbox.tap_up()
    elif direction == "right":
        xbox.tap_right()
    elif direction == "left":
        xbox.tap_left()
    logger.debug("Firing steal")
    tap_targeting()


def steal():
    logger.debug("Steal")
    if memory.main.get_encounter_id() in [273, 281]:
        _steal("left")
    elif memory.main.get_encounter_id() in [276, 279, 289]:
        _steal("up")
    else:
        _steal()


def steal_down():
    logger.debug("Steal Down")
    _steal("down")


def steal_up():
    logger.debug("Steal Up")
    _steal("up")


def steal_right():
    logger.debug("Steal Right")
    _steal("right")


def steal_left():
    logger.debug("Steal Left")
    _steal("left")


# move to battle.aeon
def aeon_summon(position):
    logger.debug(f"Summoning Aeon {position}")
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 23:
        if not Yuna.is_turn():
            return
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif (
            memory.main.battle_menu_cursor() >= 1
            and memory.main.battle_menu_cursor() < 23
        ):
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    while position != memory.main.battle_cursor_2():
        logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
        if memory.main.battle_cursor_2() < position:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.other_battle_menu():
        xbox.tap_b()

    with logging_redirect_tqdm():
        fmt = "Waiting for Aeon's turn... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            while not memory.main.turn_ready():
                pbar.update()


def heal_up(chars=3, *, full_menu_close=True):
    logger.info(f"Menuing, healing characters: {chars}")
    if memory.main.get_hp() == memory.main.get_max_hp():
        logger.debug("No need to heal. Exiting menu.")
        logger.debug(memory.main.menu_number())
        if full_menu_close:
            memory.main.close_menu()
        else:
            if memory.main.menu_open():
                memory.main.back_to_main_menu()
        return
    if not memory.main.menu_open():
        memory.main.open_menu()
    FFXC.set_neutral()
    while memory.main.get_menu_cursor_pos() != 2:
        logger.debug(f"Selecting Ability command - {memory.main.get_menu_cursor_pos()}")
        memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 2, 11)
    while memory.main.menu_number() == 5:
        logger.debug(f"Select Ability - {memory.main.menu_number()}")
        xbox.tap_b()
    logger.debug("Mark 1")
    target_pos = Yuna.main_menu_index()
    logger.debug(f"Target pos: {target_pos}")
    while memory.main.get_char_cursor_pos() != target_pos:
        memory.main.menu_direction(
            memory.main.get_char_cursor_pos(),
            target_pos,
            len(memory.main.get_order_seven()),
        )
    logger.debug("Mark 2")
    while memory.main.menu_number() != 26:
        if memory.main.get_menu_2_char_num() == 1:
            xbox.tap_b()
        else:
            xbox.tap_down()
    while not memory.main.cure_menu_open():
        xbox.tap_b()
    character_positions = {
        0: memory.main.get_char_formation_slot(0),  # Tidus
        1: memory.main.get_char_formation_slot(1),  # Yuna
        2: memory.main.get_char_formation_slot(2),  # Auron
        3: memory.main.get_char_formation_slot(3),  # Kimahri
        4: memory.main.get_char_formation_slot(4),  # Wakka
        5: memory.main.get_char_formation_slot(5),  # Lulu
        6: memory.main.get_char_formation_slot(6),  # Rikku
    }
    logger.debug(f"Character positions: {character_positions}")
    positions_to_characters = {
        val: key for key, val in character_positions.items() if val != 255
    }
    logger.debug(f"Positions to characters: {positions_to_characters}")
    maximal_hp = memory.main.get_max_hp()
    logger.debug(f"Max HP: {maximal_hp}")
    current_hp = memory.main.get_hp()
    for cur_position in range(len(positions_to_characters)):
        while (
            current_hp[positions_to_characters[cur_position]]
            < maximal_hp[positions_to_characters[cur_position]]
        ):
            logger.debug(f"Current hp: {current_hp}")
            while memory.main.assign_ability_to_equip_cursor() != cur_position:
                if memory.main.assign_ability_to_equip_cursor() < cur_position:
                    xbox.tap_down()
                else:
                    xbox.tap_up()
            xbox.tap_b()
            current_hp = memory.main.get_hp()
        if current_hp == maximal_hp or memory.main.get_yuna_mp() < 4:
            break
    logger.debug("Healing complete. Exiting menu.")
    logger.debug(memory.main.menu_number())
    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()


def lancet_swap(direction):
    logger.debug("Lancet Swap function")
    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    buddy_swap(Kimahri)

    lancet(direction)

    screen.await_turn()
    flee_all()


def lancet(direction):
    logger.debug(f"Casting Lancet with variation: {direction}")
    while memory.main.battle_menu_cursor() != 20:
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    _navigate_to_position(0)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if direction == "right":
        xbox.tap_right()
    if direction == "up":
        xbox.tap_up()
    if direction == "down":
        xbox.tap_down()
    tap_targeting()


def lancet_target(target, direction):
    logger.debug(f"Casting Lancet with variation: {direction}")
    while memory.main.battle_menu_cursor() != 20:
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    while memory.main.other_battle_menu():
        xbox.tap_b()
    retry = 0
    if memory.main.get_enemy_current_hp()[target - 20] != 0:
        # Only lancet living targets.
        while memory.main.battle_target_id() != target:
            if direction == "l":
                if retry > 5:
                    retry = 0
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_right()
                    direction = "u"
                    retry = 0
                else:
                    xbox.tap_left()
            elif direction == "r":
                if retry > 5:
                    retry = 0
                    logger.debug("Wrong character targeted.")
                    xbox.tap_left()
                    direction = "d"
                else:
                    xbox.tap_right()
            elif direction == "u":
                if retry > 5:
                    retry = 0
                    logger.debug("Wrong character targeted.")
                    xbox.tap_down()
                    direction = "l"
                else:
                    xbox.tap_up()
            elif direction == "d":
                if retry > 5:
                    retry = 0
                    logger.debug("Wrong character targeted.")
                    xbox.tap_up()
                    direction = "r"
                else:
                    xbox.tap_down()
            retry += 1

    tap_targeting()


def lancet_home(direction):
    logger.debug("Lancet (home) function")
    while memory.main.battle_menu_cursor() != 20:
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    _navigate_to_position(2)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if direction == "right":
        xbox.tap_right()
    if direction == "up":
        xbox.tap_up()
    if direction == "down":
        xbox.tap_down()
    tap_targeting()


def flee_all():
    logger.debug("Attempting escape (all party members and end screen)")
    if memory.main.battle_active():
        while not memory.main.battle_complete():
            if memory.main.user_control():
                return
            if memory.main.turn_ready():
                tidus_position = memory.main.get_battle_char_slot(0)
                logger.debug(f"Tidus Position: {tidus_position}")
                if Tidus.is_turn():
                    Tidus.flee()
                elif tidus_position >= 3 and tidus_position != 255:
                    buddy_swap(Tidus)
                elif (
                    not check_tidus_ok()
                    or tidus_position == 255
                    or memory.main.tidus_escaped_state()
                ):
                    escape_one()
                else:
                    CurrentPlayer().defend()
    logger.info("Flee complete")


def escape_all():
    logger.info("escape_all function")
    while not screen.battle_complete():
        if memory.main.turn_ready():
            escape_one()


def escape_action():
    while memory.main.main_battle_menu():
        if memory.main.battle_complete():
            break
        else:
            xbox.tap_right()
    logger.debug("In other battle menu")
    while memory.main.battle_cursor_2() != 2:
        if memory.main.battle_complete():
            break
        else:
            xbox.tap_down()
    logger.debug("Targeted Escape")
    while memory.main.other_battle_menu():
        if memory.main.battle_complete():
            break
        else:
            xbox.tap_b()
    if memory.main.battle_active():
        logger.debug("Selected Escaping")
        tap_targeting()


def escape_one():
    next_action_escape = rng_track.next_action_escape(
        character=memory.main.get_current_turn()
    )
    logger.debug(f"The next character will escape: {next_action_escape}")
    if not next_action_escape and not memory.main.get_encounter_id() == 26:
        if memory.main.get_story_progress() < 154:
            logger.debug("Character cannot escape (Lagoon). Attacking instead.")
            CurrentPlayer().attack()
        else:
            logger.debug("Character will not escape. Looking for a replacement.")
            replacement = 255
            replace_array = memory.main.get_battle_formation()
            for i in range(len(replace_array)):
                if replacement != 255:
                    pass
                elif (
                    i == 3
                    and memory.main.rng_seed() == 31
                    and memory.main.get_story_progress() < 865
                ):
                    pass
                elif replace_array[i] == 255:
                    pass
                elif replace_array[i] in memory.main.get_active_battle_formation():
                    pass
                elif rng_track.next_action_escape(replace_array[i]):
                    logger.debug(f"Character {replace_array[i]} can escape. Swapping.")
                    replacement = replace_array[i]
                    buddy_swap_char(replacement)
                    return escape_one()
                else:
                    pass
            if replacement == 255:
                logger.debug("No character could be found.")
                if memory.main.get_current_turn() == 0:
                    Tidus.flee()
                    return False
                elif memory.main.get_current_turn() == 1:
                    escape_action()
                else:
                    CurrentPlayer().attack(
                        target_id=memory.main.get_current_turn(), direction_hint="u"
                    )
                    return False
    else:
        escape_action()
        logger.debug("Attempting escape, one person")
        return True


def buddy_swap(character):
    logger.debug(f"Swapping {character} (in battle)")
    position = character.battle_slot()

    if position < 3:
        logger.debug(
            f"Cannot swap with {character}, that character is in the front party."
        )
        return
    else:
        while not memory.main.other_battle_menu():
            xbox.l_bumper()
        position -= 3
        reserveposition = position % 4
        logger.debug(f"Character is in reserve position {reserveposition}")
        if reserveposition == 3:  # Swap with last slot
            direction = "up"
        else:
            direction = "down"

        while reserveposition != memory.main.battle_cursor_2():
            if direction == "down":
                xbox.tap_down()
            else:
                xbox.tap_up()

        while memory.main.other_battle_menu():
            xbox.tap_b()
        xbox.click_to_battle()
        screen.await_turn()
        return


def buddy_swap_char(character):
    # This is a temporary hotfix, to be removed once this function is deprecated.
    if isinstance(character, int):
        if character == 0:
            return buddy_swap(Tidus)
        elif character == 1:
            return buddy_swap(Yuna)
        elif character == 2:
            return buddy_swap(Auron)
        elif character == 3:
            return buddy_swap(Kimahri)
        elif character == 4:
            return buddy_swap(Wakka)
        elif character == 5:
            return buddy_swap(Lulu)
        elif character == 6:
            return buddy_swap(Rikku)
    return buddy_swap(character)


def wrap_up():
    # When memory.main.battle_wrap_up_active() is working, we want
    # to pivot to that method instead.
    if memory.main.battle_active():
        while memory.main.battle_value() != 0:
            if memory.main.turn_ready():
                return False
        
    logger.debug("Wrapping up battle.")
    while not memory.main.battle_wrap_up_active():
        if memory.main.user_control():
            return False
        elif memory.main.menu_open():
            return False
        elif memory.main.diag_skip_possible():
            return False
    memory.main.wait_frames(1)
    while memory.main.battle_wrap_up_active():
        FFXC.set_value('btn_b', 1)
    FFXC.set_value('btn_b', 0)
    logger.debug("Wrap up complete.")
    memory.main.wait_frames(1)
    return True


def check_petrify():
    # This function is always returning as if someone is petrified, needs review.
    for iter_var in range(7):
        logger.debug(f"Checking character {iter_var} for petrification")
        if memory.main.state_petrified(iter_var):
            logger.debug(f"Character {iter_var} is petrified.")
            return True
    logger.debug("Everyone looks good - no petrification")
    return False


def check_petrify_tidus():
    return memory.main.state_petrified(0)


def rikku_od_items(slot):
    _navigate_to_position(slot, battle_cursor=memory.main.rikku_od_cursor_1)


def rikku_full_od(battle):
    # First, determine which items we are using
    if battle == "tutorial":
        item1 = memory.main.get_item_slot(73)
        logger.debug(f"Ability sphere in slot: {item1}")
        item2 = item1
    elif battle == "Evrae":
        if game_vars.skip_kilika_luck():
            item1 = memory.main.get_item_slot(81)
            logger.debug(f"Lv1 sphere in slot: {item1}")
            item2 = memory.main.get_item_slot(84)
            logger.debug(f"Lv4 sphere in slot: {item2}")
        else:
            item1 = memory.main.get_item_slot(94)
            logger.debug(f"Luck sphere in slot: {item1}")
            item2 = memory.main.get_item_slot(100)
            logger.debug(f"Map in slot: {item2}")
    elif battle == "Flux":
        item1 = memory.main.get_item_slot(35)
        logger.debug(f"Grenade in slot: {item1}")
        item2 = memory.main.get_item_slot(85)
        logger.debug(f"HP Sphere in slot: {item2}")
    elif battle == "trio":
        item1 = 108
        item2 = 108
        logger.debug(f"Wings are in slot: {item1}")
    elif battle == "crawler":
        item1 = memory.main.get_item_slot(30)
        logger.debug(f"Lightning Marble in slot: {item1}")
        item2 = memory.main.get_item_slot(85)
        logger.debug(f"Mdef Sphere in slot: {item2}")
    elif battle == "spherimorph1":
        item1 = memory.main.get_item_slot(24)
        logger.debug(f"Arctic Wind in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Def Sphere in slot: {item2}")
    elif battle == "spherimorph2":
        item1 = memory.main.get_item_slot(32)
        logger.debug(f"Fish Scale in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Sphere in slot: {item2}")
    elif battle == "spherimorph3":
        item1 = memory.main.get_item_slot(30)
        logger.debug(f"Lightning Marble in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Sphere in slot: {item2}")
    elif battle == "spherimorph4":
        item1 = memory.main.get_item_slot(27)
        logger.debug(f"Bomb Core in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Sphere in slot: {item2}")
    elif battle == "bfa":
        item1 = memory.main.get_item_slot(35)
        logger.debug(f"Grenade in slot: {item1}")
        item2 = memory.main.get_item_slot(85)
        logger.debug(f"HP Sphere in slot: {item2}")
    elif battle == "shinryu":
        item1 = memory.main.get_item_slot(109)
        logger.debug(f"Gambler's Spirit in slot: {item1}")
        item2 = memory.main.get_item_slot(58)
        logger.debug(f"Star Curtain in slot: {item2}")
    elif battle == "omnis":
        both_items = omnis_items()
        logger.debug("Omnis items, many possible combinations.")
        item1 = memory.main.get_item_slot(both_items[0])
        item2 = memory.main.get_item_slot(both_items[1])

    if item1 > item2:
        item3 = item1
        item1 = item2
        item2 = item3

    # Now to enter commands

    while not memory.main.other_battle_menu():
        xbox.tap_left()

    while not memory.main.interior_battle_menu():
        xbox.tap_b()
    rikku_od_items(item1)
    while not memory.main.rikku_overdrive_item_selected_number():
        xbox.tap_b()
    rikku_od_items(item2)
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    tap_targeting()


def check_character_ok(char_num):
    if char_num not in memory.main.get_active_battle_formation():
        return True
    return not any(
        func(char_num)
        for func in [
            memory.main.state_petrified,
            memory.main.state_confused,
            memory.main.state_dead,
            memory.main.state_berserk,
            memory.main.state_sleep,
        ]
    )


def check_tidus_ok():
    return check_character_ok(0)


def check_rikku_ok():
    return check_character_ok(6)


# unused
def check_yuna_ok():
    return check_character_ok(1)


def get_digit(number, n):
    return number // 10**n % 10


def calculate_spare_change_movement(gil_amount):
    if gil_amount > memory.main.get_gil_value():
        gil_amount = memory.main.get_gil_value()
    # gil_amount = min(gil_amount, 100000)
    position = {}
    gil_copy = gil_amount
    for index in range(0, 7):
        amount = get_digit(gil_amount, index)
        if amount > 5:
            gil_amount += 10 ** (index + 1)
        position[index] = amount
    logger.debug(position)
    for cur in range(6, -1, -1):
        if not position[cur]:
            continue
        while memory.main.spare_change_cursor() != cur:
            memory.main.side_to_side_direction(
                memory.main.spare_change_cursor(), cur, 6
            )
        target = position[cur]
        while get_digit(memory.main.spare_change_amount(), cur) != target:
            if target > 5:
                xbox.tap_down()
            else:
                xbox.tap_up()
        if memory.main.spare_change_amount() == gil_copy:
            return
    return


def charge_rikku_od():
    logger.debug(f"Battle Number: {memory.main.get_encounter_id()}")
    if not Rikku.has_overdrive() and memory.main.get_encounter_id() in [
        360,
        361,
        376,
        378,
        381,
        384,
        386,
    ]:
        if (
            not Tidus.escaped() and not Tidus.is_status_ok()
        ) or not Rikku.is_status_ok():
            logger.debug("Tidus or Rikku incapacitated, fleeing")
            logger.debug(f"{not Tidus.escaped()}")
            logger.debug(f"{not Tidus.is_status_ok()}")
            logger.debug(f"{not Rikku.is_status_ok()}")
            flee_all()
        else:
            while not memory.main.battle_complete():
                if memory.main.turn_ready():
                    if Rikku.is_turn():
                        Rikku.attack(target_id=Rikku, direction_hint="u")
                    elif Rikku.has_overdrive():
                        flee_all()
                    elif not Rikku.active():
                        buddy_swap(Rikku)
                    else:
                        escape_one()
        memory.main.click_to_control_3()
    else:
        flee_all()


def faint_check_with_escapes():
    faints = 0
    for x in range(3):
        if memory.main.get_active_battle_formation()[x] == 255:
            pass
        elif memory.main.state_dead(memory.main.get_active_battle_formation()[x]):
            faints += 1
    return faints


def check_gems():
    gem_slot = memory.main.get_item_slot(34)
    if gem_slot < 200:
        gems = memory.main.get_item_count_slot(gem_slot)
    else:
        gems = 0

    gem_slot = memory.main.get_item_slot(28)
    if gem_slot < 200:
        gems += memory.main.get_item_count_slot(gem_slot)
    logger.debug(f"Total gems: {gems}")
    return gems

