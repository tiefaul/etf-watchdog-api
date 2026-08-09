 import { Stocks } from '../lib/components/dummy_data.ts'

 export function load() {
   return {
     stocks: Stocks.map((stock) => ({
       ticker_symbol: stock.ticker_symbol,
       price: stock.price,
       shares: stock.shares
     }))
   };
 }
