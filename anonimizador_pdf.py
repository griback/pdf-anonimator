import os,re,sys,json,traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
try: import fitz
except Exception: fitz=None
APP_NAME='Anonimizador Local de PDF v3'
PATTERNS={'CPF':re.compile(r'(?<!\d)\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}(?!\d)'), 'E-mail':re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I), 'Telefone':re.compile(r'(?<!\d)(?:\+?55[\s.-]?)?(?:\(?\d{2}\)?[\s.-]?)?(?:9\d{4}|\d{4})[-\s.]?\d{4}(?!\d)')}
def require():
    if fitz is None: raise RuntimeError('PyMuPDF não está instalado.')
def variants(t):
    out={t.strip()}; d=re.sub(r'\D','',t)
    if len(d)==11: out|={d,f'{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}'}
    return [x for x in out if x]
def inspect_pdf(path,terms,enabled):
    require(); doc=fitz.open(path); pages=[]; totals={t:0 for t in terms}; pats={k:0 for k,v in enabled.items() if v}
    for i,p in enumerate(doc):
        text=p.get_text('text') or ''; hits=0
        for t in terms:
            seen=set()
            for v in variants(t):
                for r in p.search_for(v): seen.add(tuple(round(x,2) for x in r))
            totals[t]+=len(seen); hits+=len(seen)
        for name,rx in PATTERNS.items():
            if enabled.get(name):
                n=len(rx.findall(text)); pats[name]+=n; hits+=n
        pages.append({'page':i+1,'chars':len(text.strip()),'images':len(p.get_images(full=True)),'hits':hits})
    meta=dict(doc.metadata or {}); doc.close(); return pages,totals,pats,meta
def redact(src,dst,terms,enabled,manual):
    require(); doc=fitz.open(src); rep={'source':src,'output':dst,'terms':{t:0 for t in terms},'patterns':{k:0 for k,v in enabled.items() if v},'manual_redactions':0,'warnings':[],'pages':[]}
    for i,p in enumerate(doc):
        text=p.get_text('text') or ''; auto=0
        for t in terms:
            seen=set()
            for v in variants(t):
                for r in p.search_for(v):
                    key=tuple(round(x,2) for x in r)
                    if key not in seen: seen.add(key); p.add_redact_annot(r,fill=(0,0,0)); rep['terms'][t]+=1; auto+=1
        for name,rx in PATTERNS.items():
            if enabled.get(name):
                for m in rx.finditer(text):
                    for r in p.search_for(m.group(0)):
                        p.add_redact_annot(r,fill=(0,0,0)); rep['patterns'][name]+=1; auto+=1
        man=0
        for c in manual.get(i,[]):
            r=fitz.Rect(*c)&p.rect
            if not r.is_empty and r.width>1 and r.height>1: p.add_redact_annot(r,fill=(0,0,0)); man+=1; rep['manual_redactions']+=1
        if auto or man: p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_PIXELS)
        if len(text.strip())<20 and not man: rep['warnings'].append(f'Página {i+1}: pouco/nenhum texto pesquisável; revise visualmente.')
        rep['pages'].append({'page':i+1,'automatic_hits':auto,'manual_areas':man})
    try: doc.set_metadata({})
    except: pass
    try: doc.del_xml_metadata()
    except: pass
    doc.save(dst,garbage=4,clean=True,deflate=True); doc.close()
    vd=fitz.open(dst); alltext='\n'.join(p.get_text('text') or '' for p in vd); vd.close(); residual=[]
    low=alltext.casefold()
    for t in terms:
        if any(v.casefold() in low for v in variants(t)): residual.append(f'Termo ainda extraível: {t}')
    for n,rx in PATTERNS.items():
        if enabled.get(n) and rx.search(alltext): residual.append(f'Padrão {n} ainda possui ocorrência extraível.')
    rep['verification']={'status':'OK' if not residual else 'ATENÇÃO','residual_warnings':residual}
    rp=str(Path(dst).with_suffix(''))+'_relatorio.json'; Path(rp).write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf-8'); return rep,rp
