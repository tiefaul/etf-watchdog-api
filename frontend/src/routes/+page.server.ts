import { getStocks, getStockData, getStockPrice, createStock } from '$lib/api/stocks';
import type { Actions } from './$types';


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
    console.log(`grabbing ${ticker_symbol}`)
    let stockData = await getStockData(ticker_symbol);
    let stockPrice = await getStockPrice(ticker_symbol);
    stocks.push({ticker_symbol: stockData.ticker_symbol,
                price: stockPrice.close_price.toFixed(2).toString(),
                shares: '100',
                company_name: stockData.company_name});
  }
  console.log('running loads')
  return {stocks: stocks};
}


export const actions = {
  default: async ({ request }) => {
    console.log('running form action')
    const data = await request.formData();
    await createStock(data.get('ticker_symbol'));
  }
} satisfies Actions;
