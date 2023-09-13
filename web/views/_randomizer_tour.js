const AREA_PATCHES = {
  crab_gate: {
    description: 'Remove green gate in [[Crab Tunnel]]',
  },
  greenhill_gate: {
    description: 'Remove blue gate in [[Green Hill Zone]]',
    title: 'Green Hill Gate',
  },
  greenhill_walljump: {
    description: 'Door access in [[Green Hill Zoone]]',
    title: 'Green Hill Ledge',
  },
  crab_hole: {
    description: 'Rearrange blocks in [[Crab Hole]] for grav-less access',
  },
  aqueduct_bomb_blocks: {
    description: 'Replace [[Aqueduct]] power-bomb blocks with bomb blocks',
    title: 'Aqueduct Blocks',
  },
  fish_access: {
    description: 'Remove green gate in [[Red Tower Elevator Room]] and makes the access point more visible.',
    images: ['fish_access_wall', 'fish_access_gate',],
  },
  tube_access: {
    description: 'Remove green gate in [[East Tunnel]] and unhides the ceilling access.',
    images: ['tube_access_ceiling', 'tube_access_gate'],
  },
  ln_access: {
    description: 'Remove crumble blocks in [[Single Chambler]] and makes the hidden LN entrance more visible',
    title: 'LN Access',
    images: ['ln_access_wall', 'ln_access_crumble'],
  },
  east_ocean: {
    description: 'Open door to [[Sponge Bath]] and add two platforms to [[East Ocean]] (allows access only hi-jump boots)',
    images: ['east_ocean_door', 'east_ocean_island'],
  },
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

let AREA_PATCH_CARDS = '<div class="patch-card__wrapper">'
Object.entries(AREA_PATCHES).forEach(([key, options]) => {
  options.images = options.images || [key]
  const images = options.images.map(i => `
<img src="/solver/static/images/help/${i}.png" class="patch-card__image -on" />
<img src="/solver/static/images/help/${i}__vanilla.png" class="patch-card__image -off" />
`).join('')
  const title = startCase(options.title || key)
  AREA_PATCH_CARDS += `
  <div class="patch-card -width-${options.images.length}">
    <div class="patch-card__images">
      ${images}
    </div>
    <div class="patch-card__content">
      <b>${title}</b>
      ${applyMarkdown(options.description)}
    </div>
  </div>`
})

AREA_PATCH_CARDS += '</div>'