import React, { useEffect, useState } from "react";
import { TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import { getDistrictes, getBarris, getParcelesByBounds } from "../../services/api";

function ParcelesMap({ mode, zoom, setZoom, center, setCenter }) {
  const [geojson, setGeoJson] = useState({ type: "FeatureCollection", features: [] });
  const [lastLoad, setLastLoad] = useState(Date.now());
  const [districtes, setDistrictes] = useState(null);
  const [barris, setBarris] = useState(null);

  const map = useMapEvents({
    zoom: () => {
      setZoom(map.getZoom());
    },
    click: e => {
      // console.log(e);
    },
    moveend: e => {
      setCenter(map.getCenter());
    },
  });

  function onFeatureClick(e) {
    map.fitBounds(e.target.getBounds());
  }

  function onEachFeature(feature, layer) {
    layer.on({
      click: onFeatureClick,
    });
  }

  useEffect(() => {
    getDistrictes(true)
      .then(res => {
        setDistrictes(res.data);
        setGeoJson(res.data);
      })
      .then(() => setLastLoad(Date.now()))
      .catch(err => console.log("Error amb la carrega inicial dels districtes"));
  }, []);

  useEffect(() => {
    if (zoom >= 16) {
      getParcelesByBounds({ ...map.getBounds(), geom: true })
        .then(res => {
          setGeoJson(res.data);
        })
        .then(() => setLastLoad(Date.now()))
        .catch(err => console.log("Error al carregar les geometries de les parceles"));
    } else if (zoom >= 13) {
      if (barris === null) {
        getBarris(true)
          .then(res => {
            setBarris(res.data);
            setGeoJson(res.data);
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
  }, [zoom, center]);

  return (
    <>
      <TileLayer url="https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png" />
      <GeoJSON key={lastLoad} data={geojson} onEachFeature={onEachFeature} />
    </>
  );
}

export default ParcelesMap;
