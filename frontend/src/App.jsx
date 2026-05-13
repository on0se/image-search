import { useState } from 'react';

function NormalScreen({topK, setTopK, handleFileUp, handleSearch, handleModal, dbImages}) {
  return (
    <div>
      <UserControlPanel topK={topK} setTopK={setTopK} handleFileUp={handleFileUp} handleSearch={handleSearch}/>
      <ImageGrid handleModal={handleModal} dbImages={dbImages}/>
    </div>
  );
}

function ResultScreen({handleModal, dbImages, searchResults, queryImage, setScreen}) {
  return (
    <div>
      <CloseButton targetScreen={"normal"} setScreen={setScreen}/>
      <QueryImageCard Image={queryImage} handleModal={handleModal}/>
      <ImageGrid searchResults={searchResults} handleModal={handleModal} dbImages={dbImages}/>
    </div>
  );
}

function LoadingScreen() {
  return (
    <div>
      <h1>現在ロード中です</h1>
    </div>
  );
}

function ImageModal({expandImage, nextScreen, setScreen}) {
  // Modalでは画像をクリックしても拡大しない(ループしてしまう)ため、何もしない関数を渡す
  return (
    <div>
      <CloseButton targetScreen={nextScreen} setScreen={setScreen}/>
      <ExpandImageCard Image={expandImage}/>
    </div>
  );
}

function UserControlPanel({topK, setTopK, handleFileUp, handleSearch}) {
  return (
    <div style={{ 
      display:"flex",
      alignItems: "center",
      gap: 16,
      justifyContent: "center"
    }}>
      <UploadButton handleFileUp={handleFileUp} />
      <TopKSlider topK={topK} setTopK={setTopK} />
      <SearchButton handleSearch={handleSearch}/>
    </div>
  );
}

function ImageGrid({searchResults, handleModal, dbImages}) {
  /*
    画像を10列でグリッド表示するコンポーネント
    引数：画像の添え字リスト。渡されないなら全ての添え字が対象(通常画面)、渡されたらその添え字が対象(結果画面)。
  */
  // データベースがないときに検索をしても全て表示になる、その対策はあとでしろ。データベースにないなら検索できないとかね
  // searchResultsが空の時は全ての添え字が対象
  let keys;
  if (searchResults === undefined) keys = dbImages.map((_, i) => i);
  else keys = searchResults;

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
  );
}

function CloseButton({targetScreen, setScreen}) {
  return (
    <button 
      onClick={() => setScreen(targetScreen)}
      style={{
        position: "fixed",
        top: 10,
        right: 10,
      }}
    > X </button>
  );
}

function UploadButton({handleFileUp}) {
  return (
    <label style={{
      padding: "8px 16px",
      backgroundColor: "#4a90e2",
      color: "white",
      borderRadius: "8px",
      cursor: "pointer",
    }}>
      写真をアップロード
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleFileUp}
        style={{ display: "none" }}
      />
    </label>
  )

}

function SearchButton({handleSearch}) {
  return (
    <label style={{
      padding: "8px 16px",
      backgroundColor: "#4a90e2",
      color: "white",
      borderRadius: "8px",
      cursor: "pointer",
    }}>
      検索写真をアップロード
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleSearch}
        style={{ display: "none" }}
      />
    </label>
  );
}

function TopKSlider({topK, setTopK}) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <span>{topK}</span>
      <input
        type="range"
        min={1}
        max={20}
        value={topK}
        onChange={e => setTopK(e.target.value)}
      />
    </div>
  );
}

function ImageCard({Image, handleModal}) {
  return (
    <img 
      src={Image}
      onClick={() => handleModal(Image)}
      style={{
        width: "100%",
        height: "100px",
        objectFit: "cover",
      }}
    />
  );
}

function ExpandImageCard({Image}) {
  return (
    <img 
      src={Image}
      style={{
        width: "50vw",
        height: "50vw",
        objectFit: "contain",
      }}
    />
  );
}

function QueryImageCard({Image, handleModal}) {
  return (
    <img 
      src={Image}
      onClick={() => handleModal(Image)}
      style={{
        width: "100px",
        height: "100px",
        objectFit: "cover",
      }}
    />
  );
}

export default function App() {
  const [dbImages, setDbImages] = useState([]); // uploadした写真
  const [queryImage, setQueryImage] = useState(null); // クエリ画像
  const [screen, setScreen] = useState("normal"); // 表示する画面(通常、結果、ロード、拡大写真)
  const [searchResults, setSearchResults] = useState([]) // 検索結果
  const [nextScreen, setNextScreen] = useState(null); // ロード画面の次、バツボタンの次の画面の情報
  const [topK, setTopK] = useState(10); // 検索で表示する画像数
  const [expandImage, setExpandImage] = useState(null); // 拡大している写真

  // UploadButtonイベント
  async function handleFileUp(e) {
    // 写真のアップロード
    const files = Array.from(e.target.files)
    const newUrls = files.map(file => URL.createObjectURL(file));

    // ロード画面へ遷移
    setScreen("loading");

    // 画像データベース、画像ベクトルリスト、faissインデックスの更新
    const formData = new FormData();
    files.forEach(file => formData.append("files", file));
    await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData
    })
    setDbImages(prev => [...prev, ...newUrls]);

    // 通常画面へ遷移
    setScreen("normal");
  }

  // SearchButtonイベント
  async function handleSearch(e) {
    // クエリ写真のアップロード
    const file = e.target.files[0];
    const newUrl = URL.createObjectURL(file);

    // ロード画面へ遷移
    setScreen("loading");

    // クエリ画像の更新、検索、検索結果の更新
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("http://localhost:8000/search", {
      method: "POST",
      body: formData
    })
    const data = await response.json()
    setQueryImage(newUrl);
    setSearchResults(data.results)

    // 結果画面へ遷移
    setScreen("results");
  }

  // 画像拡大イベント
  function handleModal(Image) {
    setNextScreen(screen);
    setExpandImage(Image);
    setScreen("modal");
  }

  let content;
  if (screen == "normal") {
    content = <NormalScreen topK={topK} setTopK={setTopK} handleFileUp={handleFileUp} handleSearch={handleSearch} handleModal={handleModal} dbImages={dbImages}/>;
  }
  else if (screen == "results") {
    content = <ResultScreen searchResults={searchResults} handleModal={handleModal} dbImages={dbImages} queryImage={queryImage} setScreen={setScreen}/>;
  }
  else if (screen == "loading") {
    content = <LoadingScreen />;
  }
  else {
    content = <ImageModal expandImage={expandImage} nextScreen={nextScreen} setScreen={setScreen}/>;
  }

  return (
    <div>
      {content}
    </div>
  )
}