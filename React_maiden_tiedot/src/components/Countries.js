import React from 'react'
import Country from './Country'
import Countrylist from './Countrylist'


const Countries = ({countries, handleShow}) => {

    if(countries.length === 1){
        return(
            countries.map(country =>
                <Country key={country.name} country={country} />
            )
        )
    }else if(countries.length <= 10){
        return(
            <Countrylist countries={countries} handleShow={handleShow} />
        )
    }else{
        return(
            <p>Too many matches, specify another filter</p>
        )
    }
}

export default Countries
