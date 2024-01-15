require('dotenv').config();
const express = require('express');
const app = express();
const cors = require('cors');
const logger = require('./middleware/logger');

// set host and port
const HOST = '0.0.0.0';
const PORT = process.env.PORT || 8080;

// set express settings
app.use(cors());
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

// use middleware
app.use(logger);

// root response
app.get('/', (req, res) => {
    res.status(200).json({ 'message': 'Hello World' });
});

console.log(`server running on port: ${PORT}`);
app.listen(PORT, HOST);
