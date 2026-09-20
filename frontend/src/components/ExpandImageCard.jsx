export default function ExpandImageCard({Image}) {
  return (
    <img 
      src={Image}
      style={{
        width: "50vw",
        height: "50vw",
        objectFit: "contain",
      }}
    />
  )
}
