import { readDb, writeDb } from './fileStore.js';
export const auditLogRepository = {
  add(entry){ const db=readDb(); const row={id:`audit_${Date.now()}`,created_at:new Date().toISOString(),...entry}; db.auditLogs.push(row); writeDb(db); return row; },
  listByScan(scan_id){ return readDb().auditLogs.filter((x)=>x.scan_id===scan_id); }
};
