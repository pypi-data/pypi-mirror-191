if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")
    from demo.demo_00 import demo

    demo()


from q2report.q2printer.q2printer import Q2Printer
from q2report.q2printer.docx_parts import docx_parts
from q2report.q2utils import num, int_, reMultiSpaceDelete
import zipfile
import base64

points_in_mm = 2.834645669
points_in_cm = num(points_in_mm) * num(10)
twip_in_cm = num(points_in_cm) * num(20)


class Q2PrinterDocx(Q2Printer):
    def __init__(self, output_file, output_type=None):
        super().__init__(output_file, output_type)
        self.document = []
        self.xmlImageList = []
        self.images_size_list = []
        self.document.append(docx_parts["doc_start"])
        self.page_params = None
        self.table_opened = False

    def save(self):
        super().save()
        self.close_docx_table()

        self.document.append(self.page_params)
        self.document.append("</w:body>")
        self.document.append("</w:document>")

        zipf = zipfile.ZipFile(self.output_file, "w", zipfile.ZIP_DEFLATED)

        relImage = []
        for x in range(len(self.xmlImageList)):
            zipf.writestr("word/media/image%s.png" % x, base64.b64decode(self.xmlImageList[x]))
            relImage.append(docx_parts["images"] % (x, x))

        zipf.writestr("_rels/.rels", docx_parts["rels"])
        zipf.writestr("[Content_Types].xml", docx_parts["content_type"])
        zipf.writestr("word/_rels/document.xml.rels", docx_parts["word_rels"] % "".join(relImage))
        zipf.writestr("word/document.xml", "".join(self.document).encode("utf8"))
        zipf.close()

    def reset_page(
        self,
        page_width=21,
        page_height=29,
        page_margin_left=2,
        page_margin_top=1,
        page_margin_right=1,
        page_margin_bottom=1,
    ):
        super().reset_page(
            page_width,
            page_height,
            page_margin_left,
            page_margin_top,
            page_margin_right,
            page_margin_bottom,
        )

        self.close_docx_table()
        if self.page_params:
            self.document.append(self.page_params)
        self.page_params = self.get_page_params()

    def get_page_params(self):
        page_xml = f"""
<w:p>
    <w:pPr>
        <w:sectPr>
            <w:type w:val="nextPage"/>
            <w:pgSz w:w="{self.page_width * twip_in_cm}" w:h="{self.page_height * twip_in_cm}"/>
            <w:pgMar w:gutter="0" w:header="708" w:footer="708"
                    w:top="{self.page_margin_top * twip_in_cm}"
                    w:right="{self.page_margin_right * twip_in_cm}"
                    w:bottom="{self.page_margin_bottom * twip_in_cm}"
                    w:left="{self.page_margin_left * twip_in_cm}"
            />
            <w:cols w:space="708"/>
            <w:docGrid w:linePitch="360"/>
            <w:formProt w:val="false"/>
            <w:textDirection w:val="lrTb"/>
        </w:sectPr>
        <w:rPr/>
    </w:pPr>
    <w:r>
        <w:rPr/>
    </w:r>
    <w:r>
        <w:br w:type="page"/>
    </w:r>
</w:p>"""
        return page_xml

    def reset_columns(self, widths):
        self.close_docx_table()
        super().reset_columns(widths)
        self.table_opened = True
        self.document.append(
            """<w:tbl>
                                <w:tblPr>
                                    <w:tblLayout w:type="fixed"/>
                                    <w:tblInd w:w="28" w:type="dxa"/>
                                    <w:tblCellMar>
                                        <w:top w:w="28" w:type="dxa"/>
                                        <w:left w:w="28" w:type="dxa"/>
                                        <w:bottom w:w="28" w:type="dxa"/>
                                        <w:right w:w="28" w:type="dxa"/>
                                    </w:tblCellMar>
                                </w:tblPr>
                                <w:tblGrid>\n"""
        )

        for col in self._cm_columns_widths:
            self.document.append(f'\t\t<w:gridCol w:w="{int_(col * twip_in_cm)}"/>\n')
        self.document.append("""\t</w:tblGrid>\n""")

    def close_docx_table(self):
        if self._columns_count and self.table_opened:
            self.document.append("</w:tbl>\n")
            self.document.append("<w:p><w:r><w:rPr/></w:r></w:p>\n")
            self.table_opened = False

    def render_rows_section(self, rows, style, outline_level):
        super().render_rows_section(rows, style, outline_level)
        row_count = len(rows["heights"])
        spanned_cells = {}

        for row in range(row_count):  # вывод - по строкам
            self.open_table_row()
            if rows["role"] == "table_header":
                self.document.append('<w:trPr><w:tblHeader w:val="true"/></w:trPr>')

            for col in range(self._columns_count):  # цикл по клеткам строки
                key = f"{row},{col}"
                cell_data = rows.get("cells", {}).get(key, {})
                cell_text = cell_data.get("data", "")
                row_span = cell_data.get("rowspan", 1)
                col_span = cell_data.get("colspan", 1)
                cell_style = dict(style)
                # col_width = int(self._cm_columns_widths[col] * twip_in_cm)

                if key in spanned_cells:
                    if spanned_cells[key] == "":
                        continue
                    else:
                        self.add_table_cell(cell_style, "", col, spanned_cells[key])
                    continue

                if cell_data.get("style", {}):
                    cell_style.update(cell_data.get("style", {}))
                merge_str = ""
                if row_span > 1 or col_span > 1:
                    if col_span > 1:
                        merge_str = f'<w:gridSpan w:val="{col_span}"/>'
                    if row_span > 1:
                        merge_str += '<w:vMerge w:val="restart"/>'
                    for span_row in range(int_(row_span)):
                        for span_col in range(int_(col_span)):
                            span_key = f"{span_row+row},{span_col+col}"
                            if row_span > 1:
                                spanned_cells[span_key] = "<w:vMerge/>" * row_span
                            else:
                                spanned_cells[span_key] = ""

                self.add_table_cell(
                    cell_style,
                    cell_text,
                    col,
                    merge_str,
                    self.get_cell_images(cell_data.get("images"), col),
                )

            self.close_table_row()

    def get_cell_images(self, images_list, col):
        cell_images_list = []
        if not images_list:
            return ""
        for x in images_list:
            width, height, imageIndex = self.prepare_image(x, col)

            width = num(width) * num(12700) * points_in_cm
            height = num(height) * num(12700) * points_in_cm

            cell_images_list.append(docx_parts["image"] % locals())
        return "\n".join(cell_images_list)

    def open_table_row(self):
        self.document.append("\n\t<w:tr>")
        # self.document.append("\n\t\t<w:trPr>")
        # self.document.append('\n\t\t\t<w:trHeight w:val="2268" w:hRule="exact"/>')
        # self.document.append("\n\t\t</w:trPr>")
        pass

    def close_table_row(self):
        self.document.append("\n\t</w:tr>")

    def add_table_cell(self, cell_style, cell_text, col, merge_str, images=[]):
        borders = self.get_cell_borders(cell_style)
        margins = self.get_cell_paddings(cell_style)
        para_params = self.get_paragraph_params(cell_style)
        para_text = self.get_paragraph_text(cell_style, cell_text)
        valign = self.get_vertical_align(cell_style)

        self.document.append(
            f"""
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:w="{int(self._cm_columns_widths[col] * twip_in_cm)}" w:type="dxa"/>
                        {valign}
                        {merge_str}
                        {borders}
                        {margins}
                    </w:tcPr>
                    <w:p>
                        {para_params}
                        {para_text}
                        {images}
                    </w:p>
                </w:tc>
        """
        )

    def get_paragraph_text(self, cell_style, cell_text):
        cell_text = reMultiSpaceDelete.sub(" ", cell_text)
        para_text = []
        if "font-weight" in cell_style and cell_style["font-weight"] == "bold":
            cell_text = f"<b>{cell_text}</b>"
        bold = ""
        ital = ""
        undl = ""
        fontsizemod = fontsize = num(cell_style["font-size"].replace("pt", "")) * 2
        fontfamily = cell_style["font-family"]
        for x in cell_text.split("<"):
            if ">" in x:
                stl = x.split(">")[0].upper().strip().replace(" ", "")
                if "B" == stl:
                    bold = "<w:b/>"
                elif "/B" == stl:
                    bold = ""
                elif "I" == stl:
                    ital = "<w:i/>"
                elif "/I" == stl:
                    ital = ""
                elif "U" == stl:
                    undl = """<w:u w:val="single"/>"""
                elif "/U" == stl:
                    undl = ""
                elif "/FONT" in stl:
                    fontsizemod = fontsize
                # elif "FONTSIZE=" in stl:
                #     fontsizemod = grid.getFontSizeMod(fontsize / 2, stl.split("=")[1]) * 2
                elif "BR/" == stl or "BR" == stl:
                    para_text.append("""</w:p>""")
                    para_text.append(self.get_paragraph_params(cell_style))
                x = x.split(">")[1]
            if x:
                para_text.append(
                    f"""
                    <w:r>
                        <w:rPr>
                            <w:rFonts w:ascii="{fontfamily}" w:hAnsi="{fontfamily}" w:cs="{fontfamily}"/>
                            <w:sz w:val="{fontsizemod}"/>
                            {bold}{ital}{undl}
                        </w:rPr>
                        <w:t xml:space="preserve">{x}</w:t>
                    </w:r>
                    """
                )
        return "".join(para_text)

    def get_paragraph_params(self, cell_style):
        paragraph = f"""
<w:pPr>
\t{self.get_horizontal_align(cell_style)}
\t<w:widowControl w:val="0"/>
\t<w:adjustRightInd w:val="0"/>
\t<w:autoSpaceDE w:val="0"/>
\t<w:autoSpaceDN w:val="0"/>
\t<w:spacing w:before="0" w:after="0" w:lineRule="atLeast" w:line="0"/>
</w:pPr>"""
        return paragraph

    def get_vertical_align(self, cell_style):
        if cell_style["vertical-align"] == "middle":
            vert_align = '<w:vAlign w:val="center"/>'
        elif cell_style["vertical-align"] == "bottom":
            vert_align = '<w:vAlign w:val="bottom"/>'
        else:
            vert_align = ""
        return vert_align

    def get_horizontal_align(self, cell_style):
        if cell_style["text-align"] == "center":
            hor_align = '<w:jc w:val="center"/>'
        elif cell_style["text-align"] == "right":
            hor_align = '<w:jc w:val="right"/>'
        elif cell_style["text-align"] == "justify":
            hor_align = '<w:jc w:val="both"/>'
        else:
            hor_align = ""
        return hor_align

    def get_cell_borders(self, cell_style):
        border_width = cell_style["border-width"].split(" ")
        while len(border_width) < 4:
            border_width += border_width
        borders = []
        borders.append("<w:tcBorders>\n")
        for index, side in enumerate(("top", "right", "bottom", "left")):
            if int_(border_width[index]):
                borders.append(f'\t\t\t<w:{side} w:val="single" w:color="auto" w:space="0"')
                borders.append(f'\t\t\t\tw:sz="{int_(border_width[index])*10}"/>')
        borders.append("</w:tcBorders>\n")
        return "\n".join(borders)

    def get_cell_paddings(self, cell_style):
        padding = cell_style["padding"].replace("cm", "").split(" ")
        while len(padding) < 4:
            padding += padding
        margins = []
        margins.append("\n\t<w:tcMar>")
        for index, side in enumerate(("top", "right", "bottom", "left")):
            margins.append(f'\n\t\t<w:{side} w:w="{int(num(padding[index])*twip_in_cm)}" w:type="dxa"/>')
        margins.append("\n\t</w:tcMar>\n")
        return "".join(margins)
