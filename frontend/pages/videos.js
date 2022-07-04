import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'
import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import { Youtube, Download } from 'react-bootstrap-icons'
import Dropdown from 'react-bootstrap/Dropdown'
import { useState } from 'react'

export default function videos({ results, result_all_channels }) {
    const [channel, setChannel] = useState()
    const [dropdownName, setDropdownName] = useState()
    const [newResults, setNewResults] = useState()

    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    const handleDropdownClick = async (event) => {
        setDropdownName(channel)
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/videos?search=' + channel)
        const new_results = await request_channel_videos.json()
        setNewResults(new_results)
    }

    const handleResetFilter = async (event) => {
        setDropdownName()
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/videos')
        const new_results = await request_channel_videos.json()
        setNewResults(new_results)
    }

    return (
        <>
            <Container className='mt-5'>
                <EntryForm type='Videos' />
            </Container>

            <Container className='mt-5'>
                <Row>
                    <Col md='auto'>
                        <Dropdown variant="success">
                            <Dropdown.Toggle>
                                {dropdownName ? channel : 'Channels...'}
                            </Dropdown.Toggle>
                            <Dropdown.Menu>
                                {result_all_channels.map((channel, id) => (
                                    <>
                                        <Dropdown.Item
                                            key={id}
                                            onMouseOver={(e) => setChannel(e.target.text)}

                                            onMouseDown={(e) => handleDropdownClick(e)}
                                        >
                                            {channel}
                                        </Dropdown.Item>
                                    </>

                                ))}
                            </Dropdown.Menu>
                        </Dropdown>
                    </Col>
                    <Col>
                        <Button
                            onMouseDown={(e) => handleResetFilter(e)}
                        >
                            Reset</Button>
                    </Col>
                </Row>
            </Container>

            <Container className='mt-5'>
                {newResults ?

                    <>
                        {newResults.map((result, id) => (
                            <Card key={id} className='mt-5'>
                                <Card.Img
                                    variant="top" src={result.thumbnail}
                                    onClick={(e) => handleClick(result.original_url)}
                                    style={{ cursor: "pointer" }}
                                />
                                <Card.Header>
                                    <Row>
                                        <Col lg>{result.channel} - {result.title}</Col>
                                        <Col md='auto'>
                                            <Button
                                                href={result.original_url}
                                                target="_blank"
                                                variant='outline-danger'>
                                                <Youtube size={20} />
                                            </Button>
                                        </Col>
                                        <Col md='auto'>
                                            <Button
                                                variant='secondary'>
                                                <Download size={20} />
                                            </Button>
                                        </Col>
                                    </Row>
                                </Card.Header>
                            </Card>
                        ))}
                    </>
                    :
                    <>
                        {results.map((result, id) => (
                            <Card key={id} className='mt-5'>
                                <Card.Img
                                    variant="top" src={result.thumbnail}
                                    onClick={(e) => handleClick(result.original_url)}
                                    style={{ cursor: "pointer" }}
                                />
                                <Card.Header>
                                    <Row>
                                        <Col lg>{result.channel} - {result.title}</Col>
                                        <Col md='auto'>
                                            <Button
                                                href={result.original_url}
                                                target="_blank"
                                                variant='outline-danger'>
                                                <Youtube size={20} />
                                            </Button>
                                        </Col>
                                        <Col md='auto'>
                                            <Button
                                                variant='secondary'>
                                                <Download size={20} />
                                            </Button>
                                        </Col>
                                    </Row>
                                </Card.Header>
                            </Card>
                        ))}
                    </>
                }
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch('http://127.0.0.1:5000/videos')
    const results = await res.json()

    const request_all_channels = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/videos?channels')
    const result_all_channels = await request_all_channels.json()

    return {
        props: {
            results,
            result_all_channels
        }
    }
}