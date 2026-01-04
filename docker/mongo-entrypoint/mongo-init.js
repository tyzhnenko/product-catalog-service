const USER = process.env.MONGO_INITDB_ROOT_USERNAME || "admin";
const PASS = process.env.MONGO_INITDB_ROOT_PASSWORD || "admin_password";
const INIT_DB = process.env.MONGO_INITDB_DATABASE || "admin";

db = db.getSiblingDB(INIT_DB);

db.createUser({
  user: USER,
  pwd: PASS,
  roles: [{ role: "readWrite", db: INIT_DB }],
});
