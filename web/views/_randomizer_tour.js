window.PATCHES = {
  layoutPatches: {
    door_indicators_plms: {
      title: 'Flashing Doors',
      description: 'Show the color of a locked door from the other side.',
    },
    dachora: {
      title: 'Dachora',
      description: 'Disable respawning blocks in the [[Dachora Room]]',
    },
    early_super_bridge: {
      title: 'Early Supers',
      description: 'Add shot blocks to [[Early Supers Room] to escape without items.',
    },
    high_jump: {
      title: 'Hi Jump',
      description: 'Replace bomb blocks with shot blocks in [[Hi Jump Energy Tank Room]]',
    },
    moat: {
      title: 'Moat',
      description: 'Replace bomb blocks with shot blocks at [[The Moat]]',
    },
    spospo_save: {
      title: 'SpoSpo Save',
      description: 'Spore Spawn save station is always available',
    },
    nova_boost_platform: {
      title: 'Nova Boost',
      description: 'Get though [[Cathedral Entrance]] without Hi Jump',
    },
    red_tower: {
      title: 'Red Tower',
      description: 'Always be able to get back up from bottom [[Red Tower]]',
    },
    spazer: {
      title: 'Spazer',
      description: 'Replace bomb block with shot block in [[Below Spazer]]',
    },
    climb_supers: {
      title: 'Climb',
      description: 'Replace [[Climb]] Supers exit bomb block with a shot block',
    },
    brinstar_map_room: {
      title: 'Brinstar Map',
      description: 'Remove grey door in [[Brinstar Pre-Map Room]]',
    },
    kraid_save: {
      title: 'Kraid Save',
      description: '',
    },
    mission_impossible: {
      title: 'Mission Impossible',
      description: 'Replace bomb block with shot block in [[Pink Brinstar Power Bomb Room]]',
    },
  },
  areaLayout: {
    area_rando_gate_crab_tunnel: {
      description: 'Remove green gate in [[Crab Tunnel]]',
      title: 'Crab Tunnel Gate',
    },
    area_rando_gate_greenhillzone: {
      description: 'Remove blue gate in [[Green Hill Zone]]',
      title: 'Green Hill Gate',
    },
    greenhill_walljump: {
      description: 'Door access in [[Green Hill Zoone]]',
      title: 'Green Hill Ledge',
    },
    area_layout_crab_hole: {
      description: 'Rearrange blocks in [[Crab Hole]] for grav-less access',
      title: 'Crab Hole',
    },
    aqueduct_bomb_blocks: {
      description: 'Replace [[Aqueduct]] power-bomb blocks with bomb blocks',
      title: 'Aqueduct Blocks',
    },
    area_layout_caterpillar: {
      description: 'Remove green gate in [[Red Tower Elevator Room]] and makes the access point more visible.',
      images: ['fish_access_gate.png', 'fish_access_wall.png',],
      title: 'Red Tower Gate',
    },
    area_layout_east_tunnel: {
      description: 'Remove green gate in [[East Tunnel]] and unhides the ceilling access.',
      images: ['tube_access_gate.png', 'tube_access_ceiling.png'],
      title: 'East Tunnel Gate',
    },
    area_layout_single_chamber: {
      description: 'Remove crumble blocks in [[Single Chambler]] and makes the hidden LN entrance more visible',
      title: 'Single Chamber Crumble',
      images: ['ln_access_crumble.png', 'ln_access_wall.png'],
    },
    east_ocean: {
      description: 'Open door to [[Sponge Bath]] and add two platforms to [[East Ocean]] (allows access only hi-jump boots)',
      images: ['east_ocean_door.png', 'east_ocean_island.png'],
      title: 'East Ocean',
    },
  },
  variaTweaks: {
    bomb_torizo: {
      description: "The statuse in [[Bomb Torizo Room]] is activated by picking up the item he's holding (normally activated if/when you have bombs)",
      title: 'Bomb Torizo',
    },
    WS_Etank: {
      description: 'Places the item in [[Wrecked Ship Energy Tank Room]] and turns the upper door in [[Electric Death Room]] red before the ship is activated.',
      title: 'WS Energy',
    },
    LN_Chozo: {
      description: 'Activate the statue in the [[Acid Statue Room]] before space jump has been found and adds a platform for easy access.',
      title: 'Acid Statue',
    },
  }
}


// I might eventually update this to work with super metroid icons
const applyMarkdown = (s) => s.replace(
  /\[\[([^\]]+)\]\]/g,
  (_, b) => `<a
    href="https://wiki.supermetroid.run/${b.replace(/ /g,'_')}"
    target="_blank"
  >
    ${b}
  </a>`,
)

const startCase = (s) => s.replace(/_/g, ' ').replace(
    /\w\S*/g,
    (txt) => txt.charAt(0).toUpperCase() + txt.slice(1),
);

Object.entries(window.PATCHES).forEach(
  ([patch_group, patches]) => {
    Object.entries(patches).forEach(([key, options]) => {
      options.patch_group = patch_group
      options.images = options.images || [key+'.png']
    })
  }
)
