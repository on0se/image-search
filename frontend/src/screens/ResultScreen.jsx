import CloseButton from '../components/CloseButton'
import QueryImageCard from '../components/QueryImageCard'
import ImageGrid from '../components/ImageGrid'

export default function ResultScreen({handleModal, dbImages, searchResults, queryImage, setScreen}) {
  return (
    <div>
      <CloseButton targetScreen={"normal"} setScreen={setScreen}/>
      {/* Chakraのリセットで img が display:block になるため、text-align ではなく flex で中央に寄せる */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <h2>クエリ画像</h2>
        <QueryImageCard Image={queryImage} handleModal={handleModal}/>
      </div>
      <h2>検索結果（{searchResults.length}件）</h2>
      <ImageGrid searchResults={searchResults} handleModal={handleModal} dbImages={dbImages}/>
    </div>
  )
}
