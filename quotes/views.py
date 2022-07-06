# 'quotes views.py'

from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm


# Home page
def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        # Stock query params
        api_token = "pk_beb96a87bbd74a90860e98f7c537c702"
        stock_symbol = ticker

        # Try to get the quote from IEX
        try:
            api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + stock_symbol \
                + '/quote?token=' + api_token)

            # Load the returned json for parsing
            api_request_result_json = json.loads(api_request.content)

            # Parse the shot on the home.html if you're too poor for Postman (it's free)
            #final_result = " (" + str(api_request_result_json["companyName"]) + "): " + \
            #    str(api_request_result_json["latestPrice"])

            final_result = api_request_result_json
            

        except Exception as e:
            final_result = "Something's fucky, Julian."


        # Return the result, good or bad
        return render(request, 'home.html', {"get_quote_result": final_result})


    # Form hasn't been submitted yet, show quote for APPL or whoever pays the most for the ad space :-)
    else:
        #return render(request, 'home.html', {"ticker": "Look up a symbol, top right my dude."})

        # Stock query params
        api_token = "pk_beb96a87bbd74a90860e98f7c537c702"
        stock_symbol = "aapl"

        # Try to get the quote from IEX
        try:
            api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + stock_symbol \
                + '/quote?token=' + api_token)

            # Load the returned json for parsing
            api_request_result_json = json.loads(api_request.content)

            # Parse the json and return the final result
            # We'll parse the shot on the home.html instead
            #final_result = " (" + str(api_request_result_json["companyName"]) + "): " + \
            #    str(api_request_result_json["latestPrice"])

            final_result = api_request_result_json
            

        except Exception as e:
            final_result = "Something's fucky, Julian."


        # Return the result, good or bad
        return render(request, 'home.html', {"get_quote_result": final_result})



# About page
def about(request):
    return render(request, 'about.html', {})




# Portfolio page
def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        submitted_symbol = request.POST['symbol']

        if form.is_valid():
            form.save()
            messages.success(request, (submitted_symbol + " was added to portfolio."))
            return redirect('add_stock')

    else:
        # Get all the stocks in the database - all rows
        all_stocks_in_db = Stock.objects.all()

        # Load the table with API called data for each stock
        api_token = "pk_beb96a87bbd74a90860e98f7c537c702"

        # Empty list to keep all the looped stuff below
        output = []

        # Loop?
        for stock in all_stocks_in_db:
            stock_symbol = stock.symbol

            # Try to get the quote from IEX
            try:
                api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + str(stock_symbol) \
                    + '/quote?token=' + api_token)

                # Load the returned json for parsing
                api_request_result_json = json.loads(api_request.content)
                output.append(api_request_result_json)

                # Save properties to the database, how?

            except Exception as e:
                final_result = "Something's fucky, Julian."

            # Return the result
            #return render(request, 'add_stock.html', {"stock": api_request_result_json})

        # Return the result
        return render(request, 'add_stock.html', {'stocks': all_stocks_in_db, "output": output})
        #return render(request, 'add_stock.html', {"stock": api_request_result_json})



def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, (item.symbol + " has been removed."))
    return redirect('delete_stock')



# About page
def delete_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        submitted_symbol = request.POST['symbol']

        if form.is_valid():
            form.save()
            messages.success(request, (submitted_symbol + " was added to portfolio."))
            return redirect('delete_stock')

    else:
        # Get all the stocks in the database - all rows
        all_stocks_in_db = Stock.objects.all()
        return render(request, 'delete_stock.html', {'all_stocks': all_stocks_in_db})



