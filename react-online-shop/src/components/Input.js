import React from "react"

function Input ({placeholder, inputStyle, labelName, labelStyle, func}) {
    return (
        <div>
            <label style={labelStyle}> {labelName} </label>
            <input onChange={func} style={inputStyle} placeholder={placeholder} />
        </div>
    );
}

export default Input;