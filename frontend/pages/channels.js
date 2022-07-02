import Container from 'react-bootstrap/Container'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import { useEffect, useState } from 'react'
import Router from 'next/router'

export default function channels({ results }) {

    const [channel, setChannel] = useState()

    const handleSubmit = async (event) => {
        event.preventDefault()
        const url = 'http://127.0.0.1:5000/channels?search=' + channel
        await fetch(url)
        Router.reload(window.location.pathname)
    }

    return (
        <>
            <Container className='mt-3'>
                <Form>
                    <Form.Group className="mb-3">
                        <Form.Label>Channel</Form.Label>
                        <Form.Control type="string" onChange={(e) => setChannel (e.target.value)}/>
                    </Form.Group>
                    <Button variant="primary" type="submit" onClick={(e) => handleSubmit(e)}>
                        Submit
                    </Button>
                </Form>
            </Container>

            <Container className='mt-5'>
                <ul>
                    {results.map((result,id) => (
                        <li key={id}>
                            <a href={result}>{result}</a>
                        </li>
                    ))}
                </ul>
            </Container>
        </>
    )
}

export async function getStaticProps() {
    const res = await fetch('http://127.0.0.1:5000/channels')
    const results = await res.json()
    return {
        props: {
            results
        }
    }
}