import 'bootstrap/dist/css/bootstrap.min.css';
import Navigation from "../Components/Navigation"
import 'video.js/dist/video-js.min.css'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Navigation/>
      <Component {...pageProps} />
    </>
  )
}

export default MyApp
