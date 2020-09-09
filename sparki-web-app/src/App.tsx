import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import {DatabaseView} from "./DataBaseViewer";



const App: React.FC = () => {

    //Set state always returns [our value, a function to update the value]
    //useSTATE will be ran everrytime we re-render unless we do useState(() => {function})OPtimaization bro!
    const [battery, setBattery] = useState('');
    const [heading, setHeading] = useState('');
    const [ambientLight, setAmbientLight] = useState('');

    //Runs when application loads
    useEffect(()=> {
        fetch('http://172.20.10.7:4000/stats')
            .then(response => response.json())
            .then(response => {
                //response.data[0] is the first column of the database
                setBattery(response.data[0].battery);
                setHeading(response.data[0].heading);
                setAmbientLight(response.data[0].light);
            });
    });



  return (
      <header className="App-header">
          <div>
            <DatabaseView  battery={battery} heading={heading} light={ambientLight}/>
          </div>
      </header>
  )
};

export default App;
