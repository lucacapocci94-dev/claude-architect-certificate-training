import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ProductsService } from './products.service';
import { Product, ProductsResponse } from './product.model';

describe('ProductsService', () => {
  let service: ProductsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ProductsService],
    });
    service = TestBed.inject(ProductsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('list() unwraps the items array', (done) => {
    const fake: ProductsResponse = {
      items: [
        { id: 'p1', name: 'Architect day', priceEur: 1200, stock: 5, category: 'consulting' },
      ],
      total: 1,
    };

    service.list().subscribe((items) => {
      expect(items.length).toBe(1);
      expect(items[0].name).toBe('Architect day');
      done();
    });

    const req = httpMock.expectOne('/api/products');
    expect(req.request.method).toBe('GET');
    req.flush(fake);
  });

  it('list() returns [] when the server errors out', (done) => {
    service.list().subscribe((items) => {
      expect(items).toEqual([]);
      done();
    });
    httpMock.expectOne('/api/products').error(new ProgressEvent('boom'));
  });

  it('getById() returns null when product is missing', (done) => {
    service.getById('nope').subscribe((product) => {
      expect(product).toBeNull();
      done();
    });
    httpMock.expectOne('/api/products/nope').flush(null, { status: 404, statusText: 'Not Found' });
  });
});
