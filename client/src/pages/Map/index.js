import { useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import ParcelesMap from "../../components/ParcelesMap";
import "./style.scss";

function Map(props) {
  const [center, setCenter] = useState(null);
  const [zoom, setZoom] = useState(12);

  return (
    <div className="map">
      <h1 className="title is-1"> Hola sóc un Mapa</h1>
      <MapContainer className="map__container" center={[41.41, 2.13]} zoom={zoom}>
        <ParcelesMap
          mode={props.mode}
          zoom={zoom}
          setZoom={setZoom}
          center={center}
          setCenter={setCenter}
        />
      </MapContainer>
    </div>
  );
}

export default Map;
