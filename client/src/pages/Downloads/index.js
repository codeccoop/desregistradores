import { requestNotesSimples } from "../../services/api";
import React, { useState, useEffect } from "react";

function Downloads() {
  const [notesSimples, updateNotes] = useState([]);
  const [municipiState, updateMunicipi] = useState();
  useEffect(() => {
    //fem servir useEffect perquè volem carregar les dades des del principi, quan es carrega el DOM
    requestNotesSimples().then((res) => {
      updateNotes(res.data);
    });
  }, []);

  function stringifyNotes() {
    return ["municipi,barri,titular,dni titular,data"]
      .concat(
        notesSimples.map((item) => {
          const { data, municipi, titular, titular_id, barri } =
            item.attributes;
          return [municipi, barri, titular, titular_id, data].join(",");
        })
      )
      .join("\n");
  }

  function downloadNotes() {
    const tableData = stringifyNotes();
    const blob = new Blob([tableData], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "notes-simples.csv";
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
  }

  // const notesSimples = async () => {
  //   const resp = await requestNotesSimples();
  //   console.log(resp);
  //   return (
  //     <div className="notes-feed">
  //       {resp.data.map((item, index) => {
  //         return <li key={index}>{item.id}</li>;
  //       })}
  //     </div>
  //   );
  // };

  return (
    <main className="downloads">
      <p className="downloads-text">
        Pots decsarregar les dades de les notes simples en format .csv fent
        click al botó
      </p>
      <button onClick={downloadNotes}>Descarrega les dades</button>
      <form id="data-filters">
        <label for="municipi">Selecciona un municipi:</label>
        <select
          name="municipi"
          id="selector-municipi"
          value={municipiState}
          onChange={(e) => {
            updateMunicipi(e.currentTarget.value);
          }}
        >
          {console.log(municipiState)}
          <option value="empty"></option>
          {notesSimples.map((item, key) => {
            return (
              <option value={item.attributes.municipi}>
                {item.attributes.municipi}
              </option>
            );
          })}
          ;
        </select>
      </form>
      <table className="display-notes">
        <tbody>
          {/* {Utilitzar el metode filter per arrays} */}
          {notesSimples.map((item) => {
            return (
              <tr>
                <td>{item.id}</td>
                <td>{item.attributes.titular}</td>
              </tr>
            );
          })}
          ;
        </tbody>
      </table>
    </main>
  );
}
export default Downloads;
