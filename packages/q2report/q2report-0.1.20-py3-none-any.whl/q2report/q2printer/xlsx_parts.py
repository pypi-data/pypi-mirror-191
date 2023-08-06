xlsx_parts = {}

xlsx_parts[
    "xl/drawings/drawing.xml(png)"
] = """
 <xdr:oneCellAnchor>
    <xdr:from>
        <xdr:col>%(_col)s</xdr:col>
        <xdr:colOff>0</xdr:colOff>
        <xdr:row>%(_row)s</xdr:row>
        <xdr:rowOff>0</xdr:rowOff>
    </xdr:from>
    <xdr:ext cx="%(_width)s" cy="%(_height)s"/>
    <xdr:pic>
        <xdr:blipFill>
            <a:blip r:embed="rId%(_id)s"/>
        </xdr:blipFill>
        <xdr:spPr bwMode="auto">
            <a:xfrm>
                <a:off x="3030990" y="328576"/>
                <a:ext cx="996723" cy="491254"/>
            </a:xfrm>
            <a:prstGeom prst="rect">
                <a:avLst/>
            </a:prstGeom>
            <a:noFill/>
            <a:ln w="9525">
                <a:noFill/>
                <a:miter lim="800000"/>
                <a:headEnd/>
                <a:tailEnd/>
            </a:ln>
        </xdr:spPr>
    </xdr:pic>
 </xdr:oneCellAnchor>"""


xlsx_parts[
    "xl/drawings/drawing.xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
            %s
    </xdr:wsDr>"""
xlsx_parts[
    "xl/drawings/_rels/drawing.xml.rels"
] = """<?xml version="1.0" encoding="UTF-8"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
        %s
    </Relationships>
    """
xlsx_parts[
    "xl/worksheets/sheet.xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

%s

    <sheetData>

%s

    </sheetData>

%s

%s

%s

</worksheet>"""
xlsx_parts[
    "xl/worksheets/_rels/sheet.xml.rels"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
        <Relationship Id="rId1"
            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing"
            Target="../drawings/drawing%s.xml"/>
        </Relationships>"""
xlsx_parts[
    "xl/workbook.xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <workbook
        xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
        <sheets>
            %s
        </sheets>
        <calcPr calcId="125725" calcOnSave="0"/>
    </workbook>"""
xlsx_parts[
    "xl/styles.xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                %(fonts)s
                <fills count="1">
                    <fill>
                        <patternFill patternType="none"/>
                    </fill>
                </fills>
                %(borders)s
                <cellStyleXfs count="1">
                    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
                </cellStyleXfs>
                %(cellXfs)s
                <cellStyles count="1">
                    <cellStyle name="20%% - Q1" xfId="0" builtinId="30" customBuiltin="1"/>
                </cellStyles>
                <dxfs count="0"/>
                <tableStyles count="0"
                    defaultTableStyle="TableStyleMedium9"
                    defaultPivotStyle="PivotStyleLight16"/>
            </styleSheet>"""
xlsx_parts[
    "xl/sharedStrings.xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
                        count="%s"
                        uniqueCount="%s">
                        %s
                    </sst>"""
xlsx_parts[
    "workbook.xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <workbook
        xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
        <sheets>
            <!-- <sheet name="Sheet1" sheetId="1" r:id="rId1"/>     -->
        </sheets>
        <calcPr calcId="125725" calcOnSave="0"/>
    </workbook>"""
xlsx_parts[
    "xl/_rels/workbook.xml.rels-line"
] = """<Relationship Id="rId%s"
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
        Target="worksheets/sheet%s.xml"/>"""
xlsx_parts[
    "xl/_rels/workbook.xml.rels"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                        <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                        <Relationship Id="rId3"
                            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
                            Target="styles.xml"/>
                        <Relationship Id="rId4"
                            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings"
                            Target="sharedStrings.xml"/>
                        %s
                        </Relationships>"""
xlsx_parts[
    "_rels/.rels"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                    <Relationship Id="rId1"
                    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
                    Target="xl/workbook.xml"/>
                </Relationships>"""
xlsx_parts[
    "[Content_Types].xml"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
                <Default Extension="png" ContentType="image/png"/>
                <Default Extension="jpg" ContentType="image/jpg"/>
                <Default Extension="rels"
                    ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
                <Default Extension="xml" ContentType="application/xml"/>
                <Override PartName="/xl/styles.xml"
                    ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
                <Override PartName="/xl/workbook.xml"
                    ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
                <Override PartName="/xl/sharedStrings.xml"
                    ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
                %s
                </Types>"""
xlsx_parts[
    "images"
] = """<Relationship Id="rId%s"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="../media/image%s.png"/>"""
xlsx_parts[
    "wb_content_types_sheet"
] = """<Override PartName="/xl/worksheets/sheet%s.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>"""
xlsx_parts[
    "wb_content_types_image"
] = """<Override PartName="/xl/drawings/drawing%s.xml"
        ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>
"""
