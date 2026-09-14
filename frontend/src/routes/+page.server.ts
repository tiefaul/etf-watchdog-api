import { getStocks, getStockData, getStockPrice } from '../lib/components/dummy_data.ts'


interface Stocks {
  ticker_symbol: string;
  price: string;
  shares: string;
  company_name: string;
}


export const load = async () => {
  const listStocks: string[] = await getStocks();
  let stocks: Array<Stocks> = [];

  for (const ticker_symbol of listStocks) {
    let stockObj: Stocks = {ticker_symbol: '', price: '', shares: '', company_name: ''};
    let stockData = await getStockData(ticker_symbol);
    let stockPrice = await getStockPrice(ticker_symbol);
    stockObj.ticker_symbol = stockData.ticker_symbol;
    stockObj.company_name = stockData.company_name;
    stockObj.shares = '100';
    stockObj.price = stockPrice.close_price.toFixed(2).toString();
    stocks.push(stockObj);
  }
  return {stocks: stocks};
}
