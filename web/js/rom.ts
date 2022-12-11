import hasFileReader from './helpers/hasFileReader'
import Settings from './helpers/settings'
import Crc32 from './helpers/crc32'
import { VANILLA_CRC32 } from './constants'
import { get, set } from 'idb-keyval'

const VALID_EXTENSIONS = ['sfc', 'smc']
const VANILLA_ROM_KEY = 'vanillaROM'

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
    if (settings.permalink) {
      const hasROMLoaded = this.getROM().then((value) => {
        if (!value) {
          return false
        }
        const validated = this.validateChecksum(value)
        return validated
      })
    }

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

  getUnheaderedContent(content) {
    const fileSize = content.byteLength
    const isHeadered = fileSize === 3146240
    return isHeadered ? content.slice(512) : content
  }

  validateChecksum(content) {
    const fileSize = content.byteLength
    const isTooLarge = fileSize > 4*1024*1024
    if (isTooLarge) {
      console.warn(`Filesize is too big: ${content.size.toString()}`)
      return false
    }
    
    const crc32 = new Crc32()
    crc32.update(content)
    const checksum = crc32.digest()
    
    if (checksum === VANILLA_CRC32) {
      return true
    }

    console.warn('Non-Vanilla ROM detected')
    return false
  }

  validateFileExtension(name: string) {
    const lastDot = name.lastIndexOf('.')
    const extension = name.substring(lastDot + 1).toLowerCase()
    if (VALID_EXTENSIONS.includes(extension)) {
      return true
    }
    throw Error(`Unsupported file extension: ${extension}`)
  }

  async readFile(evt) {
    let content = this.getUnheaderedContent(evt.target.result)
    const validated = this.validateChecksum(content)
    if (!validated) {
      return alert('The file you have provided is not a valid Vanilla ROM.')
    }
    const data = new Uint8Array(content)
    await this.setROM(content)
  }

  useFile(file: File) {
    this.validateFileExtension(file.name)

    const reader = new FileReader()
    const onLoad = this.readFile.bind(this)
    reader.addEventListener('load', onLoad)
    reader.readAsArrayBuffer(file)
  }

  getROM() {
    return get(VANILLA_ROM_KEY)
  }

  setROM(content: Uint8Array) {
    try {
      const value = set(VANILLA_ROM_KEY, content)
      return value
    } catch (err) {
      console.error('Could not set Vanilla ROM', err)
    }
    
  }
}

export default VanillaROM
