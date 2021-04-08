import {
    Box,
    Button,
    ButtonBase,
    Checkbox,
    Collapse,
    FormControlLabel,
    Grid,
    Paper,
    Tab,
    Tabs,
    Typography
} from "@material-ui/core";
import React, {useEffect} from "react";
import FilterListIcon from "@material-ui/icons/FilterList";
import {ExpandLess, ExpandMore} from "@material-ui/icons";
import GoogleMapReact from 'google-map-react';
import {useStyles} from "./AdvancedOption.styles";
import LocationOnIcon from '@material-ui/icons/LocationOn';
import QueryAPI from "./api/Query.api";
import ReactDOM from "react-dom";
import FilterIndicator from "./FilterIndicator";

interface TabPanelProps {
    children?: React.ReactNode;
    index: any;
    value: any;
}

function TabPanel(props: TabPanelProps) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            <Box p={3}>
                {children}
            </Box>
        </div>
    );
}

const semanticNames = ['Negative', 'Neutral', 'Positive']

type Restaurant = {
    id: number;
    lat: number;
    lng: number;
    name: string;
    location: string;
}

type AdvancedOptionProps = {
    callback: (locationArr: number[], sentiments: number[]) => any
}

export default function AdvancedOption(props: AdvancedOptionProps) {
    const classes = useStyles();
    const [expandSearch, setExpandSearch] = React.useState(false);
    const [value, setValue] = React.useState(0);
    const [center, setCenter] = React.useState({lat: 1.290270, lng: 103.851959});
    const [zoom, setZoom] = React.useState(15);
    const [locationSet, setLocationSet] = React.useState<any>({});
    const [sentimentsArr, setSentimentsArr] = React.useState<boolean[]>([false, false, false]);
    const disabledLocation = React.useRef<Set<any>>(new Set<unknown>());
    const openInfoWindow = React.useRef<any>(null);

    const handleAdvanceOptionToggle = () => {
        setExpandSearch(!expandSearch);
    }

    const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
        setValue(newValue);
    };

    const renderMarker = (map: any, maps: any) => {
        QueryAPI.listRestaurants((res: { status: number, data: any }) => {
            if (res.status === 0) return;

            processMapData(res.data, map, maps);
        })
    }

    const processMapData = (data: Restaurant[], map: any, maps: any) => {
        data.forEach((e: Restaurant) => {
            let element = new maps.Marker({
                position: {lat: e.lat, lng: e.lng},
                map,
                title: e.name,
                zIndex: 100
            })

            element.addListener('click', (i: any) => {
                let id = "info_" + e.id
                let info = new maps.InfoWindow({
                    content: '<div id=' + id + '>' + e.name + '</div>'
                });

                if (openInfoWindow.current) {
                    openInfoWindow.current.close();
                }

                openInfoWindow.current = info;
                const infoWindowContent = generateInfoWindowContent(e);

                info.open(map, element);
                info.addListener('domready', () => {
                    ReactDOM.render(infoWindowContent, document.getElementById("info_" + e.id));
                })

                info.addListener('closeclick', () => {
                    openInfoWindow.current = null;
                })
            })
        })
    }

    const generateInfoWindowContent = (e: Restaurant) => {
        return (
            <div>
                <h5 style={{marginTop: 8, marginBottom: 8}}>{e.name}</h5>
                <p style={{marginTop: 8, marginBottom: 8}}>{"Address: " + e.location}</p>
                <Button disabled={disabledLocation.current.has(e.id.toString())} variant={'contained'} color={'secondary'}
                        size={'small'}
                        onClick={() => {
                            addLocation(e)
                        }}>
                    Add
                </Button>
            </div>
        )
    }

    const addLocation = (e: Restaurant) => {
        if (openInfoWindow.current) openInfoWindow.current.close();
        let newLocationSet = {};
        // @ts-ignore
        newLocationSet[e.id.toString()] = e;
        setLocationSet((cur: any) => ({...cur, ...newLocationSet}));
    }

    useEffect(() => {
        disabledLocation.current = new Set<any>();
        for (let key in locationSet) {
            if (locationSet[key] === undefined) continue;
            disabledLocation.current.add(key);
        }

    }, [locationSet])

    const renderFilterTagLocation = () => {
        let elements = [];
        for (let key in locationSet) {
            if (locationSet[key] === undefined) continue;

            elements.push(
                <FilterIndicator key={key} id={key} name={locationSet[key].name} tagType={1}
                                 onClickDelete={removeFilterTag}/>
            )
        }

        return elements;
    }

    const renderFilterTagSemantic = () => {
        let elements: JSX.Element[] = [];

        sentimentsArr.forEach((v, index) => {
            if (!v) return;

            elements.push(
                <FilterIndicator key={index - 100} id={index.toString()} name={semanticNames[index]} tagType={0}
                                 onClickDelete={removeFilterTag}/>
            )
        })

        return elements;
    }

    const removeFilterTag = (tagType: number, id: string) => {
        if (tagType === 0) {
            handleSemanticCheck(parseInt(id));
            return;
        }

        // close info window if open to match state changes
        if (openInfoWindow.current) {
            openInfoWindow.current.close();
        }

        let newLocationSet = {};
        // @ts-ignore
        newLocationSet[id] = undefined;
        setLocationSet((cur: any) => ({...cur, ...newLocationSet}));
    }

    const handleSemanticCheck = (index: number) => {
        let newValue = [...sentimentsArr];
        newValue[index] = !sentimentsArr[index];
        setSentimentsArr(newValue);
    }

    useEffect(() => {
        let locations: number[] = [];
        let semantics: number[] = [];

        for (let key in locationSet) {
            if (locationSet[key] === undefined) continue;

            locations.push(parseInt(key));
        }

        sentimentsArr.forEach((e, index) => {
            if (e) {
                semantics.push(index)
            }
        })

        props.callback(locations, semantics);
    }, [locationSet, sentimentsArr])

    return (
        <div>
            <Paper elevation={1} className={`${classes.advancedOption}`}>
                <ButtonBase onClick={handleAdvanceOptionToggle} className={classes.advancedOptionTitle}>
                    <FilterListIcon style={{marginLeft: 0, display: 'block'}}/>
                    <Typography className={classes.optionPhrase}>Advanced options</Typography>
                    {expandSearch ? <ExpandLess className={classes.expand}/> : <ExpandMore className={classes.expand}/>}
                </ButtonBase>
                <Collapse in={expandSearch} unmountOnExit>
                    <Tabs
                        value={value}
                        onChange={handleChange}
                        indicatorColor="primary"
                        textColor="primary"
                        centered
                        variant="fullWidth"
                    >
                        <Tab label="Location"/>
                        <Tab label="Sentiment"/>
                    </Tabs>

                    <TabPanel value={value} index={0}>
                        <Typography className={classes.optionGuide} component={"p"}>Click the markers on the map to filter the reviews by restaurants</Typography>
                        <div className={classes.mapDisplay}>
                            <GoogleMapReact
                                bootstrapURLKeys={{key: "AIzaSyCQFwSOrzigBfDVuDpSZHof5lb4dRnh4_s"}}
                                defaultCenter={center}
                                defaultZoom={zoom}
                                yesIWantToUseGoogleMapApiInternals
                                onGoogleApiLoaded={({map, maps}) => renderMarker(map, maps)}
                            >
                            </GoogleMapReact>
                        </div>
                    </TabPanel>
                    <TabPanel value={value} index={1}>
                        <Typography className={classes.optionGuide} component={"p"}>Choose the sentiment criteria for reviews</Typography>
                        <Grid container direction="row" alignItems="center">
                            <Grid item xs={4}>
                                <FormControlLabel
                                    control={<Checkbox color={"primary"} checked={sentimentsArr[0]}
                                                       onChange={() => handleSemanticCheck(0)}/>}
                                    label="Negative"
                                />
                            </Grid>
                            <Grid item xs={4}>
                                <FormControlLabel
                                    control={<Checkbox color={"primary"} checked={sentimentsArr[1]}
                                                       onChange={() => handleSemanticCheck(1)}/>}
                                    label="Neutral"
                                />
                            </Grid>
                            <Grid item xs={4}>
                                <FormControlLabel
                                    control={<Checkbox color={"primary"} checked={sentimentsArr[2]}
                                                       onChange={() => handleSemanticCheck(2)}/>}
                                    label="Positive"
                                />
                            </Grid>
                        </Grid>
                    </TabPanel>
                </Collapse>
            </Paper>
            <div className={`${classes.layout}`}>
                {renderFilterTagLocation()}
                {renderFilterTagSemantic()}
            </div>
        </div>
    )
}
