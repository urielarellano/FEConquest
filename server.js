const express = require("express");
const { MongoClient } = require("mongodb");
const cors = require("cors");
require('dotenv').config();

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

async function startServer() {
  try {
    await client.connect();
    const db = client.db("FEConquest");
    console.log("Connected to MongoDB");

    // Register routes here, with access to db:
    app.get("/characters", async (req, res) => {
      try {
        const characters = await db.collection("characters").find().toArray();
        res.json(characters);
      } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching characters.");
      }
    });

    app.get("/characters/:name", async (req, res) => {
      try {
        const characterName = req.params.name;
        const character = await db.collection("characters").findOne({ name: characterName });
        
        if (!character) {
          return res.status(404).send("Character not found.");
        }
        
        res.json(character);
      } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching character.");
      }
    });

    app.get("/classes", async (req, res) => {
      try {
        const classes = await db.collection("classes").find().toArray();
        res.json(classes);
      } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching classes.");
      }
    });

    app.get("/classes/:className", async (req, res) => {
      try {
        const className = req.params.className;
        const classInfo = await db.collection("classes").findOne({ class: className });
        
        if (!classInfo) {
          return res.status(404).send("Class not found.");
        }
        
        res.json(classInfo);
      } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching class.");
      }
    });

    app.listen(port, () => {
      console.log(`Server running at http://localhost:${port}`);
    });

  } catch (err) {
    console.error("MongoDB connection error:", err);
  }
}

startServer();