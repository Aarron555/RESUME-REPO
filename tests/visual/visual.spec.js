import { test, expect } from '@playwright/test';

const desktop=['/','/scan','/pricing','/first-fix','/faq','/admin','/admin/prospects','/admin/scans','/admin/pipeline','/admin/tasks','/admin/settings','/admin/design-review'];
const mobile=['/','/scan','/scan/result/demo','/pricing','/admin','/admin/tasks'];

for(const path of desktop){
  test(`desktop ${path}`,async({page})=>{
    await page.setViewportSize({width:1440,height:1024});
    await page.goto(`http://localhost:3000${path}`);
    await expect(page).toHaveScreenshot(`${path.replaceAll('/','_')||'home'}-desktop.png`,{fullPage:true,maxDiffPixelRatio:0.03});
  });
}
for(const path of mobile){
  test(`mobile ${path}`,async({page})=>{
    await page.setViewportSize({width:390,height:844});
    await page.goto(`http://localhost:3000${path}`);
    await expect(page).toHaveScreenshot(`${path.replaceAll('/','_')||'home'}-mobile.png`,{fullPage:true,maxDiffPixelRatio:0.03});
  });
}
