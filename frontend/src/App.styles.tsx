import {makeStyles} from "@material-ui/core/styles";
import Image from './pattern.svg';
import Pattern from './Endless-Constellation.svg';

export const useStyles = makeStyles((theme) => {
    return ({
        backgroundImg: {
            display: 'block',
            position: 'fixed',
            bottom: 0,
            boxSizing: 'border-box',
            width: '100%',
            height: 'auto',
            left: 0,
            top: 0,
            right: 0,
            margin: 0,
            background: `url(${Image})`,
            overflow: 'hidden',
            backgroundSize: 'cover',
            zIndex: -10,
        },
        sectionColor: {
            display: "block",
            position: "absolute",
            height: 310,
            width: "100%",
            background: `url(${Pattern})`,
            overflow: 'hidden',
        }
    })
}, {index: 1});
