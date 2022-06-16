import { requestNotesSimples } from "../../services/api";

function Downloads() {
  const obtainNotesSimples = async () => {
    const resposta = await requestNotesSimples();
    const tableData = ["municipi,barri,titular,dni titular,data"]
      .concat(
        resposta.data.map((item) => {
          const { data, municipi, titular, titular_id, barri } =
            item.attributes;
          return [municipi, barri, titular, titular_id, data].join(",");
        })
      )
      .join("\n");

    const blob = new Blob([tableData], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "notes-simples.csv";
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
  };

  return (
    <main className="downloads">
      <p className="downloads-text">
        Pots decsarregar les dades de les notes simples en format .csv fent
        click al botó
      </p>
      <button onClick={obtainNotesSimples}>Descarrega les dades</button>
    </main>
  );
}
export default Downloads;
