import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ApiService } from './api';

describe('ApiService', () => {
  let service: ApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('should use the same-origin API proxy', () => {
    service.buscarInformacoes('12345678000199').subscribe((empresa) => {
      expect(empresa.razao_social).toBe('Empresa teste');
    });

    const request = http.expectOne('/api/cnpj/informacoes/12345678000199');
    expect(request.request.method).toBe('GET');
    request.flush({ codigo_favorecido: '12345678000199', razao_social: 'Empresa teste' });
  });

  it('should reuse cached company requests', () => {
    service.buscarInformacoes('12345678000199').subscribe();
    http.expectOne('/api/cnpj/informacoes/12345678000199').flush({
      codigo_favorecido: '12345678000199',
      razao_social: 'Empresa teste',
    });

    service.buscarInformacoes('12345678000199').subscribe();
    http.expectNone('/api/cnpj/informacoes/12345678000199');
  });
});
