import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

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
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    {title}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h4>{channel_name}</h4>
                <p>
                    {description}
                </p>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}