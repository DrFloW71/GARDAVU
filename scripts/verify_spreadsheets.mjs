import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const runtimeRequire = createRequire('C:/Users/flori/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const { FileBlob, SpreadsheetFile } = await import(pathToFileURL(runtimeRequire.resolve('@oai/artifact-tool')).href);

const input = process.argv[2];
const output = process.argv[3];
await fs.mkdir(output, {recursive:true});
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
console.log((await workbook.inspect({kind:'sheet',include:'id,name',maxChars:2000})).ndjson);
const names = ['Planning', 'Équité', 'Jours fériés', 'Paramètres et avertissements'];
for (let index=0; index<names.length; index++) {
  const sheet = workbook.worksheets.getItem(names[index]);
  const range = sheet.name === 'Planning' ? 'A1:G12' : sheet.name === 'Équité' ? 'A1:G12' : sheet.name === 'Paramètres et avertissements' ? 'A1:B12' : 'A1:F12';
  const image = await workbook.render({sheetName:sheet.name,range,scale:1,format:'png'});
  await fs.writeFile(path.join(output,`${index+1}.png`),new Uint8Array(await image.arrayBuffer()));
}
