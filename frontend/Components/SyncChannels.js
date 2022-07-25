import Button from '@mui/material/Button';

export default function SyncChannels({ callback }) {

    // We have to do this because ytsearch yt-dlp is bad at finding channels by their ID.
    const handleSyncChannels = async (e) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/sync-channels')
        const request_channel_videos = await fetch(query_url)
        const result_missing_channels = await request_channel_videos.json()

        if (result_missing_channels.length > 0) {
            handleCallback(result_missing_channels)
        }
    }

    function handleCallback(data) {
        callback(data)
    }

    return (
        <>
            <Button
                variant='contained'
                color='info'
                onMouseDown={(e) => handleSyncChannels(e)}
            >
                Sync Channels
            </Button>
        </>
    )
}
