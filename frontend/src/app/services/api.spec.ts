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

  it('should start a dated import with the administrative header', () => {
    service
      .iniciarImportacao('despesas', 'chave-segura', {
        dataInicio: '2026-08-01',
        dataFim: '2026-08-31',
      })
      .subscribe((job) => expect(job.job_id).toBe('job-123'));

    const request = http.expectOne((candidate) => candidate.url === '/api/importacao/despesas');
    expect(request.request.method).toBe('POST');
    expect(request.request.headers.get('X-Admin-Key')).toBe('chave-segura');
    expect(request.request.params.get('data_inicio')).toBe('2026-08-01');
    expect(request.request.params.get('data_fim')).toBe('2026-08-31');
    request.flush({ job_id: 'job-123', status: 'PENDING' });
  });

  it('should fetch an import status with the administrative header', () => {
    service.consultarImportacao('job-123', 'chave-segura').subscribe();

    const request = http.expectOne('/api/importacao/jobs/job-123');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('X-Admin-Key')).toBe('chave-segura');
    request.flush({ job_id: 'job-123', status: 'SUCCESS', resultado: {} });
  });
});
