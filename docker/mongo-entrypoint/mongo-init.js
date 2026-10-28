const APP_USER = process.env.MONGO_APP_USERNAME;
const APP_PASS = process.env.MONGO_APP_PASSWORD;
const INIT_DB = process.env.MONGO_INITDB_DATABASE;

if (!APP_USER) throw new Error("MONGO_APP_USERNAME is not set");
if (!APP_PASS) throw new Error("MONGO_APP_PASSWORD is not set");
if (!INIT_DB) throw new Error("MONGO_INITDB_DATABASE is not set");

db = db.getSiblingDB(INIT_DB);

db.createUser({
  user: APP_USER,
  pwd: APP_PASS,
  roles: [{ role: "readWrite", db: INIT_DB }],
});
