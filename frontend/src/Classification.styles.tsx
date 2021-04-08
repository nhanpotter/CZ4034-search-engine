import {makeStyles} from "@material-ui/core/styles";

export const useStyles = makeStyles((theme) => {
    return ({
        search: {
            position: 'relative',
            borderRadius: theme.spacing(1),
            width: '80%',
            maxWidth: '700px',
            marginLeft: "auto",
            marginRight: "auto",
            height: "fit-content",
            marginBottom: "30px",
            padding: theme.spacing(2)
        },
        searchTitle: {
            color: 'white',
            textAlign: 'center',
            paddingBottom: theme.spacing(2),
            fontFamily: 'Helvetica Neue,Helvetica,Arial,sans-serif;',
            letterSpacing: '1px',
            fontWeight: 200
        },
        inputInput: {
            width: '100%',
            display: 'block',
            height: "auto"
        },
        searchBtn: {
            zIndex: 10,
            marginLeft: 'auto',
            marginRight: 'auto',
            display: 'block',
            borderRadius: theme.shape.borderRadius,
            backgroundColor: theme.palette.primary.dark,
            color: "white",
            '&:hover': {
                backgroundColor: "#1460aa"
            }
        },
        mainIcon: {
            fontSize: 120,
            display: 'block',
            marginLeft: 'auto',
            marginRight: 'auto',
            color: "white",
            marginTop: theme.spacing(3),
            marginBottom: theme.spacing(3),
            fontWeight: 400
        },
        guide: {
            width: '70%',
            maxWidth: '660px',
            marginLeft: "auto",
            marginRight: "auto",
            padding: 0,
            borderRadius: theme.shape.borderRadius,
            marginTop: theme.spacing(3),
        },
        guideInfo: {
            textAlign: 'justify',
            margin: theme.spacing(3),
            paddingBottom: theme.spacing(2),
        },
        modal: {
            borderRadius: theme.spacing(1),
            width: 300,
            height: 200,
            marginLeft: 'auto',
            marginRight: 'auto',
            marginTop: 200,
            padding: 0
        },
        alert: {
            width: '60%',
            maxWidth: '500px',
            marginLeft: "auto",
            marginRight: "auto",
            marginBottom: theme.spacing(2),
        },
        boxLabel: {
            textAlign: 'center',
            color: 'white',
            backgroundColor: theme.palette.primary.dark,
            borderTopLeftRadius: theme.shape.borderRadius,
            borderTopRightRadius: theme.shape.borderRadius,
            paddingTop: theme.spacing(1),
            paddingBottom: theme.spacing(1)
        },
        wait: {
            paddingTop: 5,
            paddingBottom: 5,
            textAlign: 'center',
            backgroundColor: theme.palette.primary.dark,
            borderTopLeftRadius: 8,
            borderTopRightRadius: 8,
            color: 'white'
        },
        tableContainer: {
            display: 'block',
            position: 'relative',
            padding: theme.spacing(2),
            width: '100%',
            boxSizing: 'border-box',
        },
        firstCol: {
            width: 110
        },
        table: {
            width: "100%",
            overflow: 'scroll',
            display: 'table',
            marginLeft: 'auto',
            marginRight: 'auto'
        },
        iconInline: {
            display: 'inline-block',
            color: theme.palette.primary.dark,
            fontSize: 20
        },
        category: {
            display: 'inline-block',
            marginLeft: 20,
            fontWeight: 500,
            fontSize: 16,
            color: theme.palette.primary.dark
        },
        sentiment: {
            fontWeight: 500,
            fontSize: 16,
            color: theme.palette.primary.dark
        },
        checked: {
            color: theme.palette.secondary.main
        },
        overall: {
            textAlign: 'center',
            marginTop: 10,
            fontSize: 22,
            color: theme.palette.primary.dark
        },
        sentimentIcon: {
            fontSize: 30,
            color: "gray",
            paddingLeft: 5
        }
    })
}, {index: 1});
