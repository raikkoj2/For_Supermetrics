import React from 'react'

const Filter = ({handleFilterChange, newFilter}) => (
    <div>
        Find countries <input value={newFilter} onChange={handleFilterChange}/>
    </div>
)

export default Filter