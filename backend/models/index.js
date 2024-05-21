const Sequelize = require('sequelize');
const sequelizeAutoMigrations = require('sequelize-auto-migrations');

const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'mongodb',
  dialectOptions: {
    useUnifiedTopology: true
  },
  define: {
    timestamps: false
  }
});

const models = {
  User: require('./user')(sequelize), // Importamos y definimos el modelo User
};

sequelizeAutoMigrations(sequelize, models, __dirname);

module.exports = { sequelize, models };
