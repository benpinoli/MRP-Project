"""Editable native PowerPoint plus offline HTML and preview; standard library/Pillow only.
See BYU_ORC_AGENTS.md. All numbers summarize existing aggregate results.
"""
from pathlib import Path
import html,json,textwrap,zipfile
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'FOR_BEN';W,H=1280,720
FONT=Path('/usr/share/fonts/dejavu-sans-fonts')
NAVY='122039';TEAL='087F77';MINT='80DED0';WHITE='FFFFFF';INK='18263C';GRAY='526179';LIGHT='EEF3F7';RED='AF3943'
slides=[]
def font(pt,bold=False):return ImageFont.truetype(str(FONT/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),round(pt*96/72))
def shape(s,x,y,w,h,fill):s['shapes'].append({'type':'rect','x':x,'y':y,'w':w,'h':h,'fill':fill})
def text(s,x,y,w,h,content,pt=20,color=INK,bold=False):
    lines=[];f=font(pt,bold)
    for paragraph in content.split('\n'):
        words=paragraph.split();line=''
        for word in words:
            trial=(line+' '+word).strip()
            if line and f.getlength(trial)>w*96:lines.append(line);line=word
            else:line=trial
        lines.append(line)
    line_px=pt*96/72*1.18
    assert len(lines)*line_px<=h*96+2,('Text does not fit',content,len(lines),h)
    s['shapes'].append({'type':'text','x':x,'y':y,'w':w,'h':h,'lines':lines,'pt':pt,'color':color,'bold':bold,'line_px':line_px})
def new(title,source='PAPER.md · November 12, 2026',dark=False):
    s={'title':title,'bg':NAVY if dark else WHITE,'shapes':[],'source':source};slides.append(s)
    text(s,.65,.29,12,.28,'FOR BEN  /  RELATED-SECURITY DISCOUNT RESEARCH',11,MINT if dark else TEAL,True)
    if not dark:text(s,.65,.84,12,.7,title,29,INK,True);shape(s,.65,1.66,12,.025,TEAL)
    text(s,.65,7.05,11.7,.22,source,9,'B8C7D9' if dark else GRAY)
    text(s,12.4,7.03,.35,.28,str(len(slides)),11,MINT if dark else GRAY)
    return s
def card(s,x,y,w,value,label,dark=False,color=TEAL):
    shape(s,x,y,w,1.45,'20334E' if dark else LIGHT)
    text(s,x+.22,y+.16,w-.44,.62,value,31,MINT if dark else color,True)
    text(s,x+.22,y+.86,w-.44,.46,label,14,WHITE if dark else GRAY)
def row(s,y,cells,widths,head=False,height=.71):
    x=.65
    for value,width in zip(cells,widths):
        shape(s,x,y,width-.035,height-.035,NAVY if head else LIGHT)
        text(s,x+.14,y+.13,width-.30,height-.16,value,15 if head else 17,WHITE if head else INK,head);x+=width

s=new('Novo: what the evidence establishes',dark=True)
text(s,.65,1.2,11.8,1.4,'Novo has historical predictive content.',35,WHITE,True)
text(s,.65,2.55,11.7,1.1,'Future predictive skill and executable profits have not been established.',25,MINT)
card(s,.65,4.25,3.88,'44','hypothesis-tree nodes',True)
card(s,4.75,4.25,3.88,'21','evidence sections in the paper',True)
card(s,8.85,4.25,3.80,'11','long-horizon comparisons',True)

s=new('What we have accomplished','PAPER.md T01–T21 · TIMELINE.md')
items=[('Samsung forecasting','Locked forecast and fixed follow-ups; no reliable primary-horizon gain.'),('Broader comparisons','US classes, receipts, A/H and holding-company exposures; heterogeneous results.'),('Long-horizon tests','Two-/five-year models, fixed ridge and rolling history; stronger benchmarks added.'),('Mechanism and source checks','Payout delivery, supply controls, split units, clocks and candidate FX decoder.')]
for i,(a,b) in enumerate(items):
    y=1.95+i*1.1;shape(s,.65,y,.075,.86,TEAL);text(s,.9,y,3.3,.76,a,20,INK,True);text(s,4.3,y,8.25,.85,b,19,GRAY)

