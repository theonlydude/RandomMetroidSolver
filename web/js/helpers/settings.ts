let SETTINGS

declare global {
  interface Window {
    VARIA_SETTINGS: VariaSettings
  }
}

export type VariaSettings = {
  permalink?: boolean
}

const DEFAULTS: VariaSettings = {
  permalink: false
};

(() => {
  SETTINGS = Object.assign({}, DEFAULTS, window.VARIA_SETTINGS)
})()

const getSettings = () => SETTINGS

export default getSettings
