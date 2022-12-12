import hasFileReader from './helpers/hasFileReader'
import Settings from './helpers/settings'
import Crc32 from './helpers/crc32'
import { VANILLA_CRC32 } from './constants'
import { del, get, set } from 'idb-keyval'

const VALID_EXTENSIONS = ['sfc', 'smc']
const VANILLA_ROM_KEY = 'vanillaROM'

declare global {
  interface Window {
    // the /randomizer route uses the variable `vanillaROM`
    vanillaROM: Uint8Array | null
    // the /customizer route uses the variable `vanillaROMBytes`
    vanillaROMBytes: Uint8Array | null
  }
}

class VanillaROM {
  el: HTMLElement | null

  constructor() {
    if (!hasFileReader()) {
      alert('This website requires the HTML5 File API, please upgrade your browser to a newer version.')
      return
    }

    const checkForStoredFile = this.checkForStoredFile.bind(this)
    const bindEvents = this.bindEvents.bind(this)
    const broadcastROMStatus = this.broadcastROMStatus.bind(this)
    checkForStoredFile()
      .then((hasFile) => {
        if (hasFile) {
          console.log('Vanilla ROM loaded from storage')
        } else {
          broadcastROMStatus(null)
          bindEvents()
        }
      })
  }

  bindEvents() {
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

  checkForStoredFile(): Promise<boolean> {
    return new Promise((resolve, _reject) => {
      this.getROM()
        .then((value) => {
          if (!value) {
            resolve(false)
            return
          }
          const validated = this.validateChecksum(value)
          if (validated) {
            this.broadcastROMStatus(value)
            resolve(true)
            return
          }
          throw Error('Invalid Vanilla ROM value stored')
        })
        .catch((err) => {
          console.error(err)
          del(VANILLA_ROM_KEY)
          resolve(false)
        })
    })
  }

  displayStatus(hasROM = false) {
    const formEl = document.getElementById('vanillaROMVisibility')
    const okEl = document.getElementById('vanillaROMOKVisibility')
    if (!formEl || !okEl) {
      return
    }
    if (hasROM) {
      formEl.style.display = 'none'
      okEl.style.display = 'block'
    } else {
      formEl.style.display = 'block'
      okEl.style.display = 'none'
    }

  }

  getUnheaderedContent(content) {
    const fileSize = content.byteLength
    const isHeadered = fileSize === 3146240
    return isHeadered ? content.slice(512) : content
  }

  broadcastROMStatus(content: Uint8Array | null) {
    const hasROM = content !== null && content.byteLength > 0
    this.displayStatus(hasROM)
    this.setLegacyROMToBrowser(content)
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
    const saved = await this.setROM(data)
    if (saved) {
      this.broadcastROMStatus(data)
    }
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
      set(VANILLA_ROM_KEY, content)
      return true
    } catch (err) {
      console.error('Could not set Vanilla ROM', err)
      return false
    }
    
  }

  setLegacyROMToBrowser(content) {
    // Inline scripts on the page uses these variables depending on the route.
    // This method sets both values for both variables to work with the inline scripts.
    window.vanillaROMBytes = content
    window.vanillaROM = content
  }
}

export default VanillaROM
