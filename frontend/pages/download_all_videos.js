import Container from 'react-bootstrap/Container'
import Button from 'react-bootstrap/Button'
import { useState } from 'react'
import Router from 'next/router'

export default function download_all_videos() {

  const [loading, setLoading] = useState()

  const handleSubmit = async (event) => {
    event.preventDefault()
    const base_url = 'http://127.0.0.1:5000/download_all_videos'
    setLoading(true)
    await fetch(base_url)
    setLoading(false)
    Router.reload(window.location.pathname)
  }

  return (
    <>
      <Container className='mt-5'>
        {loading ?
        <button className="btn btn-primary" type="button" disabled>
          <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span class="sr-only">Downloading...</span>
        </button> :
          <Button variant="primary" type="submit" onClick={(e) => handleSubmit(e)}>
            Download All Videos!
          </Button>
        }
      </Container>
    </>
  )
}
