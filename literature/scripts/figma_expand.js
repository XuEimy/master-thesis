// Prefix this script with `const batch = <current-project boards>;`.
const page = await figma.getNodeByIdAsync('101:2');
await figma.setCurrentPageAsync(page);
await Promise.all([
  figma.loadFontAsync({family:'Noto Sans SC',style:'Regular'}),
  figma.loadFontAsync({family:'Noto Sans SC',style:'Bold'})
]);
const createdNodeIds = [];
const result = [];
const columnX = [8500,10820,13140,15460];
function addText(parent, name, value, size, bold, leading) {
  const t = figma.createText();
  parent.appendChild(t);
  createdNodeIds.push(t.id);
  t.name = name;
  t.fontName = {family:'Noto Sans SC',style:bold?'Bold':'Regular'};
  t.fontSize = size;
  t.lineHeight = {unit:'PIXELS',value:leading};
  t.fills = [{type:'SOLID',color:{r:0.08,g:0.08,b:0.08}}];
  t.characters = value;
  t.resize(1952,1);
  t.textAutoResize = 'HEIGHT';
  return t;
}
for (const b of batch) {
  const name = '展开稿｜'+b.key+'｜'+b.title;
  const existing = page.children.find(n=>n.name===name);
  if (existing) { result.push({key:b.key,id:existing.id,skipped:true}); continue; }
  const x = b.column<0 ? 8500 : columnX[b.column];
  const peers = page.children.filter(n=>n.name.startsWith('展开稿｜') && n.x===x && n.y>=0);
  const y = b.column<0 ? -2600 : Math.max(0,...peers.map(n=>n.y+n.height+160));
  const f = figma.createAutoLayout('VERTICAL');
  page.appendChild(f);
  createdNodeIds.push(f.id);
  f.name = name;
  f.x = x;
  f.y = y;
  f.resize(2080,10);
  f.primaryAxisSizingMode = 'AUTO';
  f.counterAxisSizingMode = 'FIXED';
  f.paddingTop = 64; f.paddingBottom = 64; f.paddingLeft = 64; f.paddingRight = 64;
  f.itemSpacing = 26;
  f.fills = [{type:'SOLID',color:{r:1,g:1,b:1}}];
  addText(f,'标题',b.title,52,true,72);
  addText(f,'内容性质',b.status,26,false,40);
  for (let i=0;i<b.blocks.length;i++) {
    const block=b.blocks[i];
    const heading=block.kind==='heading';
    const source=block.kind==='source';
    addText(f,String(i+1).padStart(3,'0')+'｜'+block.kind,block.text,heading?38:(source?24:30),heading,heading?56:(source?38:48));
  }
  addText(f,'本轮来源', '本轮源稿：'+b.source,24,false,38);
  result.push({key:b.key,id:f.id,name:f.name,x:f.x,y:f.y,width:f.width,height:f.height,textCount:f.children.length,bodyBlockCount:b.blocks.length});
}
return {createdNodeIds,boards:result};
