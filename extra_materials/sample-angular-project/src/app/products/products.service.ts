import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, map, of } from 'rxjs';
import { Product, ProductsResponse } from './product.model';

const API_BASE = '/api/products';

@Injectable({ providedIn: 'root' })
export class ProductsService {
  private readonly http = inject(HttpClient);

  list(): Observable<Product[]> {
    return this.http.get<ProductsResponse>(API_BASE).pipe(
      map((res) => res.items),
      catchError(() => of([])),
    );
  }

  getById(id: string): Observable<Product | null> {
    return this.http.get<Product>(`${API_BASE}/${id}`).pipe(
      catchError(() => of(null)),
    );
  }
}
