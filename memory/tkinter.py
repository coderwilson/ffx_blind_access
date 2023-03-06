import ctypes
import ctypes.wintypes
import logging
import os.path
import struct
import time
from collections import Counter
from math import cos, sin
from typing import List

from ReadWriteMemory import Process, ReadWriteMemory, ReadWriteMemoryError
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

# Process Permissions
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

MAX_PATH = 260

base_value = 0


class LocProcess(Process):
    def __init__(self, *args, **kwargs):
        super(LocProcess, self).__init__(*args, **kwargs)

    def read_bytes(self, lp_base_address: int, size: int = 4):
        """
        See the original ReadWriteMemory values for details on how this works. This version allows us to pass
        the number of bytes to be retrieved instead of a static 4-byte size. Default is 4 for reverse-compatibility
        """
        try:
            read_buffer = ctypes.c_uint()
            lp_buffer = ctypes.byref(read_buffer)
            lp_number_of_bytes_read = ctypes.c_ulong(0)
            ctypes.windll.kernel32.ReadProcessMemory(
                self.handle, lp_base_address, lp_buffer, size, lp_number_of_bytes_read
            )
            return read_buffer.value
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                "msg": str(error),
                "Handle": self.handle,
                "PID": self.pid,
                "Name": self.name,
                "ErrorCode": self.error_code,
            }
            ReadWriteMemoryError(error)

    def write_bytes(self, lp_base_address: int, value: int, size: int = 4) -> bool:
        """
        Same as above, write a passed number of bytes instead of static 4 bytes. Default is 4 for reverse-compatibility
        """
        try:
            write_buffer = ctypes.c_uint(value)
            lp_buffer = ctypes.byref(write_buffer)
            lp_number_of_bytes_written = ctypes.c_ulong(0)
            ctypes.windll.kernel32.WriteProcessMemory(
                self.handle,
                lp_base_address,
                lp_buffer,
                size,
                lp_number_of_bytes_written,
            )
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                "msg": str(error),
                "Handle": self.handle,
                "PID": self.pid,
                "Name": self.name,
                "ErrorCode": self.error_code,
            }
            # ReadWriteMemoryError(error)


class FFXMemory(ReadWriteMemory):
    def __init__(self, *args, **kwargs):
        super(FFXMemory, self).__init__(*args, **kwargs)
        self.process = LocProcess()

    def get_process_by_name(self, process_name: str | bytes) -> "Process":
        """
        :description: Get the process by the process executabe\'s name and return a Process object.

        :param process_name: The name of the executable file for the specified process for example, my_program.exe.

        :return: A Process object containing the information from the requested Process.
        """
        if not process_name.endswith(".exe"):
            self.process.name = process_name + ".exe"

        process_ids = self.enumerate_processes()

        for process_id in process_ids:
            self.process.handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION, False, process_id
            )
            if self.process.handle:
                image_file_name = (ctypes.c_char * MAX_PATH)()
                if (
                    ctypes.windll.psapi.GetProcessImageFileNameA(
                        self.process.handle, image_file_name, MAX_PATH
                    )
                    > 0
                ):
                    filename = os.path.basename(image_file_name.value)
                    if filename.decode("utf-8") == process_name:
                        self.process.pid = process_id
                        self.process.name = process_name
                        return self.process
                self.process.close()

        raise ReadWriteMemoryError(f'Process "{self.process.name}" not found!')


def start():
    global process
    global x_ptr
    global y_ptr
    global coords_counter
    coords_counter = 0
    success = False

    # rwm = ReadWriteMemory()
    rwm = FFXMemory()
    print(type(rwm))
    process = rwm.get_process_by_name("FFX.exe")
    print(type(process))
    process.open()

    global base_value
    try:
        from memory import root_mem

        print("Process Modules:")
        base_value = root_mem.list_process_modules(process.pid)
        print("Process Modules complete")
        print(f"Dynamically determined memory address: {hex(base_value)}")
        success = True
    except Exception as err_code:
        print(
            f"Could not get memory address dynamically. Error code: {err_code}"
        )
        base_value = 0x00FF0000
        time.sleep(10)
    return success


def base_process_ptr():
    global process
    return process


def float_from_integer(integer):
    return struct.unpack("!f", struct.pack("!I", integer))[0]


