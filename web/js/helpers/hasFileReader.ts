const hasFileReader = () => (
  window.File && window.FileList && window.FileReader
)

export default hasFileReader
