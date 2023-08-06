<?xml version="1.0" encoding="UTF-8" standalone="yes"?><ns2:ResponsePart xmlns:ns2="http://edds.egos.esa/model"><Response><ParamResponse><ParamSampleList>{% for row in param_sample_list %}<ParamSampleListElement>{% for key, val in row.items() %}<{{key}}>{{val}}</{{key}}>{% endfor %}</ParamSampleListElement>{% endfor %}</ParamSampleList></ParamResponse></Response></ns2:ResponsePart>

