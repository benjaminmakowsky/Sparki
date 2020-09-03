/**
 * 1. Create Folder
 * 2. npm install express, cors
 */

//Allows us to  perform routing and respond to various http request methods (GET, POST, PUT, DELETE)
const express = require('express');


//--------------------------Setup------------------------------//


/*Express.js stuff*/
const app = express();  //Create an instance of express to manage our server

const PORT = 4000;      //The port to listen on


//--------------------------Controlling GET Requests------------------------------//

//Respond to GET request at the base level of our server
app.get('/', (req, res) => {
    res.send("This is the root of the server")
});

//Respond to a GET request at the designated path displaying all values in the stats table
app.get('/next', (req, res) => {
    res.send("This is /next")
});

//Respond to GET with design to retrieve individual columns
//Format localhost:PORT/next/getArgs?arg=ARG
app.get('/next/getArgs', (req, res) => {
    const {arg} = req.query; //gets the name of the cell from: ?cell=CELL_NAME
    res.send(`Passed in: ${arg}`);
});


//--------------------------Starting------------------------------//
app.listen(PORT, () => {
    console.log(`listening and started on PORT: ${PORT}`)
});