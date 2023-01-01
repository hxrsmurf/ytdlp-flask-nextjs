import {
  ArrowPathRoundedSquareIcon,
  Bars3Icon,
  BuildingLibraryIcon,
  ClockIcon,
  FolderOpenIcon,
  HandThumbUpIcon,
  HomeIcon,
  VideoCameraIcon,
} from '@heroicons/react/20/solid'
import Link from 'next/link'

export default function Sidebar() {
  return (
    <div className='fixed ml-10 mt-4'>
      <div className='min-w-[200px]'>
        {menu_items.map((item, id) => (
          <div key={id}>
            <div className='grid grid-flow-col space-x-4 mb-4'>
              {item.name == 'Break' ? (
                <>
                  <div className='min-h-[2px] bg-white m-4'></div>
                </>
              ) : (
                <>
                  <Link href={String(item.link)} className='grid grid-flow-col hover:bg-gray-500'>
                    <div>{item.icon}</div>
                    <div>{item.name}</div>
                  </Link>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const menu_items = [
  {
    name: 'Home',
    icon: <HomeIcon className='h-6 w-6' />,
    link: '/',
  },
  {
    name: 'Subscriptions',
    icon: <FolderOpenIcon className='h-6 w-6' />,
    link: '/subscriptions',
  },
  {
    name: 'Break',
  },
  {
    name: 'Library',
    icon: <BuildingLibraryIcon className='h-6 w-6' />,
    link: '/',
  },
  {
    name: 'History',
    icon: <ArrowPathRoundedSquareIcon className='h-6 w-6' />,
    link: '/',
  },
  {
    name: 'Your Videos',
    icon: <VideoCameraIcon className='h-6 w-6' />,
    link: '/',
  },
  {
    name: 'Watch Later',
    icon: <ClockIcon className='h-6 w-6' />,
    link: '/',
  },
  {
    name: 'Liked Videos',
    icon: <HandThumbUpIcon className='h-6 w-6' />,
    link: '/',
  },
]
