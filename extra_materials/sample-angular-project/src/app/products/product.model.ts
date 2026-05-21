export interface Product {
  id: string;
  name: string;
  priceEur: number;
  stock: number;
  category: 'consulting' | 'training' | 'license';
}

export interface ProductsResponse {
  items: Product[];
  total: number;
}
