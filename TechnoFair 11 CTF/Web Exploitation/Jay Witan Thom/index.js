const express = require('express');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();
const app = express();
const port = 1945;

const SECRET_KEY = process.env.SECRET_KEY;

const users = [
    {
        id: 1,
        username: 'user',
        password: 'password',
        role: 'user' 
    },
];

app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static('public'));

app.get('/',(req,res) => {
    res.render('index');
})
app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;

    const user = users.find(u => u.username === username && u.password === password);
    if (user) {
        const token = jwt.sign({ id: user.id, username: user.username, role: user.role }, SECRET_KEY, { expiresIn: '1h' });
        res.cookie('token', token, { httpOnly: true });
        res.json({ message: 'Login successful!' });
    } else {
        res.status(401).json({ message: 'Invalid credentials' });
    }
});

const authenticateToken = (req, res, next) => {
    const token = req.cookies.token;

    if (!token) return res.sendStatus(401);

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) return res.sendStatus(403);

        req.user = user;
        next();
    });
};

const checkAdminRole = (req, res, next) => {
    if (req.user.role !== 'admin') {
        return res.status(403).json({ message: 'Access forbidden: Admins only' });
    }
    next();
};

app.get('/flag', authenticateToken, (req, res) => {
    res.render('flag', { user: req.user });
});

app.get('/readfile', authenticateToken, checkAdminRole, (req, res) => {
    const filePath = path.join(__dirname, 'flag.txt');
    
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ message: 'Error reading file', error: err });
        }
        
        res.json({ content: data });
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
