let ts;try{ts=require('typescript')}catch{ts=require(process.env.TYPESCRIPT_PATH||'/home/nmaldaner/projetos/portal/node_modules/typescript')}
const fs=require('fs');
let out={};
for(const file of ['assets/learn.js','assets/site.js']){
 const src=fs.readFileSync(file,'utf8'),ast=ts.createSourceFile(file,src,ts.ScriptTarget.Latest,true,ts.ScriptKind.JS),strings=[];
 function walk(node){if(ts.isStringLiteral(node)||ts.isNoSubstitutionTemplateLiteral(node)){strings.push({value:node.text,start:Array.from(src.slice(0,node.getStart(ast))).length,end:Array.from(src.slice(0,node.end)).length})}ts.forEachChild(node,walk)}walk(ast);out[file]=strings;
}
fs.writeFileSync('i18n/js-strings.json',JSON.stringify(out,null,2));
const re=/[áéíóúãõâêôç]|\b(?:Curso|Trilha|Modulo|Topico|Lido|Marcar|lido|duvida|Duvidas|Continuar|Voltar|Correto|Reveja|Nenhuma|Fechar|Exportar|Importar|Progresso|Notas|Salvar|Cancelar|Excluir|Cor|Texto|Copiado|Selecione|Nenhum|Curso|Abrir|Link|Apagar|Restaurar|Fonte|Aparencia|Leitura|Sem|sim|nao|Nota|Grifar|Grifo|Resolvida|Reabrir|Tudo|Arquivo|Importacao|Erro|Local|Escuro|Claro|Sistema|Largura|Entrelinha|Tamanho|Conforto)\b/;
console.log(JSON.stringify(Object.fromEntries(Object.entries(out).map(([f,vs])=>[f,vs.filter(v=>re.test(v.value)).map(v=>v.value)])),null,2));
