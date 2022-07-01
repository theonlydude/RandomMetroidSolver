import hasFileReader from './helpers/hasFileReader'

export default function handleROMSelect() {
  if (!hasFileReader()) {
    alert('This website requires the HTML5 File API, please upgrade your browser to a newer version.')
    return
  }

  console.log('handle selecting the ROM')
}
