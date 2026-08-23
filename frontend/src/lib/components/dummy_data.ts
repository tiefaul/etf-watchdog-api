interface StockData {
  [key: string]: string;
}


export const Stocks: StockData[] = [
  {ticker_symbol: "SPCX", price: "100", shares: "10"},
  {ticker_symbol: "AAPL", price: "650", shares: "50"},
];
