import pandas as pd


#function that takes in store data and preps it 
def prep_store(df):
    #converting the date data into a datetime format
    df.sale_date = df.sale_date.apply(lambda date: date[:-13])
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    # convert sales date to just date
    df = df.rename(columns={'sale_amount': 'quantity', 'sale_date':'date'})
    # Reassign the date column to be a datetime type
    pd.to_datetime(df.date, format='%a-%d-%b,%Y')
    # Set the index as that date and then sort index (by the date)
    df = df.set_index("date").sort_index()
    #  adding month and day of week columns, 
    df["month"] = df.index.strftime("%m-%b")
    df["day_of_week"]= df.index.strftime("%w-%a")
    # adding total sales feature
    df["total_sales"] = df.quantity * df.item_price
    # dropping uneccessary columns
    df = df.drop(columns = ["item_upc12","item_upc14"])
    return df

#function that takes in opsd data and preps it 
def prep_opsd(df):
    #replacing signs for underscore
    #convert upper case columns to 
    df.columns = [column.replace('+','_').lower() for column in df]
    # Reassign the date column to be a datetime type
    df.date = pd.to_datetime(df.date)
    # Set the index as that date and then sort index (by the date)
    df = df.set_index("date").sort_index()
    #- Plot the distribution of each of your variables.
    df["month"] = df.index.strftime("%m-%b")
    df["year"] = df.index.year
    #fill nulls due to having same data of zero
    df.fillna(0)
    return df

    