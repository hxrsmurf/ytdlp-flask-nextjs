import 'bootstrap/dist/css/bootstrap.min.css';
import 'video.js/dist/video-js.min.css'

import Container from '@mui/material/Container';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import NavigationMUI from '../Components/Navigation-mui';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <NavigationMUI />
      <Container style={{marginTop: '100px'}}>
        <Component {...pageProps} />
      </Container>
    </>
  )
}

export default MyApp
