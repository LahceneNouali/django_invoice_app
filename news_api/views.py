from django.shortcuts import render
import requests
import json


def home(request):
    searchItem = request.GET.get('SearchItem')

    if searchItem:
        url = f'https://elhoussam.github.io/invoicesapi/db.json'
        response = requests.get(url)
        data = response.json()

        # Invoices JSON object
        inv_str = '[]'

        # Parse JSON string to Python dictionary
        inv_obj = json.loads(inv_str)

        for invoice in data:
            InvoiceItems = invoice['InvoiceItems']
            for item in InvoiceItems:
                if searchItem.upper() in item['ItemLibelle'].upper():
                    # Add invoice object to JSON object
                    inv_obj.append(invoice)

        for invoice in inv_obj:
            total_amount = 0
            invoiceItems = invoice['InvoiceItems']

            for item in invoiceItems:
                total_amount = total_amount + (item['ItemPrice']*item['ItemQuantity']) + item['ItemTax']

            invoice['TotalAmount'] = total_amount

        context = {
            'invoices': inv_obj
        }

        return render(request, 'news_api/home.html', context)

    else:
        url = f'https://elhoussam.github.io/invoicesapi/db.json'
        response = requests.get(url)
        data = response.json()

        for invoice in data:
            total_amount = 0
            invoiceItems = invoice['InvoiceItems']

            for item in invoiceItems:
                total_amount = total_amount + (item['ItemPrice']*item['ItemQuantity']) + item['ItemTax']

            invoice['TotalAmount'] = total_amount

        context = {
            'invoices': data
        }

        return render(request, 'news_api/home.html', context)




def invoice(request):
    searchItem = request.GET.get('SearchItem')

    url = f'https://elhoussam.github.io/invoicesapi/db.json'
    response = requests.get(url)
    data = response.json()

    # Invoices JSON object
    inv_str = '[]'

    # Parse JSON string to Python dictionary
    inv_obj = json.loads(inv_str)

    for invoice in data:
        if invoice['InvoiceID'] == searchItem:
            # Add invoice object to JSON object
            inv_obj.append(invoice)

            total = 0
            tva = 0
            total_amount = 0
            invoiceItems = invoice['InvoiceItems']

            for item in invoiceItems:
                ht = (item['ItemPrice'] * item['ItemQuantity'])
                ttc = (item['ItemPrice'] * item['ItemQuantity']) + item['ItemTax']
                item['HT'] = ht
                item['TTC'] = ttc

                total = total + (item['ItemPrice'] * item['ItemQuantity'])
                tva = tva + item['ItemTax']
                total_amount = total_amount + (item['ItemPrice'] * item['ItemQuantity']) + item['ItemTax']

            invoice['Total'] = total
            invoice['Tva'] = tva
            invoice['TotalAmount'] = total_amount

            updated_json_str = json.dumps(inv_obj)

            context = {
                'invoices': inv_obj
            }

            return render(request, 'news_api/invoice.html', context)