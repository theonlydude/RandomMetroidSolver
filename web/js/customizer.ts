import handleROM from './rom'

async function main() {
  console.log('sup its main')
  handleROM()
}

main()
  .catch((err) => {
    console.error(err)
  })
