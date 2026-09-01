import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ConsultasComponent } from './consulta';
import { provideRouter } from '@angular/router';
import { ApiService } from '../../services/api';
import { apiServiceMock } from '../../testing/api-service.mock';

describe('Consulta', () => {
  let component: ConsultasComponent;
  let fixture: ComponentFixture<ConsultasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsultasComponent],
      providers: [provideRouter([]), { provide: ApiService, useValue: apiServiceMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(ConsultasComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should format a CNPJ while typing', () => {
    expect(component.formatarCnpj('12345678000199')).toBe('12.345.678/0001-99');
  });

  it('should reject an incomplete CNPJ', () => {
    component.cnpjInput = '12.345';
    component.pesquisar();
    expect(component.erro()).toContain('14 números');
  });
});
