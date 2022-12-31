import { redis } from '../lib/database'
import LoginButton from '../login-button'

export default function Home({videos, channels}: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        <div>Hello World</div>
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