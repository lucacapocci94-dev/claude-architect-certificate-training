import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { ProductsListComponent } from './products-list.component';
import { ProductsService } from './products.service';
import { Product } from './product.model';

describe('ProductsListComponent', () => {
  let fixture: ComponentFixture<ProductsListComponent>;
  let serviceSpy: jasmine.SpyObj<ProductsService>;

  const fakeProducts: Product[] = [
    { id: 'p1', name: 'Architect day', priceEur: 1200, stock: 3, category: 'consulting' },
    { id: 'p2', name: 'Claude bootcamp', priceEur: 800, stock: 0, category: 'training' },
  ];

  beforeEach(async () => {
    serviceSpy = jasmine.createSpyObj<ProductsService>('ProductsService', ['list', 'getById']);
    serviceSpy.list.and.returnValue(of(fakeProducts));

    await TestBed.configureTestingModule({
      imports: [ProductsListComponent],
      providers: [{ provide: ProductsService, useValue: serviceSpy }],
    }).compileComponents();

    fixture = TestBed.createComponent(ProductsListComponent);
    fixture.detectChanges();
  });

  it('renders one <li> per product', () => {
    const lis = fixture.nativeElement.querySelectorAll('li');
    expect(lis.length).toBe(2);
  });

  it('shows an "out of stock" marker for products with stock=0', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('out of stock');
  });
});
