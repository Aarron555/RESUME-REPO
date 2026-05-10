import { readDb, writeDb } from './fileStore.js';
export const scanRepository = {
  create(scan) { const db=readDb(); db.scans.push(scan); writeDb(db); return scan; },
  update(id, patch) { const db=readDb(); const idx=db.scans.findIndex((s)=>s.id===id); if(idx<0) return null; db.scans[idx]={...db.scans[idx],...patch,updated_at:new Date().toISOString()}; writeDb(db); return db.scans[idx]; },
  getById(id) { return readDb().scans.find((s)=>s.id===id)||null; },
  getAll() { return readDb().scans; }
};
