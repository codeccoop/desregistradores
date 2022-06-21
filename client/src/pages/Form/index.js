import Map from "../Map";
import { useState } from "react";
import Input from "./Input";
import { submitNote } from "../../services/api.js";

function Form() {
  const [form, updateForm] = useState({
    titular: "",
    titular_id: "",
    municipi: "",
    barri: "",
    refcat: "",
    data: "",
    comentari: "",
  });
  const [message, setMessage] = useState({
    content: null,
    type: null,
  });

  const fields = [
    {
      label: "Nom de la propietat",
      name: "titular",
      type: "text",
      value: form.titular,
    },
    {
      label: "NIF/CIF de la propietat",
      name: "titular_id",
      type: "text",
      value: form.titular_id,
    },
    {
      label: "Municipi",
      name: "municipi",
      type: "text",
      value: form.municipi,
    },
    {
      label: "Barri",
      name: "barri",
      type: "text",
      value: form.barri,
    },
    {
      label: "Referència Cadastral",
      name: "refcat",
      type: "text",
      value: form.refcat,
    },
    {
      label: "Data",
      name: "data",
      type: "date",
      value: form.data,
    },
  ];

  function onSubmit() {
    submitNote(form).then(onSubmitSuccess).catch(onSubmitError);
  }
  function onSubmitSuccess() {
    setMessage({
      content: "El teu formulari s'ha guardat amb èxit.",
      type: "success",
    });
    formReset();
  }

  function onSubmitError() {
    setMessage({
      content:
        "Hi ha hagut un problema amb el formulari i no s'ha desat. Si us plau, intenta-ho de nou.",
      type: "danger",
    });
    formReset();
  }

  function formReset() {
    updateForm({
      titular: "",
      titular_id: "",
      municipi: "",
      barri: "",
      refcat: "",
      data: "",
      comentari: "",
    });
  }

  const onInput = ev => {
    updateForm({
      ...form,
      [ev.target.name]: ev.target.value,
    });
  };

  function formContent() {
    if (message.type != null) {
      return (
        <div className={"notification is-" + message.type}>
          <button
            className="delete"
            onClick={() => setMessage({ content: null, type: null })}
          ></button>
          {message.content}
        </div>
      );
    } else {
      return (
        <>
          {fields.map(field => {
            const props = { ...field, onInput: onInput };
            return <Input {...props} key={props.name} />;
          })}
          <div className="field">
            <label className="label">Comentaris</label>
            <div className="control">
              <textarea
                className="textarea"
                name="comentari"
                type="text"
                value={form.comentari}
                onInput={onInput}
              />
            </div>
          </div>
          <div className="field is-grouped">
            <div className="control">
              <button className="button is-link" onClick={onSubmit}>
                Enviar
              </button>
            </div>
            <div className="control">
              <button className="button is-light" onClick={formReset}>
                Cancel·lar
              </button>
            </div>
          </div>
        </>
      );
    }
  }

  return (
    <main className="form">
      <div className="form__content columns">
        <div className="form__items column">
          <h1 className="title is-1"> Hola sóc un Formulari</h1>
          {formContent()}
        </div>
        <div className="form__map column">
          <Map mode={"input"} />
        </div>
      </div>
    </main>
  );
}

export default Form;

