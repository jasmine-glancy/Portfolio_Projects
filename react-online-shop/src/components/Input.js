import React from "react"

function Input ({placeholder, inputStyle, labelName, labelStyle}) {
    return (
        <div>
            <label style={labelStyle}> {labelName} </label>
            <input style={inputStyle} placeholder={placeholder} />
        </div>
    );
}

export default Input;