import fs from 'fs';
const DB_PATH = process.env.DATA_FILE || 'data/db.json';
const seed = { scans: [], auditLogs: [], messageLogs: [], paymentRecords: [], bookingRecords: [] };
function ensure() { if (!fs.existsSync('data')) fs.mkdirSync('data'); if (!fs.existsSync(DB_PATH)) fs.writeFileSync(DB_PATH, JSON.stringify(seed, null, 2)); }
export function readDb(){ ensure(); return JSON.parse(fs.readFileSync(DB_PATH,'utf8')); }
export function writeDb(db){ ensure(); fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2)); }
