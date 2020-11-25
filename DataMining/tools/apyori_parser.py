

ROUND_FLOAT = 2

def parse_rule(rule):
  item = rule
  pair = item[0]
  items = [x for x in item[0]]
  response = {}
  response["rule"] = (list(items)[0],list(items)[1])
  response["support"] = item[1]
  response["confidence"] = item[2][0][2]
  response["lift"] = item[2][0][3] 
  return response

def apriori_table_template():
    template = """
        <h4>Reglas</h4>
        <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Regla</th>
                <th scope="col">Soporte</th>
                <th scope="col">Confianza</th>
                <th scope="col">Elevación</th>
                <th scope="col">Descripción</th>
              </tr>
            </thead>
            <tbody>
                {data}
            </tbody>
        </table>
        <button class="btn btn-sm btn-primary">Ver Mas</button>
    """
    return template

def expl_rule_to_html(rule):
    return '{ant} <i class="fa fa-arrow-right" aria-hidden="true"></i>  {cons}'. format(ant=rule[0],cons=rule[1])

def desc_to_html(data):
    rule = data["rule"]
    return """
    {ant} y {cons} normalmente se compran juntos. 
    Dada la elevacion, hay {lift} mas probailidad de que 
    al comprar {ant} se compre {cons}.
    """.format(ant=rule[0],cons=rule[1], lift=data["lift"])

def rule_to_html(number,data):
    template = """
    <tr>
        <th scope="row">{number}</th>
        <td>{rule}</td>
        <td>{support}</td>
        <td>{confidence}</td>
        <td>{lift}</td>
        <td>{description}</td>
    </tr>
    """
    return template.format(number=number,rule=expl_rule_to_html(data["rule"]),support=round(data["support"],ROUND_FLOAT)\
                            ,confidence=round(data["confidence"],ROUND_FLOAT) \
                            ,lift = round(data["lift"],ROUND_FLOAT),description=desc_to_html(data))

def rules_to_html(rules):
    template = apriori_table_template()
    content = ""
    n=1
    for rule in rules:
        data = parse_rule(rule)
        content += rule_to_html(n,data)
        n += 1
    return template.format(data=content)