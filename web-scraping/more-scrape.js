// this was some last-minute downloading of Selena, Odin, and Laslow's sprites
// because I made a small error when importing their sprites to MongoDB from the wiki

const { MongoClient } = require('mongodb');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// MongoDB connection URI (local)
const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

// Folder where gifs will be saved
const saveDir = path.join(__dirname, 'assets', 'sprites');

async function main() {
    try {
        await client.connect();
        const db = client.db('FEConquest');
        const collection = db.collection('characters');

        const targetNames = ['Selena', 'Laslow', 'Odin'];

        const characters = await collection.find({ name: { $in: targetNames } }).toArray();

        for (const char of characters) {
            const { name, sprites } = char;

            if (!sprites) continue;

            for (const className in sprites) {
                const gifUrl = sprites[className];
                const filename = `${name}-${className}.gif`;
                const filepath = path.join(saveDir, filename);

                try {
                    const response = await axios.get(gifUrl, { responseType: 'arraybuffer' });
                    fs.writeFileSync(filepath, response.data);
                    console.log(`Downloaded: ${filename}`);
                } catch (err) {
                    console.error(`Failed to download ${gifUrl} for ${filename}:`, err.message);
                }
            }
        }
    } catch (err) {
        console.error('Connection or query failed:', err);
    } finally {
        await client.close();
    }
}

main();
