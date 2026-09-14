const base_url = 'http://127.0.0.1:8000/api/etfs/'


interface StockPrice {
  price_date: string;
  close_price: number;
  ticker_symbol: string;
}


interface StockData {
  ticker_symbol: string;
  id: number;
  company_name: string;
  currency: string;
}


interface CreateStock {
  ticker_symbol: string;
}


interface DeleteStock {
  success: string;
}


const getClient = async (path: string = '') => {
  try {
    const response = await fetch(`${base_url + path}`);
    if (!response.ok) {
      let responseError = await response.json();
      throw new Error(`${responseError.detail}`);
    }
    const result = await response.json();
    return result;
  } catch (error) {
    if (error instanceof Error) {
      console.error('API ERROR:', error.message);
    } else {
      console.error('An unknown error occured');
    }
  }
}


const postClient = async (body: CreateStock, path: string = '') => {
  try {
    const response = await fetch(`${base_url + path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body)
    });
    if (!response.ok) {
      let responseError = await response.json();
      throw new Error(`${responseError.detail}`);
    }
    const result = await response.json();
    return result;
  } catch (error) {
    if (error instanceof Error) {
      console. error('API ERROR:', error.message);
    } else {
      console.error('An unknown error occured');
    }
  }
}


const deleteClient = async (path: string = '') => {
  try {
    const response = await fetch(`${base_url + path}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      let responseError = await response.json();
      throw new Error(`${responseError.detail}`);
    }
    const result = await response.json();
    return result;
  } catch (error) {
    if (error instanceof Error) {
      console. error('API ERROR:', error.message);
    } else {
      console.error('An unknown error occured');
    }
  }
}


export const getStocks = async (): Promise<string[]> => {
  const data = await getClient();
  return data;
}


export const getStockPrice = async (ticker_symbol: string): Promise<StockPrice> => {
    const data = await getClient(`${ticker_symbol}/price`);
    return data;
}


export const getStockData = async (ticker_symbol: string): Promise<StockData> => {
  const data = await getClient(`${ticker_symbol}`);
  return data;
}


export const createStock = async (ticker_symbol: string): Promise<StockData> => {
  const payload = {'ticker_symbol': ticker_symbol};
  const data = await postClient(payload);
  return data;
}


export const deleteStock = async (ticker_symbol: string): Promise<DeleteStock> => {
  const data = await deleteClient(ticker_symbol);
  return data;
}

