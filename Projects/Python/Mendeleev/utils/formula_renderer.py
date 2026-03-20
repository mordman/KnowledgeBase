"""Рендерер химических формул с поддержкой Markdown."""

import tkinter as tk
import re
import html

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

class FormulaRenderer:
    """Рендерер формул с поддержкой Markdown."""
    
    SUBSCRIPT_MAP = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ', 'h': 'ₕ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'p': 'ₚ',
        's': 'ₛ', 't': 'ₜ'
    }
    
    SUPERSCRIPT_MAP = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ'
    }
    
    def __init__(self, text_widget, settings=None):
        self.text = text_widget
        self.settings = settings or {}
        self._setup_tags()
    
    def _setup_tags(self):
        """Настраивает теги форматирования."""
        desc_font = self.settings.get('fonts', {}).get('detail_description', 
                        {"family": "Arial", "size": 11, "weight": "normal"})
        size = desc_font.get("size", 11)
        family = desc_font.get("family", "Arial")
        
        self.text.tag_configure("bold", font=(family, size, "bold"))
        self.text.tag_configure("italic", font=(family, size, "italic"))
        self.text.tag_configure("underline", font=(family, size, "underline"))
        self.text.tag_configure("heading", font=(family, size + 2, "bold"), spacing1=10, spacing3=5)
        self.text.tag_configure("list_item", lmargin1=20, lmargin2=20)
        self.text.tag_configure("normal", font=(family, size))
        self.text.tag_configure("subscript", font=(family, max(6, size - 3)), offset=-3)
        self.text.tag_configure("superscript", font=(family, max(6, size - 3)), offset=5)
    
    def render(self, content, format_type="auto"):
        """Рендерит контент."""
        self.text.delete("1.0", tk.END)
        
        if format_type == "auto":
            format_type = "html" if content.strip().startswith('<') else "markdown"
        
        if format_type == "html" and MARKDOWN_AVAILABLE:
            try:
                md = markdown.Markdown(extensions=['fenced_code', 'tables'])
                self._render_html(md.convert(content))
                return
            except:
                pass
        
        if format_type == "html":
            self._render_html(content)
        else:
            self._render_markdown(content)
    
    def _render_markdown(self, content):
        """Рендерит Markdown."""
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                self.text.insert(tk.END, "\n")
                continue
            
            if line.startswith('# '):
                self.text.insert(tk.END, line[2:] + "\n", "heading")
            elif line.startswith('- ') or line.startswith('• '):
                self.text.insert(tk.END, "• " + self._parse_formula(line[2:]) + "\n", "list_item")
            elif re.match(r'^\d+\.\s', line):
                self.text.insert(tk.END, self._parse_formula(line) + "\n", "list_item")
            else:
                self._insert_formatted_line(line)
    
    def _parse_formula(self, text):
        """Преобразует формулы H_2_O → H₂O."""
        result = []
        i = 0
        
        while i < len(text):
            if text[i] == '_' and i + 1 < len(text):
                end = text.find('_', i + 1)
                if end != -1:
                    for char in text[i + 1:end]:
                        result.append(self.SUBSCRIPT_MAP.get(char, char))
                    i = end + 1
                    continue
            
            if text[i] == '^' and i + 1 < len(text):
                end = text.find('^', i + 1)
                if end != -1:
                    for char in text[i + 1:end]:
                        result.append(self.SUPERSCRIPT_MAP.get(char, char))
                    i = end + 1
                    continue
            
            if text[i:i+2] == '**':
                end = text.find('**', i + 2)
                if end != -1:
                    result.append(text[i + 2:end])
                    i = end + 2
                    continue
            
            if text[i] == '*' and i + 1 < len(text) and text[i + 1] != '*':
                end = text.find('*', i + 1)
                if end != -1:
                    result.append(text[i + 1:end])
                    i = end + 1
                    continue
            
            result.append(text[i])
            i += 1
        
        return ''.join(result)
    
    def _insert_formatted_line(self, line):
        """Вставляет строку с форматированием."""
        processed = self._parse_formula(line)
        tags = ["normal"]
        
        if processed.startswith('**') and processed.endswith('**'):
            tags = ["bold"]
            processed = processed[2:-2]
        elif processed.startswith('*') and processed.endswith('*'):
            tags = ["italic"]
            processed = processed[1:-1]
        
        self.text.insert(tk.END, processed + "\n", tags)
    
    def _render_html(self, html_content):
        """Рендерит HTML."""
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        clean_text = html.unescape(clean_text)
        
        for line in clean_text.split('\n'):
            line = line.strip()
            if line:
                self.text.insert(tk.END, self._parse_formula(line) + "\n", "normal")
            else:
                self.text.insert(tk.END, "\n")