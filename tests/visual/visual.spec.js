import { test, expect } from '@playwright/test';
const desktop=['/','/scan','/pricing','/first-fix','/faq','/admin','/admin/scans','/admin/pipeline','/admin/design-review'];
for(const path of desktop){test(`desktop ${path}`,async({page})=>{await page.setViewportSize({width:1440,height:1024});await page.goto(`http://localhost:3000${path}`);await expect(page).toHaveScreenshot(`${path.replaceAll('/','_')||'home'}-desktop.png`,{fullPage:true,maxDiffPixelRatio:0.03});});}
