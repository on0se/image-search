export default function QueryImageCard({Image, handleModal}) {
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
  )
}
