import { useState } from 'react'

export default function AddChannel() {
  const [channel, setChannel]: any = useState()

  const handleInput = (e: any) => {
    setChannel(e.target.value)
  }

  const handleSubmit = async () => {
    if (channel) {
        await fetch('/api/addChannel?id=' + channel)
        setChannel('')
        console.log(channel)
    }
  }

  const handleClear = () => {
    setChannel('')
  }

  return (
    <div>
      <div className='grid grid-flow-col space-x-3'>
        <div>
          <input onChange={(e) => handleInput(e)} value={channel ? channel : ''} />
        </div>
        <div>
          <button onClick={() => handleSubmit()}>Submit</button>
        </div>
        <div>
          <button onClick={() => handleClear()}>Clear</button>
        </div>
      </div>
    </div>
  )
}