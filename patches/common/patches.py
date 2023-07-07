from rom.rom import snes_to_pc

patches = {
    "Removes_Gravity_Suit_heat_protection": {
        0x06e37d: [0x01],
        0x0869dd: [0x01]},
    "No_Music":{
        0x278413: [0x6f]},
    # vanilla data to restore setup asm for plandos
    "Escape_Animals_Disable": {
        0x79867: [0xb2, 0x91],
        0x798dc: [0xbb, 0x91]
    },
    # with animals suprise make the bomb blocks at alcatraz disapear with event "Zebes timebomb set" instead of "critters escaped"
    "Escape_Animals_Change_Event": {
        0x023B0A: [0x0E]
    },
    "LN_Chozo_SpaceJump_Check_Disable": {
        0x2518f: [0xea, 0xea, 0xea, 0xea, 0xea, 0xea, 0xea, 0xea]
    },
    "LN_PB_Heat_Disable": {
        0x18878: [0x80, 0x00]
    },
    "LN_Firefleas_Remove_Fune": {
        0x10ABC2: [0xff, 0x7f, 0xff, 0x7f],
    },
    "WS_Main_Open_Grey": {
        0x10BE92: [0x0]
    },
    "WS_Save_Active": {
        0x7ceb0: [0xC9]
    },
    "WS_Etank": {
        0x7cc4d: [0x37, 0xc3],
        0x7cbfb: [0x23, 0xc3]
    },
    "Phantoon_Eye_Door":{
        0x7CCAF: [0x91, 0xC2]
    },
    # has to be applied along with WS_Main_Open_Grey
    "Sponge_Bath_Blinking_Door": {
        0x7C276: [0x0C],
        0x10CE69: [0x00]
    },
    "Infinite_Space_Jump": {
        0x82493: [0x80, 0x0D]
    },
    "SpriteSomething_Disable_Spin_Attack": {
        0xD93FE: [0x0, 0x0]
    },
    "Ship_Takeoff_Disable_Hide_Samus": {
        0x112B13: [0x6B]
    },
    # Climb always in "zebes asleep" state, except during escape
    # (for escape peek in Crateria-less minimizer with disabled Tourian)
    'Climb_Asleep': {
        # replace "zebes awake" event ID with an unused event
        0x796CC: [0x7F],
        # put "Statues Hall" tension music
        0x796D6: [0x04]
    },
    # cancels the gamestate change by new_game.asm
    "Restore_Intro": {
        0x16EDA: [0x1E]
    }
}

additional_PLMs = {}
