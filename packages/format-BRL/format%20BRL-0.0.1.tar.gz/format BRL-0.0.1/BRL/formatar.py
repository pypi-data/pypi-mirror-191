def format_value(valor=0):
    try:
        valorf = f"R$ {valor:,.2f}"
        pos = valorf.find(".")
        lista_format = list(valorf)
        valorf = "".join(lista_format)
        valorf = valorf.replace(",",".")
        lista_format = list(valorf)
        lista_format[pos] = ","
        valorf = "".join(lista_format)
        return valorf
    except:
        return "R$0,00"