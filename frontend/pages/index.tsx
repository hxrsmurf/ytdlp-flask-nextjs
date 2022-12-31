import AddChannel from '../components/forms/AddChannel'
import { redis } from '../lib/database'

export default function Home() {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        <div>
          <AddChannel />
        </div>
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const videos = await redis().get('videos')
  const channels = await redis().get('channels')

  return {
    props: {
      videos: videos,
      channels: channels,
    },
  }
}