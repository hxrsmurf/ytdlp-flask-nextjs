import LoadingButton from '@mui/lab/LoadingButton';
import LoopIcon from '@mui/icons-material/Loop';

export default function LoadingCircle({ text }) {
    return (
        <>
            <LoadingButton
                loading
                loadingPosition={text ? "start" : "center"}
                startIcon={<LoopIcon />}
                variant="contained"
            >
                {text ? text : <></>}
            </LoadingButton>
        </>
    )
}