s=new('Novo: the benchmark changes the conclusion','Productive-batch scorecard · Novo rolling120 level OLS · Pragmatic coverage')
text(s,.65,1.93,12,.52,'Historical MSE reduction versus each benchmark',21,INK,True)
row(s,2.65,['Benchmark','2 years','5 years'],[6.8,2.6,2.6],True)
row(s,3.42,['No change (persistence)','+39.55%','+13.59%'],[6.8,2.6,2.6])
row(s,4.19,['Mean of past discount changes','+43.55%','+20.90%'],[6.8,2.6,2.6])
row(s,4.96,['Matching mean terminal discount','−1.57%','−6.47%'],[6.8,2.6,2.6])
text(s,.65,6.02,12,.68,'Positive = lower forecast error. These are discount-change loss reductions, not investment returns. The terminal mean uses the same matured training rows.',14,GRAY)

s=new('One narrow increment beyond the simple anchor','PAPER.md T20 · LOOP_TREE_PRODUCTIVE_BATCH_RESULTS_20261112.md')
text(s,.65,1.96,12,.7,'Five-year expanding activity OLS',25,INK,True)
card(s,.65,2.86,5.86,'6.81%','MSE reduction vs anchor · pragmatic · 88 origins')
card(s,6.77,2.86,5.86,'5.11%','MSE reduction vs anchor · strict · 74 origins')
text(s,.65,4.64,12,.9,'It also beats simpler regressions on matched origins. The advantage does not survive rolling training or ridge.',22,INK)
text(s,.65,5.93,12,.74,'Origins overlap; nonoverlap phases contain only 1–2 outcomes. Relative activity is a volume proxy, not measured liquidity. No future forecast has been validated.',15,GRAY)

s=new('What did not clear its predictive comparison','WHAT_DID_NOT_WORK.md / .csv · 543 dependent specification cases')
widths=[3.5,4.6,3.9]
row(s,2.02,['Discount situation','Variables tried','Main limitation'],widths,True,height=.64)
for i,cells in enumerate([
 ['Samsung common/preferred','Gap history, volatility; external states; activity/range; calendar','No reliable primary forecast gain'],
 ['US-listed class/receipt pairs','Lagged relative-price gap','Five of seven lose to persistence'],
 ['A/H and local/receipt gaps','Current gap; 12-month change; activity','Results depend on pair and benchmark'],
 ['Novo level/state models','Current gap, with/without trailing change','Lose to matching terminal anchors']]):
    row(s,2.74+i*.84,cells,widths,height=.79)
text(s,.65,6.26,12,.42,'The long table names each failed benchmark and retains partial wins. Blocked tests and weak explanatory fits are listed separately.',13,GRAY)

s=new('Mechanisms and measurement: useful progress','PAPER.md T16–T21 · Bounded-study and productive-batch reports')
card(s,.65,2.02,3.88,'15 years','Samsung reported cash / supply panel')
card(s,4.75,2.02,3.88,'6,091','candidate FX rows reproduced')
card(s,8.85,2.02,3.80,'0 / 60','qualified synchronized slots')
text(s,.65,3.93,12,.92,'Annual payout/supply regressions: 14 changes, weak fit and broad uncertainty. Constant class cash difference cannot identify its separate effect.',21,INK)
text(s,.65,5.08,12,1.0,'December 2007 Novo: the source-motivated two-unit candidate moves the raw daily ratio from about 2 to about 1. Legal conversion and synchronized clocks remain unresolved.',20,INK)
text(s,.65,6.35,12,.3,'This does not establish an error in the original forecasting panel or an executable opportunity.',12,GRAY)

s=new('The answer for Ben—and the next evidence','READ_ME_FIRST.md · PAPER.md · HYPOTHESIS_TREE.md')
row(s,2.00,['Claim','Current answer'],[7.7,4.3],True)
for i,cells in enumerate([
 ['Historical prediction of the measured gap','Yes, versus some benchmarks'],
 ['Extra information beyond a terminal anchor','Limited, model-specific evidence'],
 ['Validated prediction on new future origins','Not established'],
 ['Executable arbitrage profit','Not established']]):row(s,2.79+i*.72,cells,[7.7,4.3],height=.67)
text(s,.65,5.98,12,.78,'Next: qualify the source/basis/clocks, issue frozen forecasts using actually delivered future data, and retain both gains and losses against strong benchmarks.',17,TEAL,True)

