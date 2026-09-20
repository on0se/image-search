import CloseButton from '../components/CloseButton'
import QueryImageCard from '../components/QueryImageCard'
import ImageGrid from '../components/ImageGrid'

export default function ResultScreen({handleModal, dbImages, searchResults, queryImage, setScreen}) {
  return (
    <div>
      <CloseButton targetScreen={"normal"} setScreen={setScreen}/>
      <QueryImageCard Image={queryImage} handleModal={handleModal}/>
      <ImageGrid searchResults={searchResults} handleModal={handleModal} dbImages={dbImages}/>
    </div>
  )
}
