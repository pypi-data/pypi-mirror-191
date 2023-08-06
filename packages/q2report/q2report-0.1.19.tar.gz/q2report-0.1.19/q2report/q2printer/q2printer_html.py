if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")
    from demo.demo_00 import demo

    demo()


from q2report.q2printer.q2printer import Q2Printer
from q2report.q2utils import int_
import webbrowser
import os


class Q2PrinterHtml(Q2Printer):
    def __init__(self, output_file, output_type=None):
        super().__init__(output_file, output_type)
        self.html = []
        self.style = {}

    def save(self):
        self.close_html_table()
        html = (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
            "\n<html>"
            "\n\t<head>"
            '\n\t\t<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>'
            '\n\t\t<meta name="generator" content="q2report"/>'
            '\n\t\t<style type="text/css">'
        )
        html += "".join([f"\n.{self.style[x]} {x}" for x in self.style])
        html += "@media print {body {print-color-adjust: exact;}}"
        html += "\n\t\t</style>" "\n\t</head>" "\n\t<body>\n\n"

        html += "\n".join(self.html)
        html += "\n\n\t</body>" "\n</html>"
        self._OF.write(html)
        return super().save()

    def reset_page(self, **args):
        super().reset_page(**args)
        size = f"{self.page_width}cm {self.page_height}cm;"
        margin = (
            f"{self.page_margin_top}cm "
            f"{self.page_margin_right}cm "
            f"{self.page_margin_bottom}cm "
            f"{self.page_margin_left}cm;"
        )
        style = '<style type="text/css"> @page {size:' + size + "margin:" + margin + "}" + "</style>"
        self.html.append(style)

    def reset_columns(self, widths):
        super().reset_columns(widths)
        self.close_html_table()
        self.html.append('<table style="border-collapse:collapse;">')
        self.html.append("<thead></thead>")
        self.html.append("<colgroup>")
        for col in self._cm_columns_widths:
            self.html.append(f'\t<col span="1" style="width: {col*10}mm;">')
        self.html.append("</colgroup>")

    def close_html_table(self):
        if self.html:
            self.html.append("</table>")

    def get_style_index(self, style):
        style_text = "; ".join([f"{x}:{style[x]}" for x in style])
        style_text = "{" + "border: solid;" + style_text + "}"
        if style_text not in self.style:
            self.style[style_text] = f"css{len(self.style)}"
        return self.style[style_text]

    def render_rows_section(self, rows, style, outline_level):
        super().render_rows_section(rows, style, outline_level)
        row_count = len(rows["heights"])
        spanned_cells = []
        if rows["role"] == "table_header":
            self.html.append("\t<thead>")
        for row in range(row_count):
            self.html.append("\t<tr>")
            for col in range(self._columns_count):
                key = f"{row},{col}"
                if key in spanned_cells:
                    continue
                cell_data = rows.get("cells", {}).get(key, {})
                cell_text = cell_data.get("data", "&nbsp;")
                row_span = cell_data.get("rowspan", 1)
                col_span = cell_data.get("colspan", 1)
                cell_style = cell_data.get("style", {})
                if cell_data.get("images"):
                    for x in cell_data.get("images"):
                        image = x["image"]
                        width, height, imageIndex = self.prepare_image(x, col)
                        cell_text = f"""
                                    <div style="background-image:url(data:image/jpeg;base64,{image});
                                                background-repeat:no-repeat;
                                                background-size: {width}cm {height}cm;
                                                width:{self._cm_columns_widths[col]}cm;
                                                height:{height}cm;
                                    ">
                                    {cell_text}
                                    </div>"""
                if cell_style:
                    tmp_style = dict(style)
                    tmp_style.update(cell_style)
                    style_index = self.get_style_index(tmp_style)
                else:
                    style_index = self.get_style_index(style)
                if row_span > 1 or col_span > 1:
                    span_text = f' colspan="{col_span}" rowspan="{row_span}"'
                    for span_row in range(int_(row_span)):
                        for span_col in range(int_(col_span)):
                            spanned_cells.append(f"{span_row+row},{span_col+col}")
                else:
                    span_text = " "
                self.html.append(f'\t\t<td class="{style_index}" {span_text}>{cell_text}</td>')
            self.html.append("\t</tr>")
        if rows["role"] == "table_header":
            self.html.append("\t</thead>")
        if rows["role"] == "table_footer":
            self.html.append("<thead></thead>")

    def show(self):
        # print(f"file://{os.path.abspath(self.output_file)}")
        webbrowser.open_new_tab(f"file://{os.path.abspath(self.output_file)}")
