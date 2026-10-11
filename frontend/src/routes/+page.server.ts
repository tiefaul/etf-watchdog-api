import { getStocks, createStock } from '$lib/api/stocks';
import type { Actions } from './$types';


interface Stocks {
  ticker_symbol: string;
  price: string;
  shares: string;
  company_name: string;
}


export const load = async () => {
  const listStocks = await getStocks();
  let stocks: Array<Stocks> = [];

  listStocks.forEach((stock) => 
    stocks.push({
         ticker_symbol: stock.ticker_symbol,
         price: stock.close_price.toFixed(2).toString(),
         shares: '100',
         company_name: stock.company_name
       }));
  return {stocks: stocks};
  }


export const actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    await createStock(data.get('ticker_symbol') as string);
  }
} satisfies Actions;
