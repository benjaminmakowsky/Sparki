//JavaScript import statements
var http = require('http');
var mysql = require('mysql')

//create the server
var server = http.createServer();

//create a connection to the database
var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "password",
  database: "messages"
});

con.connect(function(err) {
  if (err) throw err;
});

//Create a listener  that response with a request with a webpage
server.addListener('request', (request, response) => {
  response.writeHead(200); // HTTP Status Code 200 - Okay.
  con.query("SELECT * FROM messages", (err, result) => {
    if(err){
      response.write(err)
    } else {
      response.write(JSON.stringify(result));
    }
    response.end(); // Finish and send the response.
  });
});



// default port will do fine
const port = 8080;
server.listen(port); 
console.log("The Node Server is running");