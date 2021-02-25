import axios from 'axios'
import React, { useState, useEffect } from 'react'
import Filter from './components/Filter'
import Countries from './components/Countries'


const App = () => {
    const [ newFilter, setNewFilter ] = useState('')
    const [countries, setNewCountries ] = useState([])
    useEffect( () => {
        axios
            .get('https://restcountries.eu/rest/v2/all')
            .then(response => {
                setNewCountries(response.data)
            })
    }, [])
    //console.log(countries)
    const handleFilterChange = (event) => {
        setNewFilter(event.target.value)
    }

    const handleShow = (country) => {
        setNewFilter(country)
    }

    const filteredCountries = countries.filter(country => country.name.toLowerCase().includes(newFilter.toLowerCase()))

    return(
        <div>
            <h1>
                Search country and weather infromation
            </h1>
            <Filter handleFilterChange={handleFilterChange} newFilter={newFilter} />
            <Countries countries={filteredCountries} handleShow={handleShow}/>
            
        </div>
    )
}

export default App