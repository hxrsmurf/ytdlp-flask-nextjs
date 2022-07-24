import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import { useState } from 'react'
import Router from 'next/router'
import LoadingCircle from './LoadingCircle'

export default function EntryForm({ type }) {
    const base_api = process.env.NEXT_PUBLIC_BASE_API_URL

    const [value, setValue] = useState()
    const [loading, setLoading] = useState()

    const handleSubmit = async (event) => {
        event.preventDefault()
        setLoading(true)

        if (value.includes('/c/') || value.includes('/user/') || value.includes('/channel/')) {
            await fetch(base_api + '/mongo/channels/add?url=' + value)
        } else if (value.includes('/playlist?')) {
            fetch(base_api + '/mongo/videos/add?url=' + value)
            setTimeout(() => setLoading(false), 1000)
        }
        else {
            await fetch(base_api + '/mongo/videos/add?url=' + value)
        }

        setLoading(false)
        Router.reload(window.location.pathname)
    }

    return (
        <>
            {loading ? <LoadingCircle text='Downloading...' /> :
                <Form>
                    <Form.Group className="mb-3">
                        <Form.Label>{type}</Form.Label>
                        <Form.Control type="string" onChange={(e) => setValue(e.target.value)} />
                    </Form.Group>
                    <Button variant="primary" type="submit" onClick={(e) => handleSubmit(e)}>
                        Submit
                    </Button>
                </Form>
            }
        </>
    )
}