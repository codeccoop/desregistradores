function Input (props) {
    return (<div className="field">
        <label className="label">{ props.label }</label>
        <div className="control">
            <input className="input" name={ props.name } type={ props.type } value={props.value} onInput={props.onInput} />
        </div>
    </div>)
} 

export default Input;