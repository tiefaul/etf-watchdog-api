interface StockData {
  [key: string]: string;
}


export const Stocks: StockData[] = [
  {ticker_symbol: "SPCX", price: "100", shares: "10", company_name: "SpaceX"},
  {ticker_symbol: "AAPL", price: "650", shares: "50", company_name: "Apple INC"},
  {ticker_symbol: "QQQ", price: "540", shares: "1000", company_name: "No Idea"},
];
