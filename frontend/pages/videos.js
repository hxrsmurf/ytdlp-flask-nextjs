import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'
import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import { Youtube, Download } from 'react-bootstrap-icons'
import Dropdown from 'react-bootstrap/Dropdown'
import { useState } from 'react'
import LoadingCircle from '../Components/LoadingCircle'
import { HandThumbsUp } from 'react-bootstrap-icons'

export default function videos({ results, result_all_channels }) {
    const [channel, setChannel] = useState()
    const [channelID, setChannelID] = useState()
    const [dropdownName, setDropdownName] = useState()
    const [newResults, setNewResults] = useState()
    const [loading, setLoading] = useState()

    const base_api_url = process.env.NEXT_PUBLIC_BASE_API_URL

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
        setChannel()
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/videos')
        const new_results = await request_channel_videos.json()
        setNewResults(new_results)
    }

    const handleDownloadLatest = async (event) => {
        setLoading(true)
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/videos?latest')
        handleDropdownClick()
        setLoading(false)
    }

    const handleDownloadLatestChannel = async (event) => {
        const query_url = (base_api_url + 'videos?latest=5&id=' + channelID)
        setLoading(true)
        const request_channel_videos = await fetch(query_url)
        handleDropdownClick()
        setLoading(false)
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
                                        >
                                            <Row
                                                onMouseDown={(e) => handleDropdownClick(e)}
                                                onMouseOver={(e) => {
                                                    setChannel(e.target.textContent)
                                                    setChannelID(e.target.nextSibling.textContent)
                                                }
                                                }
                                            >
                                                <Col>{channel.channel}</Col>
                                                <Col hidden>{channel.channel_id}</Col>
                                            </Row>
                                        </Dropdown.Item>
                                    </>

                                ))}
                            </Dropdown.Menu>
                        </Dropdown>
                    </Col>
                    <Col>
                        <Button
                            variant='secondary'
                            onMouseDown={(e) => handleResetFilter(e)}
                        >
                            Reset</Button>
                    </Col>
                    <Col md='auto'>
                        {loading ? <LoadingCircle text='Downloading...' />
                            :
                            <>
                                {channel ?
                                    <>
                                        <Button
                                            variant='info'
                                            onMouseDown={(e) => handleDownloadLatestChannel(e)}
                                        >
                                            Download {channel}</Button>
                                    </>
                                    :
                                    <>
                                        <Button
                                            variant='info'
                                            onMouseDown={(e) => handleDownloadLatest(e)}
                                        >
                                            Download latest</Button>
                                    </>
                                }
                            </>
                        }
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
                                        <Col lg>
                                            <Row><div className='fw-bold'>{result.channel}</div></Row>
                                            <Row><div>{result.title}</div></Row>
                                            <Row>
                                                <Col md='auto'>
                                                    {result.duration_string} minutes | {result.view_count} views | {result.upload_date} | {result.like_count}
                                                </Col>
                                            </Row>
                                        </Col>
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
                                        <Col lg>
                                            <Row><div className='fw-bold'>{result.channel}</div></Row>
                                            <Row><div>{result.title}</div></Row>
                                            <Row>
                                                <Col md='auto'>
                                                    {result.duration_string} minutes | {result.view_count} views | {result.upload_date} | {result.like_count}
                                                </Col>
                                            </Row>
                                        </Col>
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