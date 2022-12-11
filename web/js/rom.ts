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
    // TODO:  - if permalink
    //          - and valid contents
    //          - then show that ROM is stored
    //        - else
    //          - show correct upload button

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
    const isHeadered = fileSize === 3146240
    const isTooLarge = fileSize > 4*1024*1024
    if (isHeadered) {
      content = content.slice(512)
    } else if (isTooLarge) {
      throw Error(`Filesize is too big: ${content.size.toString()}`)
    }
    
    const crc32 = new Crc32()
    crc32.update(content)
    const checksum = crc32.digest()
    
    if (checksum !== VANILLA_CRC32) {
      console.error('Non-Vanilla ROM detected')
      return false
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
    const validated = this.validateChecksum(content)
    if (!validated) {
      return alert('The file you have provided is not a valid Vanilla ROM.')
    }
    // save with localForage
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
