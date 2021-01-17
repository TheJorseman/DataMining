
class HTML_tools(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def option_html(value,text):
        template = """
        <option value="{}">{}</option>
        """
        return template.format(value,text)

    @staticmethod
    def div_column(data, number=1):
        template = """
        <div class="col-{}">
            {}
        </div>
        """
        return template.format(number, data)

    @staticmethod
    def input_prepend(id, prepend, type_inp="text", disabled=True):
        input_template = """
            <label class="sr-only" for="{id}">Username</label>
            <div class="input-group mb-2">
            <div class="input-group-prepend">
                <div class="input-group-text">{prepend}</div>
            </div>
            <input type="{type}" class="form-control" id="{id}" placeholder="{id}" {disabled}>
            </div>
        """
        return input_template.format(id=id,prepend=prepend, type=type_inp, disabled = "disabled" if disabled else "")

    @staticmethod
    def input_column(id, prepend, type_inp="text", col_num=1, disabled=False):
        return div_column(input_prepend(id, prepend, type_inp), col_num=col_num, disabled=disabled)

    @staticmethod
    def input_from_list(inputs, disbled=False, required=False):
        template = """
        <div class="form-group">
            <label for="{var}">{var}</label>
            <input type="text" class="form-control" id="{var}"  {req}{dis}>
        </div>
        """
        html = ""
        for var_input in inputs:
            html += template.format(var=var_input, dis="disabled" if disbled else "", req="required" if required else "")
        return html