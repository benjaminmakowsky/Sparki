import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import {TextField} from "./TextField";
import {DatabaseView} from "./DataBaseViewer";



const App: React.FC = () => {

    //Set state always returns [our value, a function to update the value]
    //useSTATE will be ran everrytime we re-render unless we do useState(() => {function})OPtimaization bro!
    const [battery, setBattery] = useState('');
    const [heading, setHeading] = useState('');

    //Runs when application loads
    useEffect(()=> {
        fetch('http://localhost:4000/stats')
            .then(response => response.json())
            .then(response => {
                //response.data[0] is the first column of the database
                setBattery(response.data[0].battery);
                setHeading(response.data[0].heading);
            });
    });



  return (
      <header className="App-header">
          <div>
            <TextField text={"SPARKI"}/>
            <DatabaseView  battery={battery} heading={heading}/>
          </div>
      </header>
  )
};

export default App;
