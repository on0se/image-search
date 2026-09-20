import UserControlPanel from '../components/UserControlPanel'
import ImageGrid from '../components/ImageGrid'

export default function NormalScreen({topK, setTopK, handleFileUp, handleSearch, handleModal, dbImages}) {
  return (
    <div>
      <UserControlPanel topK={topK} setTopK={setTopK} handleFileUp={handleFileUp} handleSearch={handleSearch}/>
      <ImageGrid handleModal={handleModal} dbImages={dbImages}/>
    </div>
  )
}
