#!/usr/bin/env python3
"""Build simple, dependency-free DOCX checkpoints from repository Markdown."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    ROOT / "docs/regressions/LOOP_EXCEPTION_TEST_RESULTS_20261109.md":
        ROOT / "docs/regressions/LOOP_EXCEPTION_CHECKPOINT_20261109.docx",
    ROOT / "docs/regressions/STILL_REQUIRED_DATA_ACQUISITION_BRIEF_20261109.md":
        ROOT / "docs/regressions/STILL_REQUIRED_DATA_ACQUISITION_BRIEF_20261109.docx",
}


def plain(text: str) -> str:
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("**", "").replace("`", "").strip()


def run(text: str, bold: bool = False, code: bool = False) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if code:
        props.append('<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def paragraph(text: str = "", style: str | None = None, bullet: bool = False,
              code: bool = False) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if bullet:
        ppr.append('<w:ind w:left="360" w:hanging="240"/>')
    if code:
        ppr.append('<w:shd w:fill="F2F2F2"/><w:spacing w:after="40"/>')
    pprops = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    prefix = "• " if bullet else ""
    return f"<w:p>{pprops}{run(prefix + plain(text), code=code)}</w:p>"


def table(rows: list[list[str]]) -> str:
    width = max(len(row) for row in rows)
    grid = "".join('<w:gridCol w:w="2200"/>' for _ in range(width))
    body = []
    for rindex, row in enumerate(rows):
        cells = []
        for value in row + [""] * (width - len(row)):
            shade = '<w:shd w:fill="D9EAF7"/>' if rindex == 0 else ""
            tcpr = f'<w:tcPr><w:tcW w:w="2200" w:type="dxa"/>{shade}</w:tcPr>'
            cells.append(f"<w:tc>{tcpr}{paragraph(plain(value))}</w:tc>")
        body.append(f"<w:tr>{''.join(cells)}</w:tr>")
    borders = "".join(f'<w:{edge} w:val="single" w:sz="4" w:color="B7B7B7"/>'
                      for edge in ("top", "left", "bottom", "right", "insideH", "insideV"))
    props = f'<w:tblPr><w:tblBorders>{borders}</w:tblBorders><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    return f"<w:tbl>{props}<w:tblGrid>{grid}</w:tblGrid>{''.join(body)}</w:tbl>"


def markdown_body(source: str) -> str:
    lines = source.splitlines()
    parts: list[str] = []
    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            parts.append(paragraph(line, code=True))
            i += 1
            continue
        if line.startswith("| ") and i + 1 < len(lines) and re.match(r"^\|[ |:\-]+\|$", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                values = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if i == 0 or not all(re.fullmatch(r":?-+:?", cell.replace(" ", "")) for cell in values):
                    rows.append(values)
                i += 1
            if len(rows) >= 2 and all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in rows[1]):
                rows.pop(1)
            parts.append(table(rows))
            continue
        if line.startswith("### "):
            parts.append(paragraph(line[4:], "Heading3"))
        elif line.startswith("## "):
            parts.append(paragraph(line[3:], "Heading2"))
        elif line.startswith("# "):
            parts.append(paragraph(line[2:], "Title"))
        elif re.match(r"^\d+\. ", line):
            parts.append(paragraph(line, bullet=True))
        elif line.startswith("- "):
            parts.append(paragraph(line[2:], bullet=True))
        elif line.strip():
            parts.append(paragraph(line))
        else:
            parts.append(paragraph())
        i += 1
    return "".join(parts)


def build(source: Path, output: Path) -> None:
    body = markdown_body(source.read_text(encoding="utf-8"))
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>{body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" w:header="360" w:footer="360" w:gutter="0"/></w:sectPr></w:body></w:document>'''
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="20"/></w:rPr><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="34"/></w:rPr><w:pPr><w:spacing w:before="120" w:after="240"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:outlineLvl w:val="0"/><w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="27"/></w:rPr><w:pPr><w:keepNext/><w:spacing w:before="260" w:after="100"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:outlineLvl w:val="1"/><w:rPr><w:b/><w:color w:val="2F75B5"/><w:sz w:val="23"/></w:rPr><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/></w:pPr></w:style>
</w:styles>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    title = plain(source.read_text(encoding="utf-8").splitlines()[0].lstrip("# "))
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{escape(title)}</dc:title><dc:creator>MRP Project</dc:creator><cp:lastModifiedBy>MRP Project</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">2026-11-09T00:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-09T00:00:00Z</dcterms:modified></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>MRP checkpoint builder</Application></Properties>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, value in {
            "[Content_Types].xml": content_types, "_rels/.rels": root_rels,
            "word/document.xml": document, "word/styles.xml": styles,
            "word/_rels/document.xml.rels": doc_rels, "docProps/core.xml": core,
            "docProps/app.xml": app,
        }.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, value)
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    for markdown, docx in OUTPUTS.items():
        build(markdown, docx)
