export default function CloseButton({targetScreen, setScreen}) {
  return (
    <button 
      onClick={() => setScreen(targetScreen)}
      style={{
        position: "fixed",
        top: 10,
        right: 10,
      }}
    > X </button>
  )
}
