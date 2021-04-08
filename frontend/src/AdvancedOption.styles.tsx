import {makeStyles} from "@material-ui/core/styles";

export const useStyles = makeStyles((theme) => {
    return ({
        advancedOption: {
            position: 'relative',
            width: '75%',
            maxWidth: '600px',
            marginLeft: "auto",
            marginRight: "auto",
            marginBottom: "30px",
            borderRadius: 4,
            paddingLeft: theme.spacing(1),
            paddingRight: theme.spacing(1),
        },
        advancedOptionTitle: {
            display:'block',
            position: 'relative',
            paddingLeft: '4px',
            width: '100%',
            height: '50px'
        },
        optionPhrase: {
            position: 'absolute',
            top: 12,
            left: 40
        },
        expand: {
            position: 'absolute',
            right: 0,
            top: 10
        },
        mapDisplay:{
            width: "100%",
            height: "400px",
            borderRadius: 8
        },
        layout: {
            position: 'relative',
            width: '75%',
            maxWidth: '600px',
            marginLeft: "auto",
            marginRight: "auto",
        },
        optionGuide: {
            fontStyle: "italic",
            marginBottom: 10
        }
    })
}, {index: 1});
