from tkinter import *
import memory.tkinter
from memory.tkinter import (
    base_process_ptr,
    
    get_story_progress,
    battle_active,
    battle_type,
    get_encounter_id,
    turn_ready,
    get_current_turn,
    battle_wrap_up_active,
    get_map,
    
    user_control,
    get_coords,
    get_gil_value,
    menu_open,
    rng_seed
)
from random import randint
import time
memory.tkinter.start()

root = Tk()
root.geometry("800x600+10+20")
root.title('aVIna_FFX_status_window')
lab = Label(root)
lab.pack()

process_val = Entry(root, text=base_process_ptr(), bd=7, state='disabled')
process_val.pack()

story_int = Entry(root, text=get_story_progress(), bd=5, state='disabled')
story_int.pack()

v1 = bool(battle_active())
battle_active_var = Checkbutton(root, text = "Battle Active", variable = v1, state='disabled')
battle_active_var.pack()

destroy_button=Button(root, text="Destroy This Window", command=root.destroy)
destroy_button.pack()

def update():
    
   story_int['text'] = get_story_progress()
   root.after(100, update) # run itself again after 1000 ms

# run first time
update()

root.mainloop()


quit()