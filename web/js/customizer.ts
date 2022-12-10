import vanillaRom from './rom'

async function main() {
  new vanillaRom()
}

window.addEventListener('load', () => {
  main()
    .catch((err) => {
      console.error(err)
    })
})
