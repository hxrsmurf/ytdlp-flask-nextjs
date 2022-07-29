import Container from '@mui/material/Container';

import { AppBar, Dialog, IconButton, Toolbar, Typography } from '@mui/material';

import CloseIcon from '@mui/icons-material/Close';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';

export default function VideoPlayer(props) {
    const title = props.data.title
    const video_url = props.data.cdn_video
    const hls_url = props.data.cdn_video_hls
    const channel_name = props.data.channel_name
    const like_count = props.data.like_count
    const upload_date = props.data.upload_date
    const view_count = props.data.view_count
    const description = props.data.description

    return (
        <Dialog
            fullScreen
            open={props.show}
            onClose={props.onHide}
        >
            <AppBar style={{ backgroundColor: '#424242' }}>
                <Toolbar>
                    <IconButton onClick={props.onHide}>
                        <CloseIcon />
                    </IconButton>
                    <Typography sx={{ ml: 2, flex: 1 }}>{title}<span className="dot"></span>{channel_name}</Typography>
                    <Typography>
                        <ThumbUpIcon sx={{mr: 1, mb: .8}}/>{like_count}<span className="dot"></span>{view_count} views<span className="dot"></span>Uploaded {upload_date}
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container sx={{ mt: 10 }}>
                <video
                    controls
                    preload='auto'
                    userActions='{"hotkeys": true}'
                    width='1024px'
                    height='640px'
                >
                    <source src={video_url} type="video/mp4" />
                </video>
            </Container>
        </Dialog>
    );
}