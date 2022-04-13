import Map from "../Map";
import {useState} from "react";
import Input from "./Input";

function Form() {
    const [form, updateForm] = useState({
        titular: "",
        id: "",
        municipi: "",
        barri: "",
        data: "",
        comentari: ""
    });

    const fields = [
        {
            label: "Nom de la propietat",
            name: "titular",
            type: "text",
            value: form.titular
        },
        {
            label: "NIF/CIF de la propietat",
            name: "id",
            type: "text",
            value: form.id
        },
        {
            label: "Municipi",
            name: "municipi",
            type: "text",
            value: form.municipi
        },
        {
            label: "Barri",
            name: "barri",
            type: "text",
            value: form.barri
        },
        {
            label: "Data",
            name: "data",
            type: "date",
            value: form.data
        }
    ];

    function onSubmit () {
        fetch("api/form", {
            method: "POST",
            body: JSON.stringify(form),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(res => console.log("Formulari arxivat"))
        .catch(err => "oohh...");
    }

    function onCancel () {}

    const onInput = (ev) => {
        updateForm({
            ...form,
            [ev.target.name]: ev.target.value
        });
    }
    
    return (
        <main className="form">
            <div className="form__content columns">
                <div className="form__items column">
                    <h1 className="title is-1"> Hola sóc un Formulari</h1>
                    {fields.map(field => {
                        const props = {...field, onInput: onInput}
                        return (<Input {...props} />)
                    })}
                    <div className="field">
                        <label className="label">Comentaris</label>
                        <div className="control">
                            <textarea className="textarea" name="comentari" type="text" value={form.comentari} onInput={onInput}/>
                        </div>
                    </div>
                    <div className="field is-grouped">
                        <div className="control">
                            <button className="button is-link" onClick={onSubmit}>
                                Enviar
                            </button>
                        </div>
                        <div className="control">
                            <button className="button is-light" onClick={onCancel}>
                                Cancel·lar
                            </button>
                        </div>
                    </div>
                </div>
                <div className="form__map column">
                    <Map mode={'input'}/>
                </div>
            </div>
        </main>
        
    );
  }
  
  export default Form;