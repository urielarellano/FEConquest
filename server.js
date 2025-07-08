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
        const characters = await db.collection("characters")
          .find()
          .sort({ _id: 1 }) // <-- Added this
          .toArray();
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

    app.get("/characters/:name/previous", async (req, res) => {
      try {
        const current = await db.collection("characters").findOne({ name: req.params.name });

        if (!current) {
          return res.status(404).send("Current Character not found.");
        }

        const previous = await db.collection("characters")
          .find({ _id: { $lt: current._id } })  // Find earlier insertions
          .sort({ _id: -1 })                    // Sort descending (closest earlier one)
          .limit(1)
          .toArray();

        if (previous.length === 0) {
          return res.status(404).send("No previous character found.");
        }

        res.json(previous[0]);
      } catch (err) {
        console.error(err);
        res.status(500).send("Error finding previous character.");
      }
    });

    app.get("/characters/:name/next", async (req, res) => {
      try {
        const current = await db.collection("characters").findOne({ name: req.params.name });

        if (!current) {
          return res.status(404).send("Character not found.");
        }

        const next = await db.collection("characters")
          .find({ _id: { $gt: current._id } })  // Find later insertions
          .sort({ _id: 1 })                     // Sort ascending (closest later one)
          .limit(1)
          .toArray();

        if (next.length === 0) {
          return res.status(404).send("No next character found.");
        }

        res.json(next[0]);
      } catch (err) {
        console.error(err);
        res.status(500).send("Error finding next character.");
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

    const path = require("path");

    app.use(express.static(path.join(__dirname)));

    app.get("/", (req, res) => {
      res.sendFile(path.join(__dirname, "index.html"));
    });


    app.listen(port, () => {
      console.log(`Server running at http://localhost:${port}`);
    });

  } catch (err) {
    console.error("MongoDB connection error:", err);
  }
}

startServer();