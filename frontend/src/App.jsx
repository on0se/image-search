import { useState, useRef } from 'react'

import { uploadImages, searchImage } from './api'
import NormalScreen from './screens/NormalScreen'
import ResultScreen from './screens/ResultScreen'
import LoadingScreen from './screens/LoadingScreen'
import ImageModal from './screens/ImageModal'

export default function App() {
  const [dbImages, setDbImages] = useState([]) // uploadした写真
  const [queryImage, setQueryImage] = useState(null) // クエリ画像
  const [screen, setScreen] = useState("normal") // 表示する画面(通常、結果、ロード、拡大写真)
  const [searchResults, setSearchResults] = useState([]) // 検索結果
  const [nextScreen, setNextScreen] = useState(null) // ロード画面の次、バツボタンの次の画面の情報
  const [topK, setTopK] = useState(10) // 検索で表示する画像数
  const [expandImage, setExpandImage] = useState(null) // 拡大している写真
  const dbImageNames = useRef(new Set()) // uploadした写真の名前

  // UploadButtonイベント
  async function handleFileUp(e) {
    // 写真のアップロード
    const files = Array.from(e.target.files)
    const newFiles = files.filter(file => !dbImageNames.current.has(file.name)) // 新しい写真のみ追加
    if (newFiles.length === 0) return
    const newUrls = newFiles.map(file => URL.createObjectURL(file))

    // ロード画面へ遷移
    setScreen("loading")

    // 画像データベース、画像ベクトルリスト、faissインデックス、名前setの更新
    await uploadImages(newFiles)
    setDbImages(prev => [...prev, ...newUrls])
    newFiles.forEach(file => dbImageNames.current.add(file.name))


    // 通常画面へ遷移
    setScreen("normal")
  }

  // SearchButtonイベント
  async function handleSearch(e) {
    // クエリ写真のアップロード
    const file = e.target.files[0]
    const newUrl = URL.createObjectURL(file)

    // ロード画面へ遷移
    setScreen("loading")

    // クエリ画像の更新、検索、検索結果の更新
    const response = await searchImage(file, topK)
    const data = await response.json()
    setQueryImage(newUrl)
    setSearchResults(data.results)

    // 結果画面へ遷移
    setScreen("results")
  }

  // 画像拡大イベント
  function handleModal(Image) {
    setNextScreen(screen)
    setExpandImage(Image)
    setScreen("modal")
  }

  let content
  if (screen == "normal") {
    content = <NormalScreen topK={topK} setTopK={setTopK} handleFileUp={handleFileUp} handleSearch={handleSearch} handleModal={handleModal} dbImages={dbImages}/>
  }
  else if (screen == "results") {
    content = <ResultScreen searchResults={searchResults} handleModal={handleModal} dbImages={dbImages} queryImage={queryImage} setScreen={setScreen}/>
  }
  else if (screen == "loading") {
    content = <LoadingScreen />
  }
  else {
    content = <ImageModal expandImage={expandImage} nextScreen={nextScreen} setScreen={setScreen}/>
  }

  return (
    <div>
      {content}
    </div>
  )
}
