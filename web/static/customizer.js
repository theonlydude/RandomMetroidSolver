(() => {
  // js/helpers/hasFileReader.ts
  var hasFileReader = () => window.File && window.FileList && window.FileReader;
  var hasFileReader_default = hasFileReader;

  // js/helpers/settings.ts
  var SETTINGS;
  var DEFAULTS = {
    permalink: false
  };
  (() => {
    SETTINGS = Object.assign({}, DEFAULTS, window.VARIA_SETTINGS);
  })();
  var getSettings = () => SETTINGS;
  var settings_default = getSettings;

  // js/rom.ts
  var VALID_EXTENSIONS = ["sfc", "smc"];
  var VanillaROM = class {
    constructor() {
      if (!hasFileReader_default()) {
        alert("This website requires the HTML5 File API, please upgrade your browser to a newer version.");
        return;
      }
      const settings = settings_default();
      const selector = settings.permalink ? "vanillaUploadFile" : "uploadFile";
      this.el = document.getElementById(selector);
      const readFile = this.readFile.bind(this);
      this.el?.addEventListener("change", (evt) => {
        const file = evt.target.files?.[0];
        if (file) {
          readFile(file);
        }
      });
    }
    validateFileExtension(name) {
      const lastDot = name.lastIndexOf(".");
      const extension = name.substring(lastDot + 1).toLowerCase();
      if (VALID_EXTENSIONS.includes(extension)) {
        return true;
      }
      throw Error(`Unsupported file extension: ${extension}`);
    }
    readFile(file) {
      this.validateFileExtension(file.name);
      console.log("valid file extension");
    }
  };
  var rom_default = VanillaROM;

  // js/customizer.ts
  async function main() {
    new rom_default();
  }
  document.addEventListener("DOMContentLoaded", () => {
    main().catch((err) => {
      console.error(err);
    });
  });
})();
