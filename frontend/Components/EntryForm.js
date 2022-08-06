import { useState } from 'react'
import Router from 'next/router'
import LoadingCircle from './LoadingCircle'
import { Button, FormControl, FormGroup, Input, InputLabel } from '@mui/material';

export default function EntryForm() {
    const base_api = process.env.NEXT_PUBLIC_BASE_API_URL

    const [value, setValue] = useState()
    const [loading, setLoading] = useState()

    const handleSubmit = async (event) => {
        event.preventDefault()
        setLoading(true)

        if (value.includes('/c/') || value.includes('/user/') || value.includes('/channel/')) {
            await fetch(base_api + '/mongo/channels/add?url=' + value)
        } else if (value.includes('/playlist?') || value.includes('/watch?v=') || value.includes('youtu.be') || value.includes('/shorts/')){
            fetch(base_api + '/mongo/videos/add?url=' + value)
            setTimeout(() => setLoading(false), 1000)
        }
        else {
            await fetch(base_api + '/mongo/channels/add?url=' + value)
        }

        setLoading(false)
        Router.reload(window.location.pathname)
    }

    return (
        <>
            {loading ? <LoadingCircle text='Downloading...' /> :
                <FormControl sx={{ width: '63ch'}}>
                    <FormGroup  sx={{marginBottom: 3}}>
                        <InputLabel>URL</InputLabel>
                        <Input type="string" onChange={(e) => setValue(e.target.value)} />
                    </FormGroup>
                    <Button variant="contained" type="submit" color="success" onClick={(e) => handleSubmit(e)}>
                        Submit
                    </Button>
                </FormControl>
            }
        </>
    )
}