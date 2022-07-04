import vanillaRom from './rom'

async function main() {
  new vanillaRom()
}

document.addEventListener('DOMContentLoaded', () => {
  main()
    .catch((err) => {
      console.error(err)
    })
})
