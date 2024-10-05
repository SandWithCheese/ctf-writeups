import express from 'express';
import dotenv from 'dotenv';
import path from 'path';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { getAllRecipes, getRecipe, migrate } from './database.js';
dotenv.config();

const port = process.env.APP_PORT || 3000;
const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json({ extended: true }));

app.get('/', async (req, res) => {
    const id = req.query.id;
    try{
        if (!id) {
            let recipes = await getAllRecipes();
            res.render('index', { recipes: recipes });
        } else {
            let [recipe] = await getRecipe(id);
            if (!recipe) {
                throw new Error('Recipe not found');
            }
            res.render('recipe', { recipe: recipe });
        }
    } catch (err) {
        res.status(404).render('errors/404');
    }
});

app.get('/about', (req, res) => {
    res.render('about');
});

app.get('/contact', (req, res) => {
    res.render('contact');
});

app.listen(port, () => {
    migrate();
    console.log(`Server is running on http://localhost:${port}`);
});
