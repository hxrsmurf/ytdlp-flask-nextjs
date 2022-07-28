import Button from '@mui/material/Button'
import { useState } from 'react'

import EntryForm from '../Components/EntryForm'
import LoadingCircle from '../Components/LoadingCircle'
import VideoCardList from '../Components/VideoCardList'
import MissingChannels from '../Components/MissingChannels'
import SyncChannels from '../Components/SyncChannels'
import { Container, FormControl, Grid, InputLabel, Menu, MenuItem, Select } from '@mui/material'

export default function index({ results, result_all_channels }) {
    const [channel, setChannel] = useState()
    const [channelID, setChannelID] = useState()
    const [dropdownName, setDropdownName] = useState()
    const [newResults, setNewResults] = useState()
    const [loading, setLoading] = useState()
    const [missingChannels, setMissingChannels] = useState()
    const [showWatchedButton, setShowWatchedButton] = useState()

    const [anchorEl, setAnchorEl] = useState(null)
    const channelMenuOpen = Boolean(anchorEl)
    const [loadingChannelFilter, setLoadingChannelFilter] = useState()

    const base_api_url = process.env.NEXT_PUBLIC_BASE_API_URL

    const handleDropdownClick = async (event) => {
        setDropdownName(channel)
        console.log(channel)
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

    const handleChannelMenuClick = async (event) => {
        setAnchorEl(event.currentTarget)
    }

    const handleChannelClose = async (event) => {
        setAnchorEl(null)
    }

    const handleChannelNameClose = async (event) => {
        setAnchorEl(null)
        setDropdownName(event.channel_name)
        setChannelID(event.channel_id)

        console.log(event.channel_name)
        setLoadingChannelFilter(true)
        const request_channel_videos = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/search/' + channelID)
        const new_results = await request_channel_videos.json()
        setNewResults(new_results)
        setLoadingChannelFilter(false)
    }

    return (
        <>

            <Container sx={{marginTop: 5}}>
                <EntryForm type='Videos' />
            </Container>

            {missingChannels ?
                <>
                    <MissingChannels data={missingChannels} />
                </>
                :
                <></>
            }

            <Grid container spacing={2} sx={{marginTop: 5}} direction='row' justifyContent="center" alignItems="center">
                <Grid item  sx={{marginRight: 2}} width={200}>
                    <Button
                        variant='contained'
                        aria-controls={channelMenuOpen ? 'basic-menu' : undefined}
                        aria-haspopup='true'
                        aria-expanded={channelMenuOpen ? 'true' : undefined}
                        onClick={handleChannelMenuClick}
                    >
                    {dropdownName ? <>{loadingChannelFilter ? <LoadingCircle/>:  dropdownName}</> : 'Channels...'}
                    </Button>
                    <Menu
                        open={channelMenuOpen}
                        onClose={handleChannelClose}
                        anchorEl={anchorEl}
                    >
                        {result_all_channels.map((channel, id) => (
                                <div key={id}>
                                    <MenuItem key={id} onClick={() => handleChannelNameClose(channel)}>
                                        {channel.channel_name}
                                    </MenuItem>
                                </div>

                            ))}
                    </Menu>
                </Grid>

                <Grid item>
                    <Button
                        variant='contained'
                        color='secondary'
                        onMouseDown={(e) => handleResetFilter(e)}
                    >
                        Reset
                    </Button>
                </Grid>
                <Grid item>
                    <Button
                        variant='contained'
                        color='info'
                        onMouseDown={(e) => handleShowDownloadedVideos(e)}
                    >
                        Show Downloaded
                    </Button>
                </Grid>
                <Grid item>
                    {showWatchedButton ?
                        <>
                            <Button
                                variant='contained'
                                color='info'
                                onMouseDown={(e) => handleShowWatched(e)}
                            >
                                Show Watched
                            </Button>
                        </>
                        :
                        <>
                            <Button
                                variant='contained'
                                color='info'
                                onMouseDown={(e) => handleShowUnWatched(e)}
                            >
                                Show Unwatched
                            </Button>
                        </>
                    }
                </Grid>

                <Grid item>

                    {loading ? <LoadingCircle text='Downloading...' />
                        :
                        <>
                            {dropdownName ?
                                <>
                                    <Button
                                        variant='contained'
                                        color='warning'
                                        onMouseDown={(e) => handleDownloadLatestChannel(e)}
                                    >
                                        Download {dropdownName}</Button>
                                </>
                                :
                                <>
                                    <Button
                                        variant='contained'
                                        color='warning'
                                        onMouseDown={(e) => handleDownloadLatest(e)}
                                    >
                                        Download latest</Button>
                                </>
                            }
                        </>
                    }
                </Grid>

                <Grid item><SyncChannels callback={setMissingChannels} /></Grid>

            </Grid>

            <Container sx={{marginTop: 5}}>
                {loadingChannelFilter ?
                    <LoadingCircle/>
                :
                <>
                    {newResults ?
                        <>
                            <VideoCardList data={newResults} />
                        </>
                        :
                        <>
                            <VideoCardList data={results} />
                        </>
                    }
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