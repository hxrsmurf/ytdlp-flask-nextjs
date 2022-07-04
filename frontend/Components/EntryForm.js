
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import { useEffect, useState } from 'react'
import Router from 'next/router'

export default function EntryForm({ type }) {
    const base_api = process.env.NEXT_PUBLIC_BASE_API_URL

    const [value, setValue] = useState()
    const [loading, setLoading] = useState()

    const handleSubmit = async (event) => {
        event.preventDefault()
        setLoading(true)
        // If channel URL, then save to JSON file
        if (value.includes('/c/') || value.includes('/user/')){
            await fetch(base_api + 'channels?search=' + value)
        } else {
            await fetch(base_api + 'videos?add=' + value)
        }

        setLoading(false)
        Router.reload(window.location.pathname)
    }

    return (
        <>
            {loading ? <>
                <button className="btn btn-primary" type="button" disabled>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span className="sr-only">Downloading...</span>
                </button>
            </> :
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