def rng_seed():
    if int(game_vars.confirmed_seed()) == 999:
        global base_value
        key = base_value + 0x003988A5
        return process.read_bytes(key, 1)
    return int(game_vars.confirmed_seed())


def battle_active() -> bool:
    global base_value
    if game_over():
        return False
    key = base_value + 0x00D2A8E0
    value = process.read_bytes(key, 1)
    if value == 0:
        return False
    return True


def battle_wrap_up_active():
    # Not working yet, this memory value does not trigger after-battle screens
    global base_value
    key = base_value + 0x014408AC
    value = process.read_bytes(key, 4) & 0x20000
    if value >= 1:
        return True
    return False


def get_current_turn():
    return get_turn_by_index(turn_index=0)


def battle_menu_cursor():
    global base_value
    if not turn_ready():
        return 255
    key2 = base_value + 0x00F3C926
    return process.read_bytes(key2, 1)


def turn_ready():
    global base_value
    key = base_value + 0x01FCC08C
    if process.read_bytes(key, 4) == 0:
        return False
    else:
        # while not main_battle_menu():
        #    pass
        wait_frames(1)
        if game_vars.use_pause():
            wait_frames(2)
        return True


def user_control():
    global base_value
    # Auto updating via reference to the base_value above
    control_struct = base_value + 0x00F00740
    in_control = process.read(control_struct)

    if in_control == 0:
        return False
    else:
        return True


def get_coords():
    global process
    global base_value
    global x_ptr
    global y_ptr
    global coords_counter
    coords_counter += 1
    x_ptr = base_value + 0x0084DED0
    y_ptr = base_value + 0x0084DED8
    coord_1 = process.get_pointer(x_ptr)
    x = float_from_integer(process.read(coord_1))
    coord_2 = process.get_pointer(y_ptr)
    y = float_from_integer(process.read(coord_2))

    return [x, y]


def get_encounter_id():
    global base_value

    key = base_value + 0x00D2A8EC
    formation = process.read(key)

    return formation


def get_gil_value():
    global base_value
    key = base_value + 0x00D307D8
    return process.read(key)


def battle_type():
    # 0 is normal, 1 is pre-empt, 2 is ambushed
    return read_val(0x00D2C9DC)


def get_enemy_current_hp():
    global process
    global base_value
    enemy_num = 20
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)

    while enemy_num < 27:
        offset1 = (0xF90 * enemy_num) + 0x594
        key1 = base_pointer_address + offset1
        offset2 = (0xF90 * enemy_num) + 0x5D0
        key2 = base_pointer_address + offset2
        if enemy_num == 20:
            max_hp = [process.read_bytes(key1, 4)]
            current_hp = [process.read_bytes(key2, 4)]
        else:
            next_hp = process.read_bytes(key1, 4)
            if next_hp != 0:
                max_hp.append(next_hp)
                current_hp.append(process.read_bytes(key2, 4))
        enemy_num += 1
    print(f"Enemy HP current values: {current_hp}")
    return current_hp


def get_enemy_max_hp():
    global process
    global base_value
    enemy_num = 20
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)

    while enemy_num < 25:
        offset1 = (0xF90 * enemy_num) + 0x594
        key1 = base_pointer_address + offset1
        offset2 = (0xF90 * enemy_num) + 0x5D0
        key2 = base_pointer_address + offset2
        if enemy_num == 20:
            max_hp = [process.read_bytes(key1, 4)]
            current_hp = [process.read_bytes(key2, 4)]
        else:
            if max_hp != 0:
                max_hp.append(process.read_bytes(key1, 4))
                current_hp.append(process.read_bytes(key2, 4))
        enemy_num += 1
    print(f"Enemy HP max values: {max_hp}")
    print(f"Enemy HP current values: {current_hp}")
    return max_hp


def menu_open():
    global base_value

    key = base_value + 0x00F407E4
    menu_open = process.read_bytes(key, 1)
    if menu_open == 0:
        return False
    else:
        return True


def get_story_progress():
    global base_value

    key = base_value + 0x00D2D67C
    progress = process.read_bytes(key, 2)
    return progress


def get_map():
    global base_value
    key = base_value + 0x00D2CA90
    progress = process.read_bytes(key, 2)
    return progress


def game_over():
    global base_value
    key = base_value + 0x00D2C9F1
    if process.read_bytes(key, 1) == 1:
        return True
    else:
        return False
