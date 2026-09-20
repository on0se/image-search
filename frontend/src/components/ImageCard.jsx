import { useState } from 'react'
import { Skeleton } from '@chakra-ui/react'

export default function ImageCard({Image, handleModal}) {
  const [isLoaded, setIsLoaded] = useState(false) // 画像がロードされたか

  return (
    <Skeleton isLoaded={isLoaded} width="100%" height="100px">
      <img 
        src={Image}
        onLoad={() => setIsLoaded(true)}
        onClick={() => handleModal(Image)}
        style={{
          width: "100%",
          height: "100px",
          objectFit: "cover",
        }}
      />
    </Skeleton>
  )
}
