import mysql from 'mysql2';
import dotenv from 'dotenv';
dotenv.config();

const conn = mysql.createPool({
    host: process.env.DB_HOST || '127.0.0.1',
    user: process.env.DB_USER || 'root', 
    password: process.env.DB_PASS || 'MySQL',
    database: process.env.DB_DATABASE || 'chicken_daddy',
}).promise();

export async function migrate() {
    conn.query('CREATE TABLE IF NOT EXISTS recipes (id INT PRIMARY KEY, name TEXT, img_url TEXT, description TEXT, instructions TEXT)')
        .then(() => {
            conn.query('INSERT IGNORE INTO recipes (id, name, img_url, description, instructions) VALUES (1, "Ayam Geprek: The Classic", "/imgs/ayam_geprek.png", "Your average ayam geprek. Simple, yet... Delicioso 🤌✨", "1. Get the chicken\n2. Geprek the chicken\n3. Cook the chicken\n4. Eat the chicken")')
            conn.query('INSERT IGNORE INTO recipes (id, name, img_url, description, instructions) VALUES (2, "Ayam Bakar: Hell Forged", "/imgs/ayam_bakar.png", "Forged in the inferno\'s embrace, a dish that is guaranteed to give you cancer 💀💀", "1. Catch the chicken\n2. Open a portal to the underworld\n3. Roast the chicken in demonic flames\n4. Voilà, savor your extra crispy, inferno-grilled dinner!")')
            conn.query('INSERT IGNORE INTO recipes (id, name, img_url, description, instructions) VALUES (3, "Ayam Sorry", "/imgs/ayam_sorry.png", "Ku tak akan love you lagi 💔", "Cintaku, cintaku padamu\nTak besar seperti dulu\nKamu kok begitu menilai cintaku\nBegitu rendah di matamu?\nSayangku, sayangku padamu\nTak indah seperti dulu\nMaumu begini, maumu begitu\nTak pernah engkau hargai aku\nOh-oh, I am sorry\nKu tak akan love you lagi\nKupeluk, memeluk dirimu\nTak hangat seperti dulu\nKu jadi selingkuh kar\'na kau selingkuh\nBiar sama-sama kita selingkuh\nOh-oh, I am sorry\nKu tak akan love you lagi\nBiar kuputuskan saja\nKu tak mau hatiku terluka\nLebih baik kucukupkan saja\nKu tak mau batinku tersiksa\nJangan kau s\'lalu merasa\nWanita bukan dirimu saja\nLebih baik kuputuskan saja\nCari pacar lagi\nOh, yeah\nSya-na-na-na-na-na\nSya-na-na-na-na-na-na-na\nBiar kuputuskan saja\nKu tak mau hatiku terluka\nLebih baik kucukupkan saja\nKu tak mau batinku tersiksa\nJangan kau s\'lalu merasa\nWanita bukan dirimu saja\nLebih baik kuputuskan saja\nCari pacar lagi, wo\nBiar kuputuskan saja\nKu tak mau hatiku terluka\nLebih baik kucukupkan saja\nKu tak mau batinku tersiksa\nJangan kau s\'lalu merasa\nWanita bukan dirimu saja\nLebih baik kuputuskan saja\nCari pacar lagi, wo-oh\nCari pacar lagi, wo-oh\nCari pacar lagi")')
            conn.query('INSERT IGNORE INTO recipes (id, name, img_url, description, instructions) VALUES (4, "Le PapaChicken", "/imgs/papachicken.png", "The ultimate chicken dish, a divine creation that will make you question your existence. 🐔👑", "1. Summon the chicken god\n2. Offer your soul to the chicken god\n3. Prepare to be blessed with the ultimate chicken dish\n4. Ascend to chicken heaven")')
        })
}

//functions to interact with the database
export async function getAllRecipes() {
    try {
        const [results] = await conn.query('SELECT * FROM recipes')
        return results;
    } catch (err) {
        console.log(err);
    }
}

export async function getRecipe(id) {
    const [results] = await conn.query(`SELECT * FROM recipes WHERE id = ${id}`);
    return results;
}