# Serialize native editable Open XML shapes.
EMU=914400
ns='xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
def esc(x):return html.escape(str(x),quote=True)
def group():return '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
def xmlshape(o,i):
    x,y,w,h=[round(o[k]*EMU) for k in ['x','y','w','h']]
    nv=f'<p:nvSpPr><p:cNvPr id="{i}" name="{o["type"]} {i}"/><p:cNvSpPr'+(' txBox="1"' if o['type']=='text' else '')+'/>'+ '<p:nvPr/></p:nvSpPr>'
    sp=f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    sp+=f'<a:solidFill><a:srgbClr val="{o["fill"]}"/></a:solidFill>' if o['type']=='rect' else '<a:noFill/>'
    sp+='<a:ln><a:noFill/></a:ln></p:spPr>'
    body=''
    if o['type']=='text':
        para=[]
        for line in o['lines']:
            para.append(f'<a:p><a:pPr><a:lnSpc><a:spcPct val="118000"/></a:lnSpc><a:spcAft><a:spcPts val="0"/></a:spcAft></a:pPr><a:r><a:rPr lang="en-US" sz="{round(o["pt"]*100)}" b="{int(o["bold"])}"><a:solidFill><a:srgbClr val="{o["color"]}"/></a:solidFill><a:latin typeface="DejaVu Sans"/></a:rPr><a:t>{esc(line)}</a:t></a:r><a:endParaRPr lang="en-US"/></a:p>')
        body='<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/><a:lstStyle/>'+''.join(para)+'</p:txBody>'
    return '<p:sp>'+nv+sp+body+'</p:sp>'
