import 'bootstrap/dist/css/bootstrap.min.css';
import Navigation from "../Components/Navigation"
import 'video.js/dist/video-js.min.css'

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Navigation/>
      <Component {...pageProps} />
    </>
  )
}

export default MyApp
