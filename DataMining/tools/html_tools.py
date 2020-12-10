
class HTML_tools(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def option_html(value,text):
        template = """
        <option value="{}">{}</option>
        """
        return template.format(value,text)