
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import { useEffect, useState } from 'react'
import Router from 'next/router'

export default function EntryForm( {type}) {

    const [value, setValue] = useState()

    const handleSubmit = async (event) => {
        event.preventDefault()
        const base_url = 'http://127.0.0.1:5000/'
        const url = base_url + type.toLowerCase() + '?search=' + value
        console.log(url)
        await fetch(url)
        Router.reload(window.location.pathname)
    }

    return (
        <>
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>{type}</Form.Label>
                    <Form.Control type="string" onChange={(e) => setValue(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit" onClick={(e) => handleSubmit(e)}>
                    Submit
                </Button>
            </Form>
        </>
    )
}
