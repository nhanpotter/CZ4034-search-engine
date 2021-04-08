import React, {useEffect} from "react";
import {MuiThemeProvider} from "@material-ui/core/styles";
import {createMuiTheme} from "@material-ui/core";
import {useStyles} from "./App.styles";
import Main from "./Main";
import TextParserWorker from "./TextParserWorker";

const theme = createMuiTheme({
    palette: {
        primary: {
            main: "#1976d2",
            dark: "#115293"
        },
        secondary: {
            main: "#dc004e",
            dark: "#9a0036"
        },
    },
    shape: {
        borderRadius: 25
    }
});

export default function App() {
    const classes = useStyles();

    useEffect(() => {
        TextParserWorker.startWorker();

        return () => {
            TextParserWorker.terminateWorker()
        };
    }, [])
    // @ts-ignore
    return (
        <MuiThemeProvider theme={theme}>
            <div className={classes.backgroundImg}>
            </div>
            <div className={classes.sectionColor}/>
            <Main />
        </MuiThemeProvider>
    );
}
