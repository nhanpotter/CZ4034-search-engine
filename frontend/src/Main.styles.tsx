import {makeStyles} from "@material-ui/core/styles";

export const useStyles = makeStyles((theme) => {
    return ({
        root: {
            width: '80%',
            maxWidth: '600px',
            marginLeft: 'auto',
            marginRight: 'auto',
            minHeight: "100px"
        },
        paper: {
            width: '100%',
            backgroundColor: 'transparent',
            borderRadius: 0,
            paddingLeft: theme.spacing(3),
            paddingRight: theme.spacing(3),
            paddingTop: theme.spacing(1),
            paddingBottom: theme.spacing(3),
            display: 'block',
            position: 'relative',
            boxSizing: 'border-box'
        },
        wrapNavBtn: {
            display: 'inline-block',
            marginRight: theme.spacing(2)
        },
        navBtn: {
            color: "white",
            fontSize: '12px',
            padding: theme.spacing(1.2),
            borderRadius: theme.shape.borderRadius,
            fontWeight: "bold",
            textTransform: 'uppercase',
            fontFamily: 'Helvetica',
            letterSpacing: '2px',
            '&:hover': {
                backgroundColor: 'rgba(0,0,0,0.1)',
            },
            zIndex: 20,
        },
        navBar: {
            marginBottom: '20px',
            marginTop: '10px',
            paddingLeft: '20px',
        }
    })
}, {index: 1});
