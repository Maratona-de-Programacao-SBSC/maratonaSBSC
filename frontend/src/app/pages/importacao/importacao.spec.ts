import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { ApiService } from '../../services/api';
import { ImportacaoComponent } from './importacao';

describe('ImportacaoComponent', () => {
  let component: ImportacaoComponent;
  let fixture: ComponentFixture<ImportacaoComponent>;
  let apiMock: {
    iniciarImportacao: ReturnType<typeof vi.fn>;
    consultarImportacao: ReturnType<typeof vi.fn>;
    mensagemErro: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    apiMock = {
      iniciarImportacao: vi.fn(() => of({ job_id: 'job-123', status: 'PENDING' })),
      consultarImportacao: vi.fn(() => of({ job_id: 'job-123', status: 'SUCCESS', resultado: {} })),
      mensagemErro: vi.fn((_error: unknown, fallback: string) => fallback),
    };

    await TestBed.configureTestingModule({
      imports: [ImportacaoComponent],
      providers: [{ provide: ApiService, useValue: apiMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(ImportacaoComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should require an administrative key', () => {
    component.chaveAdministrativa = '';
    component.iniciar();

    expect(component.erro()).toContain('chave administrativa');
    expect(apiMock.iniciarImportacao).not.toHaveBeenCalled();
  });

  it('should start a dated import with the selected period', () => {
    component.chaveAdministrativa = 'chave-segura';
    component.dataInicio = '2026-08-01';
    component.dataFim = '2026-08-31';
    component.iniciar();

    expect(apiMock.iniciarImportacao).toHaveBeenCalledWith('despesas', 'chave-segura', {
      dataInicio: '2026-08-01',
      dataFim: '2026-08-31',
    });
    expect(component.job()?.job_id).toBe('job-123');
  });

  it('should require confirmation before a full CNPJ import', () => {
    component.selecionarTipo('cnpj');
    component.chaveAdministrativa = 'chave-segura';
    component.iniciar();

    expect(component.erro()).toContain('carga completa');
    expect(apiMock.iniciarImportacao).not.toHaveBeenCalled();
  });

  it('should expose the import button in the rendered form', () => {
    const button = fixture.nativeElement.querySelector('.submit-button') as HTMLButtonElement;
    expect(button.textContent).toContain('Iniciar importação');
  });
});
