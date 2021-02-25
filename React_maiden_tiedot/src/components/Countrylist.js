import React from 'react'

const Countrylist = ({countries, handleShow}) =>{
    return(
        <div>
            {countries.map(
                country =>
                <p key={country.name}>{country.name} <button onClick={handleShow.bind(this, country.name)}>show</button></p>
            )}
        </div>
    )
}

export default Countrylist