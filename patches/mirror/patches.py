from rom.rom import snes_to_pc

patches = {
    'Blinking[Keyhunter Room Bottom]': {
        # door Door_0E_Room_948C_PLM_ x/y updated
        snes_to_pc(0x8f8228): [0x4e, 0xc8, 0x16, 0x2d, 0xe, 0x8c],
        snes_to_pc(0xa18f7b): [0x0],
    },
    'Blinking[Moat Right]': {
        snes_to_pc(0xa185e0): [0x0],
    },
    'Blinking[Morph Ball Room Left]': {
        # door Door_31_Room_9E9F_PLM_ x/y updated
        snes_to_pc(0x8f8746): [0x42, 0xc8, 0x7e, 0x26, 0x31, 0x8c],
        snes_to_pc(0xa193a8): [0x0],
    },
    'Blinking[Green Pirates Shaft Bottom Right]': {
        # door Door_1E_Room_99BD_PLM_ x/y updated
        snes_to_pc(0x8f8470): [0x48, 0xc8, 0x1, 0x66, 0x63, 0x8c],
        snes_to_pc(0xa18572): [0x0],
    },
    'Blinking[Lower Mushrooms Left]': {
        snes_to_pc(0xa18c0c): [0x0],
    },
    'Blinking[Golden Four]': {
        snes_to_pc(0xa19f60): [0x0],
    },
    'Blinking[Green Brinstar Elevator]': {
        snes_to_pc(0xa18585): [0x0],
    },
    'Blinking[Green Hill Zone Top Right]': {
        # door Door_30_Room_9E52_PLM_ x/y updated
        snes_to_pc(0x8f8670): [0x48, 0xc8, 0x61, 0x6, 0x63, 0x8c],
        snes_to_pc(0xa19d5b): [0x0],
    },
    'Blinking[Noob Bridge Right]': {
        # door Door_33_Room_9FBA_PLM_ x/y updated
        snes_to_pc(0x8f87a6): [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        snes_to_pc(0xa19325): [0x0],
    },
    'Blinking[Warehouse Zeela Room Left]': {
        snes_to_pc(0xa19451): [0x0],
    },
    'Blinking[KraidRoomOut]': {
        # door Door_45_Room_A56B_PLM_ x/y updated
        snes_to_pc(0x8f8a1a): [0x48, 0xc8, 0x1, 0x16, 0x63, 0x8c, 0x0, 0x0],
        snes_to_pc(0xa1a056): [0x0],
    },
    'Blinking[Warehouse Entrance Right]': {
        snes_to_pc(0xa198f6): [0x0],
    },
    'Blinking[Warehouse Entrance Left]': {
        snes_to_pc(0xa198f6): [0x0],
    },
    'Blinking[Single Chamber Top Right]': {
        snes_to_pc(0xa1b88e): [0x0],
    },
    'Blinking[Kronic Boost Room Bottom Left]': {
        # door Door_58_Room_AE74_PLM_ x/y updated
        snes_to_pc(0x8f8d4e): [0x42, 0xc8, 0xe, 0x26, 0x58, 0x8c],
        snes_to_pc(0xa1b9d7): [0x0],
    },
    'Blinking[Three Muskateers Room Left]': {
        snes_to_pc(0xa1bb0d): [0x0],
    },
    'Blinking[Lava Dive Right]': {
        snes_to_pc(0xa1ad6b): [0x0],
    },
    'Blinking[RidleyRoomOut]': {
        # door Door_5C_Room_B37A_PLM_ x/y updated
        snes_to_pc(0x8f8ea6): [0x42, 0xc8, 0x2e, 0x6, 0x63, 0x8c, 0x0, 0x0],
        snes_to_pc(0xa1b81b): [0x0],
    },
    'Blinking[West Ocean Left]': {
        snes_to_pc(0xa186f6): [0x0],
    },
    'Blinking[PhantoonRoomOut]': {
        # door Door_85_Room_CC6F_PLM_ x/y updated
        snes_to_pc(0x8fc29d): [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c, 0x0, 0x0],
        snes_to_pc(0xa1c3e5): [0x0],
        snes_to_pc(0xa1c19b): [0x0],
    },
    'Blinking[Crab Maze Left]': {
        snes_to_pc(0xa18b3a): [0x0],
    },
    'Blinking[Crab Hole Bottom Left]': {
        snes_to_pc(0xa1de59): [0x0],
    },
    'Blinking[Main Street Bottom]': {
        snes_to_pc(0xa1df2f): [0x0],
    },
    'Blinking[Red Fish Room Left]': {
        snes_to_pc(0xa1d3ec): [0x0],
    },
    'Blinking[Le Coude Right]': {
        # door Door_0F_Room_95A8_PLM_ x/y updated
        # we use yellow plm from bottom door as blinking plm for entrance door
        snes_to_pc(0x8f823e): [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        snes_to_pc(0xa185dd): [0x0],
    },
    'Blinking[DraygonRoomOut]': {
        # door Door_9B_Room_D78F_PLM_ x/y updated
        snes_to_pc(0x8fc73b): [0x42, 0xc8, 0x1e, 0x26, 0x63, 0x8c, 0x3b, 0xb6, 0x31, 0x26, 0x0, 0x0, 0x3b, 0xb6, 0x31, 0x26, 0x0, 0x0],
        snes_to_pc(0xa1d111): [0x0],
    },
    'Blinking[East Tunnel Top Right]': {
        snes_to_pc(0xa1d5e1): [0x0],
    },
    'Blinking[East Tunnel Right]': {
        snes_to_pc(0xa1d5e1): [0x0],
    },
    'Blinking[Glass Tunnel Top]': {
        snes_to_pc(0xa1d53b): [0x0],
    },
    'Blinking[Red Tower Top Left]': {
        snes_to_pc(0xa19504): [0x0],
    },
    'Blinking[Caterpillar Room Top Right]': {
        snes_to_pc(0xa1a0b9): [0x0],
    },
    'Blinking[Red Brinstar Elevator]': {
        # door Door_10_Room_962A_PLM_ x/y updated
        snes_to_pc(0x8f8256): [0x54, 0xc8, 0x6, 0x2, 0x10, 0x8c],
        snes_to_pc(0xa189f1): [0x0],
    },
    'Blinking[Crocomire Speedway Bottom]': {
        # door Door_4E_Room_A923_PLM_ x/y updated
        snes_to_pc(0x8f8b96): [0x4e, 0xc8, 0x6, 0x2d, 0x4e, 0x8c],
        snes_to_pc(0xa1aa8c): [0x0],
    },
    'Blinking[Crocomire Room Top]': {
        # door Door_4F_Room_A98D_PLM_ x/y updated
        snes_to_pc(0x8ffdeb): [0x54, 0xc8, 0xff, 0xff, 0x4f, 0x8c],
        snes_to_pc(0xa1bb30): [0x0],
    },
    'Blinking[Below Botwoon Energy Tank Right]': {
        snes_to_pc(0xa1dd9a): [0x0],
    },
    'Blinking[West Sand Hall Left]': {
        snes_to_pc(0xa1dacf): [0x0],
    },
    'Blinking[Aqueduct Top Left]': {
        snes_to_pc(0xa1d3a9): [0x0],
    },
    'Blinking[Crab Shaft Right]': {
        # door Door_8F_Room_D1A3_PLM_ x/y updated
        snes_to_pc(0x8fc4fb): [0x48, 0xc8, 0x1, 0x36, 0x8f, 0x8c],
        snes_to_pc(0xa1d005): [0x0],
    },
    'Blinking[RidleyRoomIn]': {
        # door Door_5A_Room_B32E_PLM_ x/y updated
        snes_to_pc(0x8f8e98): [0x48, 0xc8, 0xe, 0x16, 0x5a, 0x8c],
        snes_to_pc(0xa1a638): [0x0],
    },
    'Blinking[DraygonRoomIn]': {
        # door Door_9E_Room_DA60_PLM_ x/y updated
        snes_to_pc(0x8fc7bb): [0x48, 0xc8, 0x1, 0x6, 0x9e, 0x8c],
        snes_to_pc(0xa1d356): [0x0],
    },
    'Blinking[PhantoonRoomIn]': {
        # door Door_86_Room_CD13_PLM_ x/y updated
        snes_to_pc(0x8fc2b3): [0x42, 0xc8, 0xe, 0x6, 0x86, 0x8c],
        snes_to_pc(0xa1cd16): [0x0],
    },
    'Blinking[KraidRoomIn]': {
        # door Door_47_Room_A59F_PLM_ x/y updated
        snes_to_pc(0x8f8a34): [0x42, 0xc8, 0x1, 0x16, 0x47, 0x8c],
        snes_to_pc(0xa19f37): [0x0],
    },
    'Indicator[KihunterBottom]': {
        # door Door_10_Room_962A_PLM_ x/y updated
        snes_to_pc(0x8f8256): [0xff, 0xff, 0x6, 0x2, 0xe, 0x0],
    },
    'Indicator[GreenHillZoneTopRight]': {
        # door Door_31_Room_9E9F_PLM_ x/y updated
        snes_to_pc(0x8f8746): [0xff, 0xff, 0x7e, 0x26, 0x30, 0x0],
    },
    'Save_G4': {
        # 0x80c527 load point entry - x/y updated
        snes_to_pc(0x80c527): [0xed, 0xa5, 0x16, 0x92, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x58, 0x0, 0x60, 0x0],
        # TODO map icon X/Y
        snes_to_pc(0x82c86f): [0x78, 0x0, 0x48, 0x0],
    },
    'Save_Gauntlet': {
        # 0x80c519 load point entry - x/y updated
        snes_to_pc(0x80c519): [0xbd, 0x99, 0x1a, 0x8b, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x78, 0x0, 0x50, 0x0],
        # music in room state header
        snes_to_pc(0x8f99ce): [0x9],
        # TODO map icon X/Y
        snes_to_pc(0x82c86b): [0x58, 0x0, 0x18, 0x0],
    },
    'Save_Watering_Hole': {
        # 0x80c979 load point entry - x/y updated
        snes_to_pc(0x80c979): [0x3b, 0xd1, 0x98, 0xa4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x78, 0x0, 0xd0, 0xff],
        # music in room state header
        snes_to_pc(0x8fd14c): [0x1b, 0x6],
        # TODO map icon X/Y
        snes_to_pc(0x82ca0f): [0x68, 0x0, 0x28, 0x0],
    },
    'Save_Mama': {
        # 0x80c96b load point entry - x/y updated
        snes_to_pc(0x80c96b): [0x55, 0xd0, 0xe4, 0xa3, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x68, 0x0, 0xf0, 0xff],
        # music in room state header
        snes_to_pc(0x8fd066): [0x1b, 0x6],
        # TODO map icon X/Y
        snes_to_pc(0x82ca0b): [0x97, 0x0, 0x67, 0x0],
    },
    'Save_Aqueduct': {
        # 0x80c95d load point entry - x/y updated
        snes_to_pc(0x80c95d): [0xa7, 0xd5, 0xd4, 0xa7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x88, 0x0, 0x20, 0x0],
        # TODO map icon X/Y
        snes_to_pc(0x82ca07): [0xc4, 0x0, 0x50, 0x0],
    },
    'Save_Etecoons': {
        # 0x80c631 load point entry - x/y updated
        snes_to_pc(0x80c631): [0x51, 0xa0, 0x3a, 0x8f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x68, 0x0, 0xd0, 0xff],
        # music in room state header
        snes_to_pc(0x8fa062): [0xf, 0x5],
        # TODO map icon X/Y
        snes_to_pc(0x82c8d9): [0x28, 0x0, 0x58, 0x0],
    },
    'Save_Firefleas': {
        # 0x80c73b load point entry - x/y updated
        snes_to_pc(0x80c73b): [0x5a, 0xb5, 0x9e, 0x9a, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x88, 0x0, 0x0, 0x0],
        # music in room state header
        snes_to_pc(0x8fb56b): [0x18, 0x5],
        # TODO map icon X/Y
        snes_to_pc(0x82c93f): [0x28, 0x1, 0x38, 0x0],
    },
    'Save_Crab_Shaft': {
        # 0x80c995 load point entry - x/y updated
        snes_to_pc(0x80c995): [0xa3, 0xd1, 0x68, 0xa4, 0x0, 0x0, 0x0, 0x1, 0x0, 0x2, 0x88, 0x0, 0x60, 0x0],
        # TODO map icon X/Y
        snes_to_pc(0x82ca17): [0x90, 0x0, 0x50, 0x0],
    },
    'Save_Main_Street': {
        # 0x80c9a3 load point entry - x/y updated
        snes_to_pc(0x80c9a3): [0xc9, 0xcf, 0xd8, 0xa3, 0x0, 0x0, 0x0, 0x1, 0x0, 0x5, 0x88, 0x0, 0x10, 0x0],
        # TODO map icon X/Y
        snes_to_pc(0x82ca1b): [0x58, 0x0, 0x78, 0x0],
    },
    'Blinking[Climb Bottom Left]': {
        # door Door_12_Room_96BA_PLM_ x/y updated
        snes_to_pc(0x8f82fe): [0x42, 0xc8, 0x2e, 0x86, 0x12, 0x8c],
        snes_to_pc(0xa18683): [0x0],
    },
}

additional_PLMs = {
    'Morph_Zebes_Awake': {
        'room': 0x9e9f,
        'state': 0x9ecb,
        'plm_bytes_list': [
            [0xff, 0xff, 0x3a, 0x29, 0x1a, 0x0],
        ],
        'locations': [('Morphing Ball', 0)],
    },
    'WS_Map_Grey_Door': {
        'room': 0xcc6f,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x4e, 0x6, 0x61, 0x90],
        ],
    },
    'WS_Map_Grey_Door_Openable': {
        'room': 0xcc6f,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x4e, 0x6, 0x61, 0x10],
        ],
    },
    'WS_Save_Blinking_Door': {
        'room': 0xcaf6,
        'state': 0xcb08,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x11, 0x36, 0x62, 0xc],
        ],
    },
    'Maridia Sand Hall Seal': {
        'room': 0xd252,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x90],
        ],
    },
    'Save_G4': {
        'room': 0xa5ed,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x12, 0xc, 0x7, 0x0],
        ],
    },
    'Save_Gauntlet': {
        'room': 0x99bd,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x3, 0xa, 0x6, 0x0],
        ],
    },
    'Save_Watering_Hole': {
        'room': 0xd13b,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0xb, 0xa, 0x7, 0x0],
        ],
    },
    'Save_Mama': {
        'room': 0xd055,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x9, 0xb, 0x6, 0x0],
        ],
    },
    'Save_Aqueduct': {
        'room': 0xd5a7,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x6, 0x9, 0x5, 0x0],
        ],
    },
    'Save_Etecoons': {
        'room': 0xa051,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0xb, 0xb, 0x7, 0x0],
        ],
    },
    'Save_Firefleas': {
        'room': 0xb55a,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x8, 0x9, 0x7, 0x0],
        ],
    },
    'Save_Crab_Shaft': {
        'room': 0xd1a3,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x12, 0x29, 0x9, 0x0],
        ],
    },
    'Save_Main_Street': {
        'room': 0xcfc9,
        'plm_bytes_list': [
            [0x6f, 0xb7, 0x17, 0x59, 0xa, 0x0],
        ],
    },
    'Blinking[Moat Right]': {
        'room': 0x95ff,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Lower Mushrooms Left]': {
        'room': 0x9969,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x3e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Golden Four]': {
        'room': 0xa5ed,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x4e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Green Brinstar Elevator]': {
        'room': 0x9938,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Warehouse Zeela Room Left]': {
        'room': 0xa471,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x1e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Warehouse Entrance Right]': {
        'room': 0xa6a1,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x2e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Warehouse Entrance Left]': {
        'room': 0xa6a1,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Single Chamber Top Right]': {
        'room': 0xad5e,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Three Muskateers Room Left]': {
        'room': 0xb656,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x2e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Lava Dive Right]': {
        'room': 0xaf14,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[West Ocean Left]': {
        'room': 0x93fe,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x7e, 0x46, 0x63, 0x8c],
        ],
    },
    'Blinking[Crab Maze Left]': {
        'room': 0x957d,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x3e, 0x16, 0x63, 0x8c],
        ],
    },
    'Blinking[Crab Hole Bottom Left]': {
        'room': 0xd21c,
        'plm_bytes_list': [
            [0x42, 0xc8, 0xe, 0x16, 0x63, 0x8c],
        ],
    },
    'Blinking[Main Street Bottom]': {
        'room': 0xcfc9,
        'plm_bytes_list': [
            [0x4e, 0xc8, 0x16, 0x7d, 0x63, 0x8c],
        ],
    },
    'Blinking[Red Fish Room Left]': {
        'room': 0xd104,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x2e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[East Tunnel Top Right]': {
        'room': 0xcf80,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[East Tunnel Right]': {
        'room': 0xcf80,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x31, 0x16, 0x63, 0x8c],
        ],
    },
    'Blinking[Glass Tunnel Top]': {
        'room': 0xcefb,
        'plm_bytes_list': [
            [0x54, 0xc8, 0x6, 0x2, 0x63, 0x8c],
        ],
    },
    'Blinking[Red Tower Top Left]': {
        'room': 0xa253,
        'plm_bytes_list': [
            [0x42, 0xc8, 0xe, 0x46, 0x63, 0x8c],
        ],
    },
    'Blinking[Caterpillar Room Top Right]': {
        'room': 0xa322,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x36, 0x63, 0x8c],
        ],
    },
    'Blinking[Below Botwoon Energy Tank Right]': {
        'room': 0xd6fd,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[West Sand Hall Left]': {
        'room': 0xd461,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x3e, 0x6, 0x63, 0x8c],
        ],
    },
    'Blinking[Aqueduct Top Left]': {
        'room': 0xd5a7,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x5e, 0x16, 0x63, 0x8c],
        ],
    },
    'Indicator[LandingSiteRight]': {
        'room': 0x948c,
        'plm_bytes_list': [
            [0xff, 0xff, 0x2e, 0x6, 0x0, 0x0],
        ],
    },
    'Indicator[KihunterRight]': {
        'room': 0x95ff,
        'plm_bytes_list': [
            [0xff, 0xff, 0x1e, 0x6, 0xd, 0x0],
        ],
    },
    'Indicator[NoobBridgeRight]': {
        'room': 0xa253,
        'plm_bytes_list': [
            [0xff, 0xff, 0xe, 0x46, 0x33, 0x0],
        ],
    },
    'Indicator[MainShaftBottomRight]': {
        'room': 0x9cb3,
        'plm_bytes_list': [
            [0xff, 0xff, 0x6e, 0x6, 0x22, 0x0],
        ],
    },
    'Indicator[BigPinkBottomRight]': {
        'room': 0x9e52,
        'plm_bytes_list': [
            [0xff, 0xff, 0x7e, 0x6, 0x29, 0x0],
        ],
    },
    'Indicator[RedTowerElevatorLeft]': {
        'room': 0xa2f7,
        'plm_bytes_list': [
            [0xff, 0xff, 0x1, 0x6, 0x3c, 0x0],
        ],
    },
    'Indicator[WestOceanRight]': {
        'room': 0xca08,
        'plm_bytes_list': [
            [0xff, 0xff, 0x3e, 0x6, 0xc, 0x0],
        ],
    },
    'Indicator[LeCoudeBottom]': {
        'room': 0x94cc,
        'plm_bytes_list': [
            [0xff, 0xff, 0x9, 0x2, 0xf, 0x0],
        ],
    },
    'Indicator[WreckedShipMainShaftBottom]': {
        'room': 0xcc6f,
        'plm_bytes_list': [
            [0xff, 0xff, 0x29, 0x2, 0x84, 0x0],
        ],
    },
    'Indicator[CathedralEntranceRight]': {
        'room': 0xa788,
        'plm_bytes_list': [
            [0xff, 0xff, 0x2e, 0x6, 0x4a, 0x0],
        ],
    },
    'Indicator[CathedralRight]': {
        'room': 0xafa3,
        'plm_bytes_list': [
            [0xff, 0xff, 0x4e, 0x6, 0x49, 0x0],
        ],
    },
    'Indicator[RedKihunterShaftBottom]': {
        'room': 0xb5d5,
        'plm_bytes_list': [
            [0xff, 0xff, 0x9, 0x2, 0x5e, 0x0],
        ],
    },
    'Indicator[WastelandLeft]': {
        'room': 0xb62b,
        'plm_bytes_list': [
            [0xff, 0xff, 0x1, 0x6, 0x5f, 0x0],
        ],
    },
    'Indicator[MainStreetBottomRight]': {
        'room': 0xd08a,
        'plm_bytes_list': [
            [0xff, 0xff, 0x3e, 0x6, 0x8d, 0x0],
        ],
    },
    'Indicator[CrabShaftRight]': {
        'room': 0xd5a7,
        'plm_bytes_list': [
            [0xff, 0xff, 0x5e, 0x16, 0x8f, 0x0],
        ],
    },
    'Indicator[ColosseumBottomRight]': {
        'room': 0xd78f,
        'plm_bytes_list': [
            [0xff, 0xff, 0x1e, 0x6, 0x9a, 0x0],
        ],
    },
}
