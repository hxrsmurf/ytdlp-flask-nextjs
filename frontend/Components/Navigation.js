import Navbar from 'react-bootstrap/Navbar'
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav'

export default function Navigation() {
    return (
        <>
            <Navbar bg="dark" variant="dark">
                <Container>
                    <Nav className="me-auto">
                        <Nav.Link href="/">Home</Nav.Link>
                        <Nav.Link href="/videos">Videos</Nav.Link>
                        <Nav.Link href="/channels">Channels</Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
        </>
    )
}