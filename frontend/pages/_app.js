import 'bootstrap/dist/css/bootstrap.min.css';
import Navigation from "../Components/Navigation"

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Navigation/>
      <Component {...pageProps} />
    </>
  )
}

export default MyApp
