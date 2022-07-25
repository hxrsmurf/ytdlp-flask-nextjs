import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import Dropdown from 'react-bootstrap/Dropdown'
import { useState } from 'react'

import EntryForm from '../Components/EntryForm'
import LoadingCircle from '../Components/LoadingCircle'
import VideoCardList from '../Components/VideoCardList'
import MissingChannels from '../Components/MissingChannels'
import SyncChannels from '../Components/SyncChannels'

export default function index({ results, result_all_channels }) {
    const [channel, setChannel] = useState()
    const [channelID, setChannelID] = useState()
    const [dropdownName, setDropdownName] = useState()
    const [newResults, setNewResults] = useState()
    const [loading, setLoading] = useState()
    const [missingChannels, setMissingChannels] = useState()
    const [showWatchedButton, setShowWatchedButton] = useState()

    const base_api_url = process.env.NEXT_PUBLIC_BASE_API_URL

    const handleDropdownClick = async (event) => {
        setDropdownName(channel)
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/search/' + channelID)
        const new_results = await request_channel_videos.json()
        setNewResults(new_results)
    }

    const handleResetFilter = async (event) => {
        setDropdownName()
        setChannel()
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos')
        const new_results = await request_channel_videos.json()
        setNewResults(new_results)
    }

    const handleDownloadLatest = async (event) => {
        const latest_range = 1
        const query_url = (base_api_url + '/mongo/download/latest?range=' + latest_range + '&id=' + 'all')
        setLoading(true)
        fetch(query_url)
        setTimeout(() => setLoading(false), 1000);
    }

    const handleDownloadLatestChannel = async (event) => {
        const latest_range = 7
        const query_url = (base_api_url + '/mongo/download/latest?range=' + latest_range + '&id=' + channelID)
        setLoading(true)
        fetch(query_url)
        setTimeout(() => setLoading(false), 1000);
    }

    const handleShowDownloadedVideos = async (event) => {
        const request = await fetch(base_api_url + '/mongo/videos/downloaded')
        const results = await request.json()
        setNewResults(results)
    }

    const handleShowWatched = async (event) => {
        const request = await fetch(base_api_url + '/mongo/videos/watched')
        const results = await request.json()
        setShowWatchedButton(false)
        setNewResults(results)
    }

    const handleShowUnWatched = async (event) => {
        const request = await fetch(base_api_url + '/mongo/videos/unwatched')
        const results = await request.json()
        setShowWatchedButton(true)
        setNewResults(results)
    }

    return (
        <>
            <Container className='mt-5'>
                <EntryForm type='Videos' />
            </Container>

            {missingChannels ?
                <>
                    <MissingChannels data={missingChannels} />
                </>
                :
                <></>
            }

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
                                        >
                                            <Row
                                                onMouseDown={(e) => handleDropdownClick(e)}
                                                onMouseOver={(e) => {
                                                    setChannel(e.target.textContent)
                                                    setChannelID(e.target.nextSibling.textContent)
                                                }
                                                }
                                            >
                                                <Col>{channel.channel_name}</Col>
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
                        <Button
                            variant='info'
                            onMouseDown={(e) => handleShowDownloadedVideos(e)}
                        >
                            Show Downloaded</Button>
                    </Col>
                    <Col md='auto'>
                        {showWatchedButton ?
                        <>
                            <Button
                                variant='secondary'
                                onMouseDown={(e) => handleShowWatched(e)}
                            >
                                Show Watched
                            </Button>
                        </>
                        :
                        <>
                            <Button
                                variant='secondary'
                                onMouseDown={(e) => handleShowUnWatched(e)}
                            >
                                Show Unwatched
                            </Button>
                        </>
                        }

                    </Col>
                    <Col md='auto'>
                        {loading ? <LoadingCircle text='Downloading...' />
                            :
                            <>
                                {dropdownName ?
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
                                            variant='warning'
                                            onMouseDown={(e) => handleDownloadLatest(e)}
                                        >
                                            Download latest</Button>
                                    </>
                                }
                            </>
                        }
                    </Col>

                    <Col md='auto'>
                        <SyncChannels callback={setMissingChannels}/>
                    </Col>

                </Row>
            </Container>

            <Container className='mt-5'>
                {newResults ?
                    <>
                        <VideoCardList data={newResults} />
                    </>
                    :
                    <>
                        <VideoCardList data={results} />
                    </>
                }
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos')
    const results = await res.json()

    const request_all_channels = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/unique/channel')
    const result_all_channels = await request_all_channels.json()

    return {
        props: {
            results,
            result_all_channels
        }
    }
}