import React, {useState, useEffect} from 'react'
import axios from 'axios'

// muuttujassa api_key on nyt käynnistyksessä annettu api-avaimen arvo
const api_key = process.env.REACT_APP_API_KEY

const Country = ({country}) =>{
    const [temperature, setNewTemperature ] = useState('')
    const [icon, setNewIcon ] = useState('')
    const [windDir, setNewWindDir ] = useState('')
    const [windSpeed, setNewWindSpeed ] = useState('')

    useEffect( () => {
        axios
            .get('http://api.weatherstack.com/current?access_key=' + api_key + '&query=' + country.capital)
            .then(response => {
                const weather = response.data
                setNewTemperature(weather.current.temperature)
                setNewIcon(weather.current.weather_icons[0])
                setNewWindDir(weather.current.wind_dir)
                setNewWindSpeed(weather.current.wind_speed)
            })
    }, [])
   
    //If axios haven't already gathered the weather data, information is shown without it
    //this isn't usually visible for user because the update is so quick
    return(
        <div>
            <h2>{country.name}</h2>
            <p>
                capital {country.capital}
                <br/>
                population {country.population}
            </p>
            <h3>Spoken languages</h3>
            <ul>
                {country.languages.map(language => <li key={language.name}>{language.name}</li>)}
            </ul>
            <img src={country.flag} width={100}></img>
            <h3>Weather in {country.capital}</h3>
            <p><strong>temperature:</strong> {temperature} Celsius</p>
            <img widht={50} src={icon}></img>
            <p><strong>wind:</strong> {windSpeed} mph direction {windDir}</p>
        </div>
    )
    
}

export default Country