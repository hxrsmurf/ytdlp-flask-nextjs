import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { SessionProvider } from "next-auth/react"
import Sidebar from '../components/Sidebar'

export default function App({
  Component,
  pageProps: { session, ...pageProps },
}: AppProps) {
  return (
    <SessionProvider session={session}>
      <Sidebar/>
      <Component {...pageProps} />
    </SessionProvider>
  )
}