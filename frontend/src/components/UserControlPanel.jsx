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
  )
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
  )
}

export default function UserControlPanel({topK, setTopK, handleFileUp, handleSearch}) {
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
  )
}
