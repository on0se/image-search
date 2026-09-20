import CloseButton from '../components/CloseButton'
import ExpandImageCard from '../components/ExpandImageCard'

export default function ImageModal({expandImage, nextScreen, setScreen}) {
  return (
    <div>
      <CloseButton targetScreen={nextScreen} setScreen={setScreen}/>
      <ExpandImageCard Image={expandImage}/>
    </div>
  )
}
