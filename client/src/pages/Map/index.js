import React, {useEffect, useState} from "react";
import {MapContainer, TileLayer, GeoJSON, useMapEvent} from "react-leaflet";
import "./style.scss"

function onEachFeatureInputMode (feature, layer) {
    layer.on({
        click: onFeatureClick
    });
}

function onEachFeatureViewMode (feature, layer) {}

function onFeatureClick (ev) {
    console.log(ev);
}

function Map(props) {
    function MapEvents () {
        const map = useMapEvent("zoom", () => {
            console.log("zoom change");
            setZoom(map.getZoom());
        });

        return null;
    }

    const [geojson, setGeoJson] = useState({type: "FeatureCollection", features: []})
    const [lastLoad, setLastLoad] = useState(Date.now());
    const [districtes, setDistrictes] = useState(null);
    const [barris, setBarris] = useState(null);
    const [zoom, setZoom] = useState(12);

    useEffect(() => {
        fetch("data/geometries/districtes.geojson")
            .then(res => res.json())
            .then(data => {
                setDistrictes(data);
                setGeoJson(data);
            })
            .then(() => setLastLoad(Date.now()))
            .catch(err => console.log("Error amb la carrega inicial dels districtes"));
    }, []);

    useEffect(() => {
        if (zoom >= 13) {
            if (barris === null) {
                fetch("data/geometries/barris.geojson")
                    .then(res => res.json())
                    .then(data => {
                        setBarris(data);
                        setGeoJson(data);
                    })
                    .then(() => setLastLoad(Date.now()))
                    .catch(err => console.log("Error al carregar les geometries dels barris"));
            } else {
                setGeoJson(barris);
                setLastLoad(Date.now());
            }
        } else {
            setGeoJson(districtes);
            setLastLoad(Date.now());
        }
    }, [zoom])

    return (
        <div className="map">  
            <h1 className="title is-1"> Hola sóc un Mapa</h1>
            <MapContainer className="map__container" center={[41.41, 2.13]} zoom={zoom}>
                <MapEvents />
                <TileLayer
                    url="https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png"
                />
                <GeoJSON key={lastLoad} data={geojson} onEachFeature={props.mode === 'input' ? onEachFeatureInputMode : onEachFeatureViewMode}/>
            </MapContainer>
        </div>
    );
  }
  
  export default Map;