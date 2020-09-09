//Allows us to  perform routing and respond to various http request methods (GET, POST, PUT, DELETE)
const express = require('express');

/* Cross-Origin-Resource-Sharing
This is what allows our front-end react app to connect with our server and fetch the data being presented.
Without cors() it would fail and nothing would happen. */
const cors = require('cors');

//Allows us to connect to our database
const mysql = require('mysql');


//--------------------------Setup------------------------------//

// //Debug function to verify which path is being captured
// function printPath(req, res, next){
//     console.log(req.path);
//     next();
// }

/*Express.js stuff*/
const app = express();  //Create an instance of express to manage our server
//app.use(printPath,cors());        //Without this line, when we try to fetch from react. Nothing would happen
app.use(cors());        //Without this line, when we try to fetch from react. Nothing would happen

const PORT = 4000;      //The port to listen on

/*Creating the database connection*/
const con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "password",
    database: "SPARKI"
});

con.connect(function(err) {
    if (err) throw err;
});


//--------------------------Controlling GET Requests------------------------------//

//Respond to a GET request at the designated path displaying all values in the stats table
app.get('/stats', (req, res) => {
    con.query("SELECT * FROM stats", (err, result) => {
        if (err) {return res.send(err)}
        else {return res.json({data: result})}
    });
});

//Respond to GET with design to retrieve individual columns
//Format localhost:PORT/stats/get?cell=CELL_NAME
app.get('/stats/get', (req, res) => {
    const {cell} = req.query; //gets the name of the cell from: ?cell=CELL_NAME
    const query = `SELECT ${cell} FROM stats`; //Creates the query selecting the desired cell from stats table
    con.query(query, (err, result) => {
        if (err) {
            return res.send(err);
        } else {
            return res.json({data: result});
        }
    });
});


//--------------------------Starting------------------------------//
app.listen(PORT, () => {
    console.log(`listening and started on PORT: ${PORT}`)
});