import hasFileReader from './helpers/hasFileReader'
import Settings from './helpers/settings'
import Crc32 from './helpers/crc32'
import { VANILLA_CRC32 } from './constants'

const VALID_EXTENSIONS = ['sfc', 'smc']

class VanillaROM {
  el: HTMLElement | null

  constructor() {
    if (!hasFileReader()) {
      alert('This website requires the HTML5 File API, please upgrade your browser to a newer version.')
      return
    }
    const settings = Settings()
    const selector = settings.permalink ? 'vanillaUploadFile' : 'uploadFile'
    this.el = document.getElementById(selector)
    const useFile = this.useFile.bind(this)
    this.el?.addEventListener('change', (evt: Event) => {
      const file = (<HTMLInputElement>evt.target).files?.[0]
      if (file) {
        useFile(file)
      }
    })
  }

  validateChecksum(content) {
    const fileSize = content.byteLength
    if (fileSize === 3146240) {
      console.log('potential headered ROM')
      content = content.slice(512)
    } else if (fileSize > 4*1024*1024) {
      throw Error(`Filesize is too big: ${content.size.toString()}`)
    } else {
      console.log('correct size')
    }
    
    const crc32 = new Crc32()
    crc32.update(content)
    const checksum = crc32.digest()
    
    if (checksum !== VANILLA_CRC32) {
      throw Error('Non-Vanilla ROM detected')
    }

    return true
  }

  validateFileExtension(name: string) {
    const lastDot = name.lastIndexOf('.')
    const extension = name.substring(lastDot + 1).toLowerCase()
    if (VALID_EXTENSIONS.includes(extension)) {
      return true
    }
    throw Error(`Unsupported file extension: ${extension}`)
  }

  readFile(evt) {
    const content = evt.target.result
    this.validateChecksum(content)
  }

  useFile(file: File) {
    this.validateFileExtension(file.name)

    const reader = new FileReader()
    const onLoad = this.readFile.bind(this)
    reader.addEventListener('load', onLoad)
    reader.readAsArrayBuffer(file)
  }
}

export default VanillaROM
