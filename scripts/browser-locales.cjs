const {chromium}=require(process.env.PLAYWRIGHT_PATH||'/home/nmaldaner/projetos/timesmkt3/node_modules/playwright');
const assert=require('assert'),fs=require('fs');
const base=process.env.BASE_URL||'http://127.0.0.1:33541';
const locales=(process.env.LOCALES||'en,es').split(',');
(async()=>{
 const browser=await chromium.launch({headless:true}),ctx=await browser.newContext({viewport:{width:1440,height:1000}}),page=await ctx.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));let ptExport;
 await page.goto(base+'/curso/trilha1/modulo-1-1.html');await page.locator('[data-inema-read-toggle]').first().click();ptExport=await page.evaluate(()=>INEMA.exportJSON());
 for(const lang of locales){
  await page.goto(base+'/'+lang+'/');assert.equal(await page.locator('html').getAttribute('lang'),lang);assert.equal(await page.evaluate(()=>INEMA.progress('curso').done),0);
  assert.equal(await page.locator('[data-os-languages] a').count(),3);
  await page.locator('[data-os-resume]').click();await page.waitForURL(new RegExp('/'+lang+'/curso/trilha1/modulo-1-1.html'));
  assert.equal(await page.evaluate(data=>INEMA.importJSON(data).ok,ptExport),false);
  await page.locator('[data-inema-read-toggle]').first().click();assert.equal(await page.locator('[data-inema-read-label]').first().innerText(),lang==='en'?'Read':'Leído');
  await page.locator('[data-inema-doubt-toggle]').first().click();
  assert.equal(await page.locator('[data-task]').first().isChecked(),false);await page.locator('[data-task]').first().check();
  await page.evaluate(()=>{const p=document.querySelector('[data-inema-block]'),r=document.createRange();r.setStart(p.firstChild,0);r.setEnd(p.firstChild,20);INEMA.highlight(r,{note:'locale verification',color:'yellow'})});
  await page.reload();assert.equal(await page.locator('[data-task]').first().isChecked(),true);assert.equal(await page.evaluate(()=>INEMA.progress('curso').done),1);assert(await page.locator('mark.inema-hl').count()>0);
  await page.goto(base+'/'+lang+'/');await page.locator('[data-inema-journey-open]').click();assert(await page.getByRole('heading',{name:lang==='en'?'My journey':'Mi recorrido'}).isVisible());
  await page.getByRole('button',{name:lang==='en'?'Return to last position':'Volver al último punto'}).click();await page.waitForURL(new RegExp('/'+lang+'/curso/trilha1/modulo-1-1.html'));
  const other=lang==='en'?'es':'en';assert((await page.locator('[data-os-languages] a[hreflang="'+other+'"]').getAttribute('href')).endsWith(other+'/curso/trilha1/modulo-1-1.html'));
  for(const route of ['index.html','curso/trilha4/modulo-4-2.html','materiais/index.html']){
   await page.goto(base+'/'+lang+'/'+route);await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),lang+' mobile overflow '+route);
  }
  await page.screenshot({path:'.verificacao/'+lang+'-mobile.png',fullPage:true});await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/'+lang+'/');await page.screenshot({path:'.verificacao/'+lang+'-desktop.png',fullPage:true});
 }
 const nojs=await browser.newContext({javaScriptEnabled:false});const np=await nojs.newPage();for(const lang of locales){await np.goto(base+'/'+lang+'/curso/trilha1/index.html');assert(await np.locator('.topic-explanation').first().isVisible())}
 assert.deepEqual(errors,[]);fs.writeFileSync('.verificacao/locales-results.json',JSON.stringify({ok:true,languages:locales,checks:['translated UI','separate storage','reject cross-language import','highlights persist','resume stays in locale','language links preserve lesson','mobile overflow','no JavaScript reading'],errors},null,2));await browser.close();console.log('OK: EN/ES learning state, UI, navigation, mobile and no-JS reading.');
})().catch(e=>{console.error(e);process.exit(1)});
