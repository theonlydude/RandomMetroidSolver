window.PATCHES = {
  layout: [
    {
      id: 'door_indicators_plms',
      title: 'Flashing Doors',
      description: 'Show the color of a locked door from the other side.',
      images: ['flashing_doors.gif'],
    },
    {
      id: 'dachora',
      title: 'Dachora',
      description: 'Disable respawning blocks in the [[Dachora Room]]',
    },
    {
      id: 'early_super_bridge',
      title: 'Early Supers',
      description: 'Add shot blocks to [[Early Supers Room]] to escape without morph.',
      images: ['early_super.png'],
    },
    {
      id: 'high_jump',
      title: 'Hi Jump',
      description: 'Replace bomb blocks with shot blocks in [[Hi Jump Energy Tank Room]]',
    },
    {
      id: 'moat',
      title: 'Moat',
      description: 'Replace bomb blocks with shot blocks at [[The Moat]]',
    },
    {
      id: 'spospo_save',
      title: 'SpoSpo Save',
      description: 'Access [[Big Pink]] save station without morph',
      images: ['spore_save.png'],
    },
    {
      id: 'nova_boost_platform',
      title: 'Nova Boost',
      description: 'Get though [[Cathedral Entrance]] without Hi Jump',
      images: ['cathedral.png'],
    },
    {
      id: 'red_tower',
      title: 'Red Tower',
      description: 'Always be able to get back up from bottom [[Red Tower]]',
    },
    {
      id: 'spazer',
      title: 'Spazer',
      description: 'Replace bomb block with shot block in [[Below Spazer]]',
      images: ['spazer_block.png'],
    },
    {
      id: 'climb_supers',
      title: 'Climb',
      description: 'Replace [[Climb]] Supers exit bomb block with a shot block',
    },
    {
      id: 'brinstar_map_room',
      title: 'Brinstar Map',
      description: 'Remove grey door in [[Brinstar Pre-Map Room]]',
      images: ['bt_map.png'],
    },
    {
      id: 'kraid_save',
      title: 'Kraid Save',
      description: 'Replace the bomb block in the [[Warehouse Kihunter Room]] with a shot block',
    },
    {
      id: 'mission_impossible',
      title: 'Mission Impossible',
      description: 'Replace bomb block with shot block in [[Pink Brinstar Power Bomb Room]]',
    },
  ],
  areaLayout: [
    {
      id: 'area_rando_gate_crab_tunnel',
      description: 'Remove green gate in [[Crab Tunnel]]',
      title: 'Crab Tunnel Gate',
      images: ['crab_gate.png'],
    },
    {
      id: 'area_layout_crab_hole',
      description: 'Rearrange blocks in [[Crab Hole]] for grav-less access',
      title: 'Crab Hole',
      images: ['crab_hole.png'],
    },
    {
      id: 'area_rando_gate_greenhillzone',
      description: 'Remove blue gate in [[Green Hill Zone]] and make meme route wall jump easier',
      title: 'Green Hill Gate',
      images: ['greenhill_gate.png', 'greenhill_walljump.png'],
    },
    {
      id: 'aqueduct_bomb_blocks',
      description: 'Replace [[Aqueduct]] power-bomb blocks with bomb blocks',
      title: 'Aqueduct Blocks',
    },
    {
      id: 'area_rando_gate_caterpillar',
      description: 'Remove the green gate in the [[Caterpillar Room]]',
      title: 'Red Tower Gate',
      images: ['fish_gate.png'],
    },
    {
      id: 'area_layout_caterpillar',
      description: 'Access maridia entrance in the [[Caterpillar Room]]',
      images: ['fish_access.png',],
      title: 'Red Tower Access',
    },
    {
      id: 'area_rando_gate_east_tunnel',
      description: 'Remove green gate in [[East Tunnel]]',
      title: 'East Tunnel Gate',
      images: ['tube_gate.png'],
    },
    {
      id: 'area_layout_east_tunnel',
      description: 'Reveals ceilling access in the east tunnel.',
      images: ['tube_access.png'],
      title: 'East Tunnel',
    },
    {
      id: 'area_layout_ln_exit',
      description: 'Remove crumble blocks in [[Single Chamber]]',
      title: 'LN Crumbles',
      images: ['ln_gate.png'],
    },
    {
      id: 'area_layout_single_chamber',
      description: 'Makes the hidden LN entrance in [[Single Chamber]] more accessible. Also removes crumble blocks.',
      title: 'LN Access',
      images: ['ln_access.png', 'ln_gate.png'],
    },
    {
      id: 'east_ocean',
      description: 'Open door to [[Sponge Bath]] and add two platforms to [[East Ocean]] (access [[Forgoten Highway]] with only hi-jump boots)',
      images: ['sponge_bath_blue_door.gif', 'forgotten_all_the_way.png'],
      title: 'East Ocean',
    },
  ],
  variaTweaks: [
    {
      id:'bomb_torizo',
      description: "The status in [[Bomb Torizo Room]] is activated by picking up the item he's holding (normally activated when you have bombs)",
      title: 'Bomb Torizo',
    },
    {
      id: 'WS_Etank',
      description: 'Places the item in [[Wrecked Ship Energy Tank Room]] and colors upper door in [[Electric Death Room]] before the ship is activated.',
      title: 'WS Energy',
      images: ['ws_etank.png'],
    },
    {
      id: 'LN_Chozo',
      description: 'Activate the statue in the [[Acid Statue Room]] before space jump has been found and adds a platform for easy access.',
      title: 'Acid Statue',
      images: ['ln_chozo.png'],
    },
  ]
}


// I might eventually update this to work with super metroid icons
const applyMarkdown = (s) => s.replace(
  /\[\[([^\]]+)\]\]/g,
  (_, b) => `<a
    href="https://wiki.supermetroid.run/${b.replace(/ /g,'_')}"
    target="_blank"
  >${b}</a>`,
)

const startCase = (s) => s.replace(/_/g, ' ').replace(
    /\w\S*/g,
    (txt) => txt.charAt(0).toUpperCase() + txt.slice(1),
);

window.PATCHES_HELP = {}

Object.entries(window.PATCHES).forEach(
  ([patch_group, patches]) => {
    window.PATCHES_HELP[patch_group] = '<div class="patch-selector__cards">'
    patches.forEach(patch => {
      patch.patch_group = patch_group
      patch.images = patch.images || [patch.id+'.png']
      const images = patch.images.map(i => `<img src="/solver/static/images/help/${i}" />`).join('')
      window.PATCHES_HELP[patch_group] += `
<div class="patch-card -width-${patch.images.length}">
     <div class="patch-card__images">${images}</div>
     <div class="patch-card__content">
         <div class="patch-card__title">${patch.title}</div>
         <span>${applyMarkdown(patch.description)}</span>
     </div>
</div>
`
    })
  }
)
