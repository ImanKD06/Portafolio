const express = require("express");
const cors = require("cors");

const app = express();

app.use(express.json());


app.use(cors({
  origin: "https://imankd06.github.io"
}));


app.post("/chat", async (req, res) => {
  try {
    res.json({ response: "Hola desde Render" });
  } catch (error) {
    res.status(500).json({ error: "Error en el servidor" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Servidor corriendo en puerto " + PORT);
});
