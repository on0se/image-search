import ImageCard from './ImageCard'

export default function ImageGrid({searchResults, handleModal, dbImages}) {
  /*
    画像を10列でグリッド表示するコンポーネント
    引数：画像の添え字リスト。渡されないなら全ての添え字が対象(通常画面)、渡されたらその添え字が対象(結果画面)。
  */
  // searchResultsが空の時は全ての添え字が対象
  let keys
  if (searchResults === undefined) keys = dbImages.map((_, i) => i)
  else keys = searchResults

  return (
    <div style={{
      display: "grid", 
      gridTemplateColumns: "repeat(10, 1fr)", // 10列を均等に分ける
      gap: 8
    }}>
      {keys.map(key => 
        <ImageCard key={key} Image={dbImages[key]} handleModal={handleModal}/>
      )}
    </div>
  )
}
