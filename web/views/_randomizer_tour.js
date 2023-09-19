window.PATCHES = {
  layoutPatches: [
    {
      id: 'door_indicators_plms',
      title: 'Flashing Doors',
      description: 'Show the color of a locked door from the other side.',
    },
    {
      id: 'dachora',
      title: 'Dachora',
      description: 'Disable respawning blocks in the [[Dachora Room]]',
    },
    {
      id: 'early_super_bridge',
      title: 'Early Supers',
      description: 'Add shot blocks to [[Early Supers Room] to escape without items.',
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
      description: 'Spore Spawn save station is always available',
    },
    {
      id: 'nova_boost_platform',
      title: 'Nova Boost',
      description: 'Get though [[Cathedral Entrance]] without Hi Jump',
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
    },
    {
      id: 'kraid_save',
      title: 'Kraid Save',
      description: '',
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
    },
    {
      id: 'area_layout_crab_hole',
      description: 'Rearrange blocks in [[Crab Hole]] for grav-less access',
      title: 'Crab Hole',
    },
    {
      id: 'area_rando_gate_greenhillzone',
      description: 'Remove blue gate in [[Green Hill Zone]] and make meme route wall jump easier',
      title: 'Green Hill Gate',
      images: ['area_rando_gate_greenhillzone.png', 'greenhill_walljump.png'],
    },
    {
      id: 'aqueduct_bomb_blocks',
      description: 'Replace [[Aqueduct]] power-bomb blocks with bomb blocks',
      title: 'Aqueduct Blocks',
    },
    {
      id: 'area_layout_caterpillar',
      description: 'Access maridia red fish entrance',
      images: ['fish_access_wall.png',],
      title: 'Red Tower',
    },
    {
      id: 'area_layout_east_tunnel',
      description: 'Reveals ceilling access in the east tunnel.',
      images: ['tube_access_ceiling.png'],
      title: 'East Tunnel',
    },
    {
      id: 'area_layout_single_chamber',
      description: 'Makes the hidden LN entrance more accessible',
      title: 'LN Access',
      images: ['ln_access_wall.png'],
    },
    {
      id: 'east_ocean',
      description: 'Open door to [[Sponge Bath]] and add two platforms to [[East Ocean]] (allows access only hi-jump boots)',
      images: ['east_ocean_door.png', 'east_ocean_island.png'],
      title: 'East Ocean',
    },
  ],
  variaTweaks: [
    {
      id:' bomb_torizo',
      description: "The statuse in [[Bomb Torizo Room]] is activated by picking up the item he's holding (normally activated if/when you have bombs)",
      title: 'Bomb Torizo',
    },
    {
      id: 'WS_Etank',
      description: 'Places the item in [[Wrecked Ship Energy Tank Room]] and turns the upper door in [[Electric Death Room]] red before the ship is activated.',
      title: 'WS Energy',
    },
    {
      id: 'LN_Chozo',
      description: 'Activate the statue in the [[Acid Statue Room]] before space jump has been found and adds a platform for easy access.',
      title: 'Acid Statue',
    },
  ]
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
