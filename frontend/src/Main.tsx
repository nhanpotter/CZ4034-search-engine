import {useStyles} from "./Main.styles";
import React, {useEffect} from "react";
import {
    ButtonBase,
} from "@material-ui/core";
import {Link, Route, Switch, Redirect} from 'react-router-dom';
import Search from "./Search";
import Crawl from "./Crawl";
import Classification from "./Classification";

type routeObject = {
    name: string,
    url: string,
    component: JSX.Element
}

const navigationLink: routeObject[] = [
    {
        name: 'Search',
        url: '/search',
        component: <Search />
    },
    {
        name: 'Classification',
        url: '/classify',
        component: <Classification />
    },
    {
        name: 'Crawl',
        url: '/crawl',
        component: <Crawl />
    },
]

export default function Main() {
    const classes = useStyles();

    // @ts-ignore
    return (
        <div>
            <div className={classes.paper}>
                <div className={classes.navBar}>
                    {navigationLink.map(e => (
                        <div key={e.name} className={classes.wrapNavBtn}>
                            <Link to={e.url} style={{textDecoration: 'none'}}><ButtonBase className={classes.navBtn}>{e.name}</ButtonBase></Link>
                        </div>
                    ))}
                </div>

                <Switch>
                    {navigationLink.map(e => (
                        <Route path={e.url} component={() => e.component}/>
                    ))}

                    <Redirect to="/search" />
                </Switch>
            </div>
        </div>
    );
}
