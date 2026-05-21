import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductsService } from './products.service';
import { Product } from './product.model';

@Component({
  selector: 'app-products-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section class="products">
      <h2>Catalogue</h2>

      <p *ngIf="loading()">Loading…</p>

      <ul *ngIf="!loading() && products().length > 0">
        <li *ngFor="let p of products()">
          <strong>{{ p.name }}</strong>
          — €{{ p.priceEur }} ({{ p.category }})
          <em *ngIf="p.stock === 0">— out of stock</em>
        </li>
      </ul>

      <p *ngIf="!loading() && products().length === 0">No products available.</p>
    </section>
  `,
  styles: [
    `
      .products { font-family: system-ui, sans-serif; padding: 1rem; }
      ul { list-style: none; padding: 0; }
      li { padding: 0.5rem 0; border-bottom: 1px solid #eee; }
    `,
  ],
})
export class ProductsListComponent implements OnInit {
  private readonly service = inject(ProductsService);

  readonly products = signal<Product[]>([]);
  readonly loading = signal(true);

  ngOnInit(): void {
    this.service.list().subscribe((items) => {
      this.products.set(items);
      this.loading.set(false);
    });
  }
}