def rels(items):return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{kind}" Target="{target}"/>' for id,kind,target in items)+'</Relationships>'
def doc(x):return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+x
files={}
files['_rels/.rels']=rels([('rId1','officeDocument','ppt/presentation.xml')])
files['ppt/presentation.xml']=doc(f'<p:presentation {ns}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>'+''.join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1,len(slides)+1))+'</p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')
files['ppt/_rels/presentation.xml.rels']=rels([('rId1','slideMaster','slideMasters/slideMaster1.xml')]+[(f'rId{i+1}','slide',f'slides/slide{i}.xml') for i in range(1,len(slides)+1)])
clr='<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>'
files['ppt/slideMasters/slideMaster1.xml']=doc(f'<p:sldMaster {ns}><p:cSld><p:spTree>{group()}</p:spTree></p:cSld>{clr}<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
files['ppt/slideMasters/_rels/slideMaster1.xml.rels']=rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml'),('rId2','theme','../theme/theme1.xml')])
files['ppt/slideLayouts/slideLayout1.xml']=doc(f'<p:sldLayout {ns} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>{group()}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
files['ppt/slideLayouts/_rels/slideLayout1.xml.rels']=rels([('rId1','slideMaster','../slideMasters/slideMaster1.xml')])
colors={'dk1':INK,'lt1':WHITE,'dk2':NAVY,'lt2':LIGHT,'accent1':TEAL,'accent2':MINT,'accent3':RED,'accent4':GRAY,'accent5':'4075A4','accent6':'D5A848','hlink':TEAL,'folHlink':'6F5197'}
scheme=''.join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k,v in colors.items())
fill='<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
files['ppt/theme/theme1.xml']=doc(f'<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Ben research"><a:themeElements><a:clrScheme name="Research">{scheme}</a:clrScheme><a:fontScheme name="Research"><a:majorFont><a:latin typeface="DejaVu Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="DejaVu Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Research"><a:fillStyleLst>{fill*3}</a:fillStyleLst><a:lnStyleLst>'+''.join(f'<a:ln w="{w}">{fill}<a:prstDash val="solid"/></a:ln>' for w in [6350,12700,19050])+'</a:lnStyleLst><a:effectStyleLst>'+('<a:effectStyle><a:effectLst/></a:effectStyle>'*3)+f'</a:effectStyleLst><a:bgFillStyleLst>{fill*3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>')
for i,s in enumerate(slides,1):
    files[f'ppt/slides/slide{i}.xml']=doc(f'<p:sld {ns}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{s["bg"]}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree>{group()}'+''.join(xmlshape(o,j) for j,o in enumerate(s['shapes'],2))+'</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
    files[f'ppt/slides/_rels/slide{i}.xml.rels']=rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml')])
types={'ppt/presentation.xml':'presentationml.presentation.main','ppt/slideMasters/slideMaster1.xml':'presentationml.slideMaster','ppt/slideLayouts/slideLayout1.xml':'presentationml.slideLayout','ppt/theme/theme1.xml':'drawingml.theme'}
types.update({f'ppt/slides/slide{i}.xml':'presentationml.slide' for i in range(1,len(slides)+1)})
files['[Content_Types].xml']=doc('<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'+''.join(f'<Override PartName="/{k}" ContentType="application/vnd.openxmlformats-officedocument.{v}+xml"/>' for k,v in types.items())+'</Types>')
with zipfile.ZipFile(OUT/'ACCOMPLISHMENTS.pptx','w',zipfile.ZIP_DEFLATED) as z:
    for name,value in files.items():z.writestr(name,value)

# Same scene model gives a browser deck and visual preview, without network assets.
sections=[];thumbs=[];transcript=['# Research accomplishments — seven-slide presentation','']
for i,s in enumerate(slides,1):
    im=Image.new('RGB',(W,H),'#'+s['bg']);draw=ImageDraw.Draw(im);elements=[]
    transcript+=['## '+str(i)+'. '+s['title'],'']
    for o in s['shapes']:
        x,y,w,h=[o[k]*96 for k in ['x','y','w','h']]
        if o['type']=='rect':draw.rectangle((x,y,x+w,y+h),fill='#'+o['fill']);elements.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#{o["fill"]}"></div>')
        else:
            f=font(o['pt'],o['bold'])
            for line_no,line in enumerate(o['lines']):draw.text((x,y+line_no*o['line_px']),line,font=f,fill='#'+o['color'])
            txt='<br>'.join(esc(line) for line in o['lines']);elements.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;color:#{o["color"]};font-size:{o["pt"]*96/72}px;line-height:1.18;font-weight:{700 if o["bold"] else 400}">{txt}</div>')
            transcript.append(' '.join(o['lines']))
    im.thumbnail((640,360));thumbs.append(im)
    sections.append(f'<section class="slide {"active" if i==1 else ""}" aria-label="Slide {i}: {esc(s["title"])}" style="background:#{s["bg"]}">'+''.join(elements)+'</section>')
    transcript.append('')
sheet=Image.new('RGB',(1280,1440),'#DDE4EB')
for i,im in enumerate(thumbs):sheet.paste(im,((i%2)*640,(i//2)*360))
sheet.save(OUT/'PRESENTATION_PREVIEW.png')
(OUT/'PRESENTATION.md').write_text('\n'.join(transcript))
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FOR BEN — Research accomplishments</title><style>*{box-sizing:border-box}body{margin:0;background:#0A1426;font-family:"DejaVu Sans",Arial,sans-serif;overflow:hidden}.stage{width:1280px;height:720px;position:absolute;left:50%;top:50%;transform-origin:center center}.slide{position:absolute;inset:0;display:none}.slide.active{display:block}button{position:fixed;bottom:8px;border:0;background:#233C5A;color:white;padding:8px 14px;cursor:pointer;font-size:14px;z-index:4}#back{left:8px}#next{right:8px}#hint{position:fixed;top:5px;right:12px;color:#8CA8BF;font-size:11px;z-index:5}@media print{@page{size:landscape;margin:0}body{overflow:visible;background:white}.stage{position:static;transform:none!important;width:1280px;height:auto}.slide{display:block!important;position:relative;width:1280px;height:720px;break-after:page}button,#hint{display:none}}</style><body><div id="hint">← / → / Space · Home / End · P to print</div><main class="stage">'''+''.join(sections)+'''</main><button id="back" aria-label="Previous slide">←</button><button id="next" aria-label="Next slide">→</button><script>let index=0;const slides=[...document.querySelectorAll('.slide')];function show(i){index=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,n)=>s.classList.toggle('active',n===index));document.title=`${index+1}/${slides.length} · FOR BEN`}function resize(){document.querySelector('.stage').style.transform=`translate(-50%,-50%) scale(${Math.min(innerWidth/1280,innerHeight/720)})`}document.getElementById('back').onclick=()=>show(index-1);document.getElementById('next').onclick=()=>show(index+1);addEventListener('keydown',e=>{if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();show(index+1)}else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(index-1)}else if(e.key==='Home')show(0);else if(e.key==='End')show(slides.length-1);else if(e.key.toLowerCase()==='p')print()});addEventListener('resize',resize);resize();show(0)</script></body></html>'''
(OUT/'ACCOMPLISHMENTS.html').write_text(page.replace('@page{size:landscape;margin:0}', '@page{size:13.333333in 7.5in;margin:0}'))
print(json.dumps({'slides':len(slides),'PowerPoint':'FOR_BEN/ACCOMPLISHMENTS.pptx','offline_browser_deck':'FOR_BEN/ACCOMPLISHMENTS.html','preview':'FOR_BEN/PRESENTATION_PREVIEW.png'},indent=2))
