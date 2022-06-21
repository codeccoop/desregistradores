const apiURL = process.env.REACT_APP_API;

export function submitNote(note) {
  return fetch(`${apiURL}notes-simples`, {
    method: "POST",
    body: JSON.stringify({ data: note }),
    headers: {
      Accept: "application/json; charset=UTF-8",
      "Content-Type": "application/json; charset=UTF-8",
    },
  })
    .then(res => res.json())
    .then(db_entry => {
      return fetch(`${apiURL}comentaris`, {
        method: "POST",
        body: JSON.stringify({
          data: {
            text: note.comentari,
            nota_simple: db_entry.data.id,
          },
        }),
        headers: {
          Accept: "application/json; charset=UTF-8",
          "Content-Type": "application/json; charset=UTF-8",
        },
      });
    });
}

export function requestNotesSimples() {
  return fetch(`${apiURL}notes-simples`, {
    method: "GET",
    headers: {
      Accept: "application/json; charset=UTF-8",
    },
  }).then(res => res.json());
}

export function getDistrictes(geom = false) {
  return fetch(`${apiURL}districtes?geom=${geom}`, {
    method: "GET",
    headers: {
      Accept: "application/json; charset=UTF-8",
    },
  }).then(res => res.json());
}

export function getBarris(geom = false) {
  return fetch(`${apiURL}barris?geom=${geom}`, {
    method: "GET",
    headers: {
      Accept: "application/json; charset=UTF-8",
    },
  }).then(res => res.json());
}

export function getParcelesByBounds({ _northEast, _southWest, geom }) {
  const bbox = {
    west: _southWest.lng,
    south: _southWest.lat,
    east: _northEast.lng,
    north: _northEast.lat,
  };
  return fetch(`${apiURL}parceles?geom=${geom}`, {
    method: "POST",
    headers: {
      Accept: "application/json; charset=UTF-8",
      "Content-Type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify(bbox),
  }).then(res => res.json());
}
