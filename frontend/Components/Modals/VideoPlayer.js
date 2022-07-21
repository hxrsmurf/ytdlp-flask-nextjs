import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import { Dot, HandThumbsUp } from 'react-bootstrap-icons';

export default function VideoPlayer(props) {
    const title = props.data.title
    const video_url = props.data.cdn_video
    const channel_name = props.data.channel_name
    const like_count = props.data.like_count
    const upload_date = props.data.upload_date
    const view_count = props.data.view_count
    const description = props.data.description

    return (
        <Modal
            {...props}
            aria-labelledby="contained-modal-title-vcenter"
            fullscreen
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    {title}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h4>{channel_name}</h4>
                <Container>
                    <video
                        controls
                        preload='auto'
                        userActions='{"hotkeys": true}'
                        width='1024px'
                        height='640px'
                        >
                        <source src={video_url} type="video/mp4"/>
                    </video>
                </Container>
            </Modal.Body>
            <Modal.Footer>
                <HandThumbsUp/> {like_count}<Dot/>{view_count} views
                <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}