class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title(APP_NAME); self.geometry('1220x820'); self.minsize(1000,700); self.pdf=tk.StringVar(); self.cpf=tk.BooleanVar(); self.email=tk.BooleanVar(); self.phone=tk.BooleanVar(); self.doc=None; self.pi=0; self.zoom=1.25; self.img=None; self.manual={}; self.start=None; self.tmp=None; self.build()
    def build(self):
        top=ttk.Frame(self,padding=10); top.pack(fill='x'); ttk.Label(top,text=APP_NAME,font=('Segoe UI',17,'bold')).pack(anchor='w'); ttk.Label(top,text='Redação permanente de texto e áreas visuais — processamento local.').pack(anchor='w')
        row=ttk.Frame(top); row.pack(fill='x',pady=7); ttk.Entry(row,textvariable=self.pdf).pack(side='left',fill='x',expand=True); ttk.Button(row,text='1. Selecionar PDF',command=self.choose).pack(side='left',padx=4); self.an_btn=ttk.Button(row,text='2. Analisar PDF',command=self.analyze); self.an_btn.pack(side='left')
        body=ttk.Panedwindow(self,orient='horizontal'); body.pack(fill='both',expand=True,padx=10); L=ttk.Frame(body,padding=5); R=ttk.Frame(body,padding=5); body.add(L,weight=2); body.add(R,weight=5)
        ttk.Label(L,text='Termos específicos (um por linha)',font=('Segoe UI',10,'bold')).pack(anchor='w'); self.terms=tk.Text(L,height=8); self.terms.pack(fill='x',pady=4)
        box=ttk.LabelFrame(L,text='Detecção automática',padding=7); box.pack(fill='x'); ttk.Checkbutton(box,text='CPF',variable=self.cpf).pack(anchor='w'); ttk.Checkbutton(box,text='E-mail',variable=self.email).pack(anchor='w'); ttk.Checkbutton(box,text='Telefone',variable=self.phone).pack(anchor='w')
        ttk.Label(L,text='Status / análise',font=('Segoe UI',10,'bold')).pack(anchor='w',pady=(8,2)); self.log=tk.Text(L,height=18,state='disabled',wrap='word'); self.log.pack(fill='both',expand=True)
        self.gen=ttk.Button(L,text='4. GERAR PDF ANONIMIZADO',command=self.process,state='disabled'); self.gen.pack(fill='x',pady=(8,3),ipady=6); self.ver=ttk.Button(L,text='5. Verificar último resultado',command=self.verify_last,state='disabled'); self.ver.pack(fill='x')
        nav=ttk.Frame(R); nav.pack(fill='x'); ttk.Button(nav,text='◀',command=lambda:self.page(-1)).pack(side='left'); self.pl=ttk.Label(nav,text='Página - / -'); self.pl.pack(side='left',padx=8); ttk.Button(nav,text='▶',command=lambda:self.page(1)).pack(side='left'); ttk.Button(nav,text='− Zoom',command=lambda:self.z(-.2)).pack(side='left',padx=(20,3)); ttk.Button(nav,text='+ Zoom',command=lambda:self.z(.2)).pack(side='left'); ttk.Button(nav,text='Desfazer área',command=self.undo).pack(side='right'); ttk.Button(nav,text='Limpar página',command=self.clear).pack(side='right',padx=4)
        ttk.Label(R,text='3. Revisão visual: arraste o mouse sobre qualquer área que também deva ser eliminada.',font=('Segoe UI',10,'bold')).pack(anchor='w',pady=5)
        cf=ttk.Frame(R); cf.pack(fill='both',expand=True); self.cv=tk.Canvas(cf,bg='#555',cursor='crosshair'); vs=ttk.Scrollbar(cf,orient='vertical',command=self.cv.yview); hs=ttk.Scrollbar(cf,orient='horizontal',command=self.cv.xview); self.cv.configure(yscrollcommand=vs.set,xscrollcommand=hs.set); self.cv.grid(row=0,column=0,sticky='nsew'); vs.grid(row=0,column=1,sticky='ns'); hs.grid(row=1,column=0,sticky='ew'); cf.rowconfigure(0,weight=1); cf.columnconfigure(0,weight=1); self.cv.bind('<ButtonPress-1>',self.down); self.cv.bind('<B1-Motion>',self.move); self.cv.bind('<ButtonRelease-1>',self.up); self.last=None
    def logit(self,s,clear=False):
        self.log.config(state='normal');
        if clear:self.log.delete('1.0','end')
        self.log.insert('end',s+'\n'); self.log.see('end'); self.log.config(state='disabled'); self.update_idletasks()
    def choose(self):
        p=filedialog.askopenfilename(filetypes=[('PDF','*.pdf')]);
        if not p:return
        try:
            if self.doc:self.doc.close()
            self.doc=fitz.open(p); self.pdf.set(p); self.pi=0; self.manual={}; self.render(); self.gen.config(state='disabled'); self.logit('PDF carregado. Clique em “2. Analisar PDF”.',True)
        except Exception as e:self.err(e)
    def opts(self): return [x.strip() for x in self.terms.get('1.0','end').splitlines() if x.strip()],{'CPF':self.cpf.get(),'E-mail':self.email.get(),'Telefone':self.phone.get()}
    def analyze(self):
        p=self.pdf.get().strip()
        if not p or not os.path.isfile(p): messagebox.showwarning(APP_NAME,'Primeiro selecione um PDF válido.'); return
        try:
            self.logit('Analisando PDF...',True); terms,en=self.opts(); pages,tot,pats,meta=inspect_pdf(p,terms,en); self.logit(f'Páginas: {len(pages)}'); self.logit(f'Páginas com pouco/nenhum texto: {[x["page"] for x in pages if x["chars"]<20] or "nenhuma"}')
            if terms:
                for k,v in tot.items(): self.logit(f'Termo “{k}”: {v} ocorrência(s) encontrada(s)')
            else:self.logit('Nenhum termo específico informado.')
            for k,v in pats.items():self.logit(f'{k}: {v} possível(is) ocorrência(s)')
            self.logit(f'Metadados presentes: {"sim" if any(meta.values()) else "não/aparentemente vazios"}'); self.logit('Análise concluída. Revise visualmente e use “4. GERAR PDF ANONIMIZADO”.'); self.gen.config(state='normal')
        except Exception as e:self.err(e)
    def render(self):
        if not self.doc:return
        p=self.doc[self.pi]; pix=p.get_pixmap(matrix=fitz.Matrix(self.zoom,self.zoom),alpha=False); self.img=tk.PhotoImage(data=pix.tobytes('ppm')); self.cv.delete('all'); self.cv.create_image(0,0,anchor='nw',image=self.img); self.cv.config(scrollregion=(0,0,pix.width,pix.height)); self.pl.config(text=f'Página {self.pi+1} / {len(self.doc)}')
        for c in self.manual.get(self.pi,[]):
            r=fitz.Rect(*c); self.cv.create_rectangle(r.x0*self.zoom,r.y0*self.zoom,r.x1*self.zoom,r.y1*self.zoom,outline='red',width=3,fill='red',stipple='gray50')
    def page(self,d):
        if self.doc:self.pi=max(0,min(len(self.doc)-1,self.pi+d));self.render()
    def z(self,d):self.zoom=max(.5,min(3,self.zoom+d));self.render()
    def down(self,e):
        if not self.doc:return
        self.start=(self.cv.canvasx(e.x),self.cv.canvasy(e.y)); self.tmp=self.cv.create_rectangle(*self.start,*self.start,outline='red',width=2)
    def move(self,e):
        if self.start and self.tmp:self.cv.coords(self.tmp,*self.start,self.cv.canvasx(e.x),self.cv.canvasy(e.y))
    def up(self,e):
        if not self.start:return
        x0,y0=self.start;x1,y1=self.cv.canvasx(e.x),self.cv.canvasy(e.y);self.start=None
        if self.tmp:self.cv.delete(self.tmp);self.tmp=None
        c=(min(x0,x1)/self.zoom,min(y0,y1)/self.zoom,max(x0,x1)/self.zoom,max(y0,y1)/self.zoom)
        if c[2]-c[0]>3 and c[3]-c[1]>3:self.manual.setdefault(self.pi,[]).append(c);self.logit(f'Área manual adicionada na página {self.pi+1}.')
        self.render()
    def undo(self):
        a=self.manual.get(self.pi,[])
        if a:a.pop();self.render()
    def clear(self):self.manual[self.pi]=[];self.render()
    def process(self):
        src=self.pdf.get().strip(); terms,en=self.opts()
        if not terms and not any(en.values()) and not any(self.manual.values()):messagebox.showwarning(APP_NAME,'Não há nada selecionado para anonimizar.');return
        dst=filedialog.asksaveasfilename(defaultextension='.pdf',initialfile=Path(src).stem+'_ANONIMIZADO.pdf',initialdir=str(Path(src).parent),filetypes=[('PDF','*.pdf')])
        if not dst:return
        if os.path.abspath(dst)==os.path.abspath(src):messagebox.showerror(APP_NAME,'Não sobrescreva o PDF original.');return
        try:
            self.logit('Processando redações...'); rep,rp=redact(src,dst,terms,en,self.manual); self.last=(dst,terms,en); self.logit('=== PDF GERADO ===');
            for k,v in rep['terms'].items():self.logit(f'Termo “{k}”: {v} removida(s)')
            for k,v in rep['patterns'].items():self.logit(f'{k}: {v} removida(s)')
            self.logit(f'Áreas manuais: {rep["manual_redactions"]}'); self.logit(f'Verificação textual automática: {rep["verification"]["status"]}');
            for w in rep['warnings']+rep['verification']['residual_warnings']:self.logit('AVISO: '+w)
            self.logit('Saída: '+dst); self.logit('Relatório: '+rp); self.ver.config(state='normal'); messagebox.showinfo(APP_NAME,'PDF anonimizado criado.\n\nFaça também uma revisão visual final.')
        except Exception as e:self.err(e)
    def verify_last(self):
        if not self.last:return
        dst,terms,en=self.last
        try:
            pages,tot,pats,_=inspect_pdf(dst,terms,en); self.logit('=== NOVA VERIFICAÇÃO ==='); bad=False
            for k,v in tot.items():self.logit(f'Termo “{k}”: {v} restante(s)');bad|=v>0
            for k,v in pats.items():self.logit(f'{k}: {v} restante(s)');bad|=v>0
            self.logit('Resultado: '+('ATENÇÃO — ainda há conteúdo pesquisável correspondente.' if bad else 'OK — nenhum termo/padrão selecionado foi localizado na camada textual.'))
        except Exception as e:self.err(e)
    def err(self,e):self.logit('ERRO: '+str(e));traceback.print_exc();messagebox.showerror(APP_NAME,str(e))
if __name__=='__main__':
    if fitz is None:
        r=tk.Tk();r.withdraw();messagebox.showerror(APP_NAME,'PyMuPDF não encontrado. Execute instalar.bat ou instale requirements.txt.');sys.exit(1)
    App().mainloop()
