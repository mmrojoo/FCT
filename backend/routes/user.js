const express = require('express');
const bcrypt = require('bcryptjs');
const { models } = require('../models');

const router = express.Router();
const User = models.User;

router.post('/register', async (req, res) => {
  const { nombre, apellidos, correoElectronico, username, password } = req.body;

  try {
    // Verificar si el correo electrónico o el nombre de usuario ya existen
    const existingUser = await User.findOne({
      where: {
        [models.Sequelize.Op.or]: [
          { username },
          { correoElectronico }
        ]
      }
    });

    if (existingUser) {
      return res.status(400).json({ message: 'Nombre de usuario o correo electrónico ya registrado' });
    }

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const newUser = await User.create({
      nombre,
      apellidos,
      correoElectronico,
      username,
      password
    });

    res.status(201).json(newUser);
  } catch (error) {
catch (error) {
  console.error('Error al registrar usuario', error);
  res.status(500).json({ message: 'Error al registrar usuario' });
}
  }
});

module.exports = router;
