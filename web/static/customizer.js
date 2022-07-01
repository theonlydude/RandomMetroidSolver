(() => {
  // js/helpers/hasFileReader.ts
  var hasFileReader = () => window.File && window.FileList && window.FileReader;
  var hasFileReader_default = hasFileReader;

  // js/rom.ts
  function handleROMSelect() {
    if (!hasFileReader_default()) {
      alert("This website requires the HTML5 File API, please upgrade your browser to a newer version.");
      return;
    }
    console.log("handle selecting the ROM");
  }

  // js/customizer.ts
  async function main() {
    console.log("sup its main");
    handleROMSelect();
  }
  main().catch((err) => {
    console.error(err);
  });
})();
