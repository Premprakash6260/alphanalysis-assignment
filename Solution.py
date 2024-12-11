import csv
from datetime import date
import yfinance as yf


ddate = input("Enter the date (YYYY-MM-DD): ")

# Take user input for amount
amount = float(input("Enter your investable amount: "))

filename = "Output_" + ddate + ".csv"

with open('Stocks_new.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row

    with open(filename, 'w', newline='') as output_file:
      csv_writer = csv.writer(output_file)
      csv_writer.writerow(['Ticker', 'Weightage', ddate])

      for line in csv_reader:
          try:
              ticker = line[0].strip()  # Get the ticker from the first column
              weightage = line[1].strip()
              print(f"Fetching data for ticker: {ticker}")
              
              # Download historical data for the ticker
              stocks = yf.download(ticker)
              
              # Check if data is returned
              if stocks.empty:
                  print(f"No data found for ticker: {ticker}")
                  csv_writer.writerow([ticker, weightage, "No Data Found"])
              else:
                  # Extract the closing price for the specified date
                  closing_price = stocks.loc[ddate, 'Close']
                  # Ensure we write only the scalar value
                  if isinstance(closing_price, (float, int)):  # Scalar value
                    closing_price = round(closing_price, 2)  # Round to 2 decimal places
                  else:  # Handle Series (if the index is not scalar)
                    closing_price = round(closing_price.values[0], 2)

                  amount_to_invest = float(weightage) * amount

                  shares_bought = round(amount_to_invest/closing_price, 2)
                  
                  csv_writer.writerow([ticker, weightage, shares_bought])
          except KeyError:
              print(f"No data available for {ticker} on {ddate}.")
          except Exception as e:
              print(f"An error occurred for ticker {ticker}: {